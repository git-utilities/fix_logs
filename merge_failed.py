#!/usr/bin/env python3


import argparse
import json
import sys

from lib import (
    fix_merge,
    git,
    GitException,
    os_cd,
    parent_directory_name,
)


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


def main(args):
    """
    **Parameters**

    - `config_path` String, path to `failed.json` log file

    **Example**

        main("./failed.json")
    """
    with open(args.get('failed', './failed.json'), 'r') as failed_fd:
        failed_json = json.load(failed_fd)

    defaults = {
        'no_push': args.get('no_push', failed_json.get('no_push')),
        'verbose': args.get('verbose', failed_json.get('verbose'))
    }

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

    if conflicts_list:
        with open('conflicts.json', 'a') as conflicts_fd:
            json.dump(conflicts_list, conflicts_fd)
            print("Wrote conflicts to -> conflicts.json")

    if merged_list:
        with open('merged.json', 'a') as merged_fd:
            json.dump(merged_list, merged_fd)
            print("Wrote merged to -> merged.json")


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


main(args_dict)
