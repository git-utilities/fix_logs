#!/usr/bin/env python3


import argparse
import json
import sys

from lib import (git, GitException, os_cd, parent_directory_name)


__about__ = '''
Written for those that did not Fork properly
'''


__description__ = '''
Simple Python script that runs `git mergtool` en-mass
'''


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


if __name__ != '__main__':
    raise NotImplementedError("Try running as a script, eg. python file-name.py --help")


def fix_merge(repo):
    """
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


def main(args_dict):
    """
    **Parameters**

    - `args_dict`, expects dictionary similar to...

        {
            "about": None,
            "failed": "./failed.json",
            "license": None,
            "verbose": True,
        }

    **Example**

        main({"failed": "./failed.json", "verbose": True})

    **Returns**

        {
            "merged": [
                'repository_dir': "repo['repository_dir']",
                'repository_source': "repo['source']",
            ],

            "failed": [
                'repository_dir': "repo['repository_dir']",
                'message': "e.message",
                'code': "e.status['code']",
                'err': "e.status['err']",
                'out': "e.status['out']",
            ]
        }
    """
    with open(args_dict['failed'], 'r') as failed_fd:
        failed_json = json.load(failed_fd)

    conflicts_list = []
    merged_list = []
    for repo in failed_json:
        os_cd(repo['repository_dir'])

        try:
            status = git(['mergetool'], "cannot resolve conflicts", True)
        except GitException as e:
            conflicts_list.append({
                'repository_dir': repo['repository_dir'],
                'message': e.message,
                'code': e.status['code'],
                'err': e.status['err'],
                'out': e.status['out']
            })
            if args_dict['verbose']:
                print("{error_message}".format(error_message = e.message))
        else:
            status.update({
                'repository_dir': repo['repository_dir'],
                'repository_source': repo['source']
            })
            merged_list.append(status)
            if args_dict['verbose']:
                print("Fixed: {}".format(parent_directory_name(repo['repository_dir'])))

    return {
        "conflicts": conflicts_list,
        "merged": merged_list,
    }


parser = argparse.ArgumentParser(description = __description__)

parser.add_argument('--about',
                    action = 'store_true',
                    help = 'Prints info about this script and exits')

parser.add_argument('--failed',
                    default = './failed.json',
                    help = 'Path to failed.json file')

parser.add_argument('--license',
                    action = 'store_true',
                    help = 'Prints script license and exits')

parser.add_argument('--verbose',
                    action = 'store_true',
                    help = 'Prints command standard out if set')

args_dict = vars(parser.parse_args())

if args_dict['about']:
    print(__about__)
    sys.exit()

if args_dict['license']:
    print(__license__)
    sys.exit()


results = main(args_dict)
conflicts = results.get('conflicts')
if conflicts:
    with open('conflicts.json', 'a') as conflicts_fd:
        json.dump(conflicts, conflicts_fd)
        print("Wrote conflicts to -> conflicts.json")


merged = results.get('merged')
if merged:
    with open('merged.json', 'a') as merged_fd:
        json.dump(merged, merged_fd)
        print("Wrote merged to -> merged.json")
