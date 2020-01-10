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

    - `configs` Dictionary, similar to

        {
          "fixed": "./fixed.json",
          "failed": "./failed.json",
          "defaults": {
            "origin_branch": "master",
            "origin_remote": "origin",
            "source_branch": "master",
            "source_remote": "source",
            "fix_branch": "fix",
            "fix_commit": "Fixes logs"
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

    - `origin_branch`
    - `origin_remote`
    - `source_branch`
    - `source_remote`
    - `fix_branch`
    - `fix_commit`
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

    git(['remote', 'add', source_remote, repo['source']], "Cannot add remote {source}".format(**repo))
    git(['fetch', source_remote, source_branch], "Cannot fetch {source}".format(**repo))

    latest_hash = git(['log', '-1', '--format="%h"', "{remote}/{branch}".format(
        remote = origin_remote,
        branch = origin_branch)],
        "Cannot retrieve hash for {remote}".format(remote = origin_remote))['out']

    source_hash = git(['log', '-1', '--format="%h"', "{remote}/{branch}".format(
        remote = source_remote,
        branch = source_branch)],
        "Cannot retrieve hash for {remote}".format(remote = source_remote))['out']

    git(['checkout', source_hash], "Cannot checkout {remote} {hash}".format(
        remote = source_remote,
        hash = source_hash))

    git(['checkout', '-b', "{fix_branch}".format(
        fix_branch = fix_branch)],
        "Cannot checkout {fix_branch}".format(
            fix_branch = fix_branch))

    git(['merge', latest_hash], "Cannot auto-merge {remote} {hash}".format(
        remote = origin_remote,
        hash = latest_hash))

    git(['commit', '-m', "{fix_commit}".format(
        fix_commit = fix_commit)], "Cannot commit to {fix_branch}".format(
            fix_branch = fix_branch))

    git(['checkout', "{remote}/{branch}".format(
        remote = origin_remote,
        branch = origin_branch)], "Cannot checkout {remote}/{branch}".format(
            remote = origin_remote,
            branch = origin_branch))

    git(['merge', fix_branch], "Cannot auto-merge {fix_branch}".format(
        fix_branch = fix_branch))

    git(['push', '--force', origin_remote, origin_branch], "Cannot push {remote} {branch}".format(
        remote = origin_remote,
        branch = origin_branch))

    git(['branch', '--delete', fix_branch], "Cannot delete {fix_branch}".format(
        fix_branch = fix_branch))

    return {
        'code': 0,
        'err': '',
        'out': "Finished fixing {dir}".format(dir = repo['dir'])
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