#!/usr/bin/env python3


import json
import os
import subprocess


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
        self.status = status


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

        git(['status'], "Cannot read git status", True)

    **Returns** dictionary from `run(cmd)` function

    **Throws/Raises** `GitException`

        - if exit `code` is greater than `0`
        - or if `err` (Standard Error) contains output
    """
    status = run(['git'] + arg_list)
    if status['code'] > 0 or status['err']:
        raise GitException(error_message, status)

    if verbose:
        print(status['out'])

    return status


def fix(repo, configs):
    """
    Attempts to fix git log for `repo`

    **Parameters**

    - `repo` Dictionary, similar to...

        {
            "dir": "_local-git-directory_",
            "source": "_remote-git-url_"
        }

    - `configs` Dictionary, similar to...

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

    **Returns** dictionary similar to `run(cmd)` function output

    **Note**, each individual `repo` may overwrite `default` configurations

    - `origin_branch` Git branch name to merge source `source_branch` with
    - `origin_remote` Get remote name to push changes to
    - `source_branch` Git branch to _inject_ into `origin_branch`
    - `source_remote` Git remote name to fetch log corrections from
    - `fix_branch` Git branch name to _triage_ merge conflicts with
    - `fix_commit` Git commit message for successful merges
    - `keep_fix_branch` If `True`, skips attempting to push to `origin_remote` after merge
    - `no_push` If `True`, skips deleting `fix_branch` after merge
    """
    if os.path.isdir(repo['dir']) is False:
        raise TypeError("No directory at {dir}".format(**repo))

    os.chdir(os.path.abspath(repo['dir']))

    origin_branch = repo.get('origin_branch', configs['origin_branch'])
    origin_remote = repo.get('origin_remote', configs['origin_remote'])
    source_branch = repo.get('source_branch', configs['source_branch'])
    source_remote = repo.get('source_remote', configs['source_remote'])
    fix_branch = repo.get('fix_branch', configs['fix_branch'])
    fix_commit = repo.get('fix_commit', configs['fix_commit'])

    no_push = repo.get('no_push', configs.get('no_push'))
    keep_fix_branch = repo.get('keep_fix_branch', configs.get('keep_fix_branch'))

    verbose = configs.get('verbose', False)

    git(arg_list = ['remote', 'add', source_remote, repo['source']],
        error_message = "Cannot add remote {source}".format(**repo),
        verbose = verbose)

    git(arg_list = ['fetch', source_remote, source_branch],
        error_message = "Cannot fetch {source}".format(**repo),
        verbose = verbose)

    latest_hash = git(arg_list = ['log', '-1', '--format="%h"', "{remote}/{branch}".format(
            remote = origin_remote,
            branch = origin_branch)],
        error_message = "Cannot retrieve hash for {remote}".format(remote = origin_remote),
        verbose = verbose)['out']

    source_hash = git(arg_list = ['log', '-1', '--format="%h"', "{remote}/{branch}".format(
            remote = source_remote,
            branch = source_branch)],
        error_message = "Cannot retrieve hash for {remote}".format(remote = source_remote),
        verbose = verbose)['out']

    git(arg_list = ['checkout', source_hash],
        error_message = "Cannot checkout {remote} {hash}".format(remote = source_remote, hash = source_hash),
        verbose = verbose)

    git(arg_list = ['checkout', '-b', "{fix_branch}".format(fix_branch = fix_branch)],
        error_message = "Cannot checkout {fix_branch}".format(fix_branch = fix_branch),
        verbose = verbose)

    git(arg_list = ['merge', latest_hash],
        error_message = "Cannot auto-merge {remote} {hash}".format(remote = origin_remote, hash = latest_hash),
        verbose = verbose)

    git(arg_list = ['commit', '-m', "{fix_commit}".format(fix_commit = fix_commit)],
        error_message = "Cannot commit to {fix_branch}".format(fix_branch = fix_branch),
        verbose = verbose)

    git(arg_list = ['checkout', "{remote}/{branch}".format(remote = origin_remote, branch = origin_branch)],
        error_message = "Cannot checkout {remote}/{branch}".format(remote = origin_remote, branch = origin_branch),
        verbose = verbose)

    git(arg_list = ['merge', fix_branch],
        error_message = "Cannot auto-merge {fix_branch}".format(fix_branch = fix_branch),
        verbose = verbose)

    if not keep_fix_branch:
        git(arg_list = ['branch', '--delete', fix_branch],
            error_message = "Cannot delete {fix_branch}".format(fix_branch = fix_branch),
            verbose = verbose)

    out_message = "Finished fixing {dir}".format(dir = repo['dir'])
    if not no_push:
        git(arg_list = ['push', '--force', origin_remote, origin_branch],
            error_message = "Cannot push {remote} {branch}".format(remote = origin_remote, branch = origin_branch),
            verbose = verbose)
        out_message = "Skipped pushing to {remote} {branch}".format(remote = source_remote, branch = source_branch)

    return {
        'code': 0,
        'err': '',
        'out': out_message
    }


def main(config_path):
    """
    Parses `config.json` file and loops over each repository within `config['repos']`

    Writes fixed log to file defined by `config['fixed']`

    Writes failures log to file defined by `config['failed']`

    **Parameters**

    - `config_path` String, path to `config.json` configuration file
    """
    failed_list = []
    fixed_list = []
    with open(config_path, 'r') as configs_fd:
        configs = json.load(configs_fd)

    for repo in configs['repos']:
        try:
            status = fix(repo, configs)
        except GitException as e:
            failed_list.append({
                'repository_dir': repo['dir'],
                'message': e.message,
                'code': e.status['code'],
                'err': e.status['err'],
                'out': e.status['out']
            })
            if configs.get('verbose'):
                print("{message} -> {dir}".format(message = e.message, dir = repo['dir']))
        else:
            status.update({
                'repository_dir': repo['dir'],
                'repository_source': repo['source']
            })
            fixed_list.append(status)
            if configs.get('verbose'):
                print("Fixed and pushed -> {dir}".format(dir = repo['dir']))

    if failed_list and configs['failed']:
        with open(configs['failed'], 'a') as failed_fd:
            json.dump(failed_list, failed_fd)
            print("Wrote failures to {failed}".format(failed = configs['failed']))

    if fixed_list and configs['fixed']:
        with open(configs['fixed'], 'a') as fixed_fd:
            json.dump({"fixed": fixed_list}, fixed_fd)
            print("Wrote fixes to {fixed}".format(fixed = configs['fixed']))


if __name__ == '__main__':
    raise NotImplementedError("Try running importing as module, eg. import lib")
