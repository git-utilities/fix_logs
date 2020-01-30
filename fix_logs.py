#!/usr/bin/env python3


import argparse
import sys

from lib import fix_logs_main


__about__ = '''
Written for those that did not Fork properly
'''


__description__ = '''
Simple Python script that attempts to fix git logs/history en-mass
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


parser = argparse.ArgumentParser(description = __description__)

parser.add_argument('--about',
                    action = 'store_true',
                    help = 'Prints info about this script and exits')

parser.add_argument('--config',
                    default = './config.json',
                    help = 'Path to config.json file')

parser.add_argument('--merge_strategy',
                    default = 'source',
                    help = 'Git merge strategy to use, check `git help merge | less -p "-X <option>"`')

parser.add_argument('--origin_branch',
                    default = 'master',
                    help = 'Git branch name to merge source `source_branch` with')

parser.add_argument('--origin_remote',
                    default = 'origin',
                    help = 'Get remote name to push changes to')

parser.add_argument('--source_branch',
                    default = 'master',
                    help = 'Git branch to _inject_ into `origin_branch`')

parser.add_argument('--source_remote',
                    default = 'source',
                    help = 'Git remote name to fetch log corrections from')

parser.add_argument('--no_push',
                    action = 'store_true',
                    help = 'Skips attempting to push to `origin_remote` after merge')

parser.add_argument('--keep_fix_branch',
                    action = 'store_true',
                    help = 'Skips deleting `fix_branch` after merge')

parser.add_argument('--license',
                    action = 'store_true',
                    help = 'Prints script license and exits')

parser.add_argument('--verbose',
                    action = 'store_true',
                    help = 'Prints command standard out if set')

args = vars(parser.parse_args())

if args['about']:
    print(__about__)
    sys.exit()

if args['license']:
    print(__license__)
    sys.exit()

fix_logs_main(args)
