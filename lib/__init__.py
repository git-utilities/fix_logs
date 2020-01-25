#!/usr/bin/env python3


import json
import os
import subprocess
import srblib


__license__ = '''
Git Fix Logs
Copyright (C) 2020  S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation; version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''


class GitException(Exception):
    """
    Raise error from `run` git commands

    **Properties**

    - `self.message` String, error message
    - `self.status` Dictionary, returned from `run(cmd)` function
    """

    def __init__(self, message, status):
        super(GitException, self).__init__(message)
        self.message = message
        self.status = status


def os_cd(path):
    """
    A short-cut for _`cd` like_ commands

    **Throws**

    - `Throws/Raises` if path does not exist
    """
    abspath = srblib.abs_path(path)
    if os.path.isdir(abspath) is False:
        raise TypeError("No directory at {abspath}".format(abspath = abspath))

    os.chdir(abspath)


def run(cmd):
    """
    **Parameters**

    - `cmd` should be a list, eg. `run(['git', 'status'])`

    **Returns** dictionary similar to...

        {
            "code": _number_,
            "out": "_standard-out_",
            "err": "_standard-error_"
        }

    - `code` contains the exit code/status of command run
    - `out` may contain Standard Out
    - `err` may contain Standard Error
    """
    pipes = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = pipes.communicate()
    return {
        'code': pipes.returncode,
        'out': out,
        'err': err
    }


def git(arg_list, error_message, verbose = False):
    """
    **Parameters**

    - `arg_list` List, Git args to send to `run(cmd)` function
    - `error_message` String, message to print and log if errors are detected
    - `verbose` Boolean, if `True` then prints success and failure messages

    **Example**

        git(['status'], "cannot read git status", True)

    **Returns** dictionary from `run(cmd)` function

    **Throws/Raises** `GitException`

        - if exit `code` is greater than `0`
        - or if `err` (Standard Error) contains output
    """
    if verbose:
        print("arg_list -> {}".format(arg_list))

    status = run(['git'] + arg_list)
    if status['code'] > 0 and status['err']:
        raise GitException(error_message, status)
    elif status['err']:
        print(status['err'].decode("utf-8"))

    if verbose:
        print("status['out'] -> {}".format(status['out']))

    return status


def parent_directory_name(path):
    """
    **Notes**

    This function could also be a lambda

        parent_directory_name = lambda path: os.path.abspath(path).split(os.path.sep)[-2]
    """
    return os.path.abspath(path).split(os.path.sep)[-1]
    # return os.path.abspath(path).split(os.path.sep)[-2]


def consolidate_repo_configs(defaults, repo):
    """
    Merges `defaults` into `repo` and returns Dictionary

    **Parameters**

    - `defaults` Dictionary, similar to...

        {
          "fixed": "./fixed.json",
          "failed": "./failed.json",
          "defaults": {
            "origin_branch": "master",
            "origin_remote": "origin",
            "source_branch": "master",
            "source_remote": "source",
            "fix_branch": "fix",
            "fix_commit": "Fixes logs",
            "keep_fix_branch": false,
            "no_push": false
          },
          "repos": [
            {
              "dir": "~/git/hub/llSourcell/Bitcoin_Trading_Bot",
              "source": "https://github.com/jaungiers/Multidimensional-LSTM-BitCoin-Time-Series.git"
            },
            {
              "dir": "~/git/hub/llSourcell/How-to-Predict-Stock-Prices-Easily-Demo",
              "source": "git@github.com:jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction.git"
            },
            {
              "dir": "~/git/hub/llSourcell/How_to_simulate_a_self_driving_car",
              "source": "git@github.com:naokishibuya/car-behavioral-cloning.git"
            }
          ]
        }

    - Expects `repo` dictionary, similar to...

        {
            "dir": "_local-git-directory_",
            "source": "_remote-git-url_",
        }


    **Returns**, dictionary, similar to...

        {
            "dir": "_local-git-directory_",
            "source": "_remote-git-url_",
            "name": "_repo-name_",
            "origin_branch": "master",
            "origin_remote": "origin",
            "source_branch": "master",
            "source_remote": "source",
            "fix_branch": "fix",
            "fix_commit": "Fixes logs",
            "keep_fix_branch": false,
            "no_push": false
        }

    **Note**

    New `repo['name']` is optional and defaults to parent directory name of `repo['dir']` for backwards compatibility

    Each `repo` may overwrite `default` configurations for...

    - `origin_branch` Git branch name to merge source `source_branch` with
    - `origin_remote` Get remote name to push changes to
    - `source_branch` Git branch to _inject_ into `origin_branch`
    - `source_remote` Git remote name to fetch log corrections from
    - `fix_branch` Git branch name to _triage_ merge conflicts with
    - `fix_commit` Git commit message for successful merges
    - `keep_fix_branch` If `True`, skips attempting to push to `origin_remote` after merge
    - `no_push` If `True`, skips deleting `fix_branch` after merge
    """
    repo_configs = {
        "dir": repo['dir'],
        "source": repo['source'],
        "origin_branch": repo.get('origin_branch', defaults['origin_branch']),
        "origin_remote": repo.get('origin_remote', defaults['origin_remote']),
        "source_branch": repo.get('source_branch', defaults['source_branch']),
        "source_remote": repo.get('source_remote', defaults['source_remote']),
        "fix_branch": repo.get('fix_branch', defaults['fix_branch']),
        "fix_commit": repo.get('fix_commit', defaults['fix_commit']),
        "no_push": repo.get('no_push', defaults.get('no_push')),
        "keep_fix_branch": repo.get('keep_fix_branch', defaults.get('keep_fix_branch')),
        "verbose": defaults.get('verbose', False),
    }
    repo_configs['name'] = repo.get('origin_branch', parent_directory_name(repo_configs['dir'])),

    return repo_configs


def fix_log(repo):
    """
    Attempts to fix git log for `repo`

    **Returns** dictionary similar to `run(cmd)` function output

    **Parameters**

    - Expects `repo` to be a dictionary similar to...

        {
            "dir": "_local-git-directory_",
            "source": "_remote-git-url_",
            "name": "repo-name",
            "origin_branch": "master",
            "origin_remote": "origin",
            "source_branch": "master",
            "source_remote": "source",
            "fix_branch": "fix",
            "fix_commit": "Fixes logs",
            "keep_fix_branch": false,
            "no_push": false
        }

    **Raises**

    - `ValueError` with message similar to...

        Cannot obtain `latest_hash` or `source_hash`
    """
    os_cd(repo['dir'])

    git(arg_list = ['remote', 'add', repo['source_remote'], repo['source']],
        error_message = "{name} cannot add `source_remote` or `source`".format(**repo),
        verbose = repo['verbose'])

    # git(arg_list = ['fetch', repo['source_remote'], "{source_branch}:{source_remote}/{source_branch}".format(**repo)],
    git(arg_list = ['fetch', repo['source_remote']],
        error_message = "{name} cannot fetch `source_remote` or `source_branch`".format(**repo),
        verbose = repo['verbose'])

    # Notice, the following two variables are probably considered _porcelain_ for Git CLI
    latest_hash = git(
        arg_list = ['log', '-1', '--format="%h"', "{origin_remote}/{origin_branch}".format(
            origin_remote = repo['origin_remote'],
            origin_branch = repo['origin_branch'])],
        error_message = "{name} cannot retrieve hash for `origin_remote` or `origin_branch`".format(**repo),
        verbose = repo['verbose']
    )['out'].decode("utf-8")

    source_hash = git(
        arg_list = ['log', '-1', '--format="%h"', "{source_remote}/{source_branch}".format(**repo)],
        error_message = "{name} cannot retrieve hash for `source_remote` or `source_branch`".format(**repo),
        verbose = repo['verbose']
    )['out'].decode("utf-8")

    if not latest_hash or not source_hash:
        ValueError("cannot obtain `latest_hash` or `source_hash`")

    git(arg_list = ['checkout', source_hash],
        error_message = "{name} cannot checkout last hash for `source_remote` or `source_remote`".format(**repo),
        verbose = repo['verbose'])

    git(arg_list = ['checkout', '-b', "{fix_branch}".format(fix_branch = repo['fix_branch'])],
        error_message = "{name} cannot checkout `fix_branch` or `fix_branch`".format(**repo),
        verbose = repo['verbose'])

    git(arg_list = ['merge', latest_hash],
        error_message = "{name} cannot merge `latest_hash` {latest_hash}".format(latest_hash = latest_hash, **repo),
        verbose = repo['verbose'])

    git(arg_list = ['commit', '-m', "{fix_commit}".format(fix_commit = repo['fix_commit'])],
        error_message = "{name} cannot commit to `fix_branch`".format(**repo),
        verbose = repo['verbose'])

    git(arg_list = ['checkout', "{origin_remote}/{origin_branch}".format(**repo)],
        error_message = "{name} cannot checkout `origin_remote` or `origin_branch`".format(**repo),
        verbose = repo['verbose'])

    git(arg_list = ['merge', repo['fix_branch']],
        error_message = "{name} cannot auto-merge `fix_branch`".format(**repo),
        verbose = repo['verbose'])

    if not repo['keep_fix_branch']:
        git(arg_list = ['branch', '--delete', repo['fix_branch']],
            error_message = "{name} cannot delete `fix_branch`".format(**repo),
            verbose = repo['verbose'])

    out_message = "Finished fixing {dir}".format(dir = repo['dir'])
    if not repo['no_push']:
        git(arg_list = ['push', '--force', repo['origin_remote'], repo['origin_branch']],
            error_message = "{name} cannot push `origin_remote` or `origin_branch`".format(**repo),
            verbose = repo['verbose'])

        out_message = "{name} skipped pushing to `source_remote` `source_branch`".format(**repo)

    return {
        'code': 0,
        'err': '',
        'out': out_message
    }


def fix_merge(repo):
    """
    **Returns** dictionary similar to `run(cmd)` function output

    **Parameters**

    - Expects `repo` to be a dictionary similar to...

        {
            "dir": "_local-git-directory_",
            "source": "_remote-git-url_",
            "name": "repo-name",
            "origin_branch": "master",
            "origin_remote": "origin",
            "source_branch": "master",
            "source_remote": "source",
            "fix_branch": "fix",
            "fix_commit": "Fixes logs",
            "keep_fix_branch": false,
            "no_push": false
        }

    **Raises**

    - `ValueError` with message similar to...

        Cannot obtain `latest_hash` or `source_hash`
    """
    git(['mergetool'], "cannot resolve conflicts", True)
    out_message = "Finished fixing {dir}".format(dir = repo['dir'])
    if not repo['no_push']:
        git(arg_list = ['push', '--force', repo['origin_remote'], repo['origin_branch']],
            error_message = "{name} cannot push `origin_remote` or `origin_branch`".format(**repo),
            verbose = repo['verbose'])

        out_message = "{name} skipped pushing to `source_remote` `source_branch`".format(**repo)

    return {
        'code': 0,
        'err': '',
        'out': out_message
    }


def fix_logs_main(args):
    """
    Parses `config.json` file and loops over each repository within `config['repos']`

    Writes fixed log to file defined by `config['fixed']`

    Writes failures log to file defined by `config['failed']`

    **Parameters**

    - `config_path` String, path to `config.json` configuration file
    """
    git_dir = "{}".format(os.path.sep).join(__file__.split(os.path.sep)[0:-2])
    with open(args.get('config', './config.json'), 'r') as configs_fd:
        configs = json.load(configs_fd)

    defaults = {
        'origin_branch': args.get('origin_branch', configs.get('origin_branch')),
        'origin_remote': args.get('origin_remote', configs.get('origin_remote')),
        'source_branch': args.get('source_branch', configs.get('source_branch')),
        'source_remote': args.get('source_remote', configs.get('source_remote')),
        'fix_branch': args.get('fix_branch', configs.get('fix_branch')),
        'fix_commit': args.get('fix_commit', configs.get('fix_commit')),
        'keep_fix_branch': args.get('keep_fix_branch', configs.get('keep_fix_branch')),
        'no_push': args.get('no_push', configs.get('no_push')),
        'verbose': args.get('verbose', configs.get('verbose')),
        'repos': configs['repos'],
    }

    failed_list = []
    fixed_list = []
    for repo in defaults['repos']:
        repo_configs = consolidate_repo_configs(defaults, repo)
        try:
            status = fix_log(repo_configs)
        except GitException as e:
            failed_list.append({
                'repository_dir': repo_configs['dir'],
                'message': e.message,
                'code': e.status['code'],
                'err': e.status['err'].decode("utf-8"),
                'out': e.status['out'].decode("utf-8"),
            })
            if repo_configs['verbose']:
                print("{error_message}".format(error_message = e.message))
        else:
            status.update({
                'repository_dir': repo_configs['dir'],
                'repository_source': repo_configs['source']
            })
            fixed_list.append(status)
            if repo_configs['verbose']:
                print("Fixed: {name}".format(**repo_configs))

    os_cd(git_dir)
    if failed_list and configs['failed']:
        failed_abspath = srblib.abs_path(configs['failed'])
        print("failed_abspath -> {}".format(failed_abspath))
        with open(failed_abspath, 'w') as failed_fd:
            json.dump({'failed': failed_list}, failed_fd)
            print("Wrote failures to -> {failed}".format(**configs))

    if fixed_list and configs['fixed']:
        fixed_abspath = srblib.abs_path(configs['fixed'])
        with open(fixed_abspath, 'w') as fixed_fd:
            json.dump({"fixed": fixed_list}, fixed_fd)
            print("Wrote fixes to -> {fixed}".format(configs))


if __name__ == '__main__':
    raise NotImplementedError("Try running importing as module, eg. import lib")
