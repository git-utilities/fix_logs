## Git Fix Logs
[heading__title]:
  #git-fix-logs
  "&#x2B06; Top of ReadMe File"


Python scripts to assists with Git merging origin over source  en-mass.


- when multiple remote repositories are missing license files, and/or commit history from a Fork gone wrong

- when one or two _`git push --force remote branch`_ commands isn't enough

- for categorizing multiple repositories that cannot be automatically fixed and pushed; as well as why


## [![Byte size of fix_logs][badge__master__fix_logs__source_code]][fix_logs__master__source_code] [![Open Issues][badge__issues__fix_logs]][issues__fix_logs] [![Open Pull Requests][badge__pull_requests__fix_logs]][pull_requests__fix_logs] [![Latest commits][badge__commits__fix_logs__master]][commits__fix_logs__master]


------


- [:building_construction: Requirements][heading__requirements]

- [:zap: Quick Start][heading__quick_start]

- [&#x1F5D2; Notes][notes]

- [:shell: Command Line Examples][heading__command_line_examples]

- [:card_index: Attribution][heading__attribution]

- [:balance_scale: License][heading__license]


------



## Requirements
[heading__requirements]:
  #requirements
  "&#x1F3D7; What is needed prior to making use of this repository"


The Git command line utility is required for doing version management stuff.

This script makes use of the following built-in Python libraries...


```
argparse
json
os
subprocess
sys
```


Pip install additional requirements via...


```Bash
pip install --user -r requirements.txt
```


It is also a good idea to learn how to [resolve merge conflicts](https://stackoverflow.com/questions/161813/how-to-resolve-merge-conflicts-in-git)


Optionally see [Python Guide -- `virtualenvs`](https://docs.python-guide.org/dev/virtualenvs/) for information on running this project, and it's dependencies, within a _Virtual Environment_, TLD...


```Bash
pip3 install --user pipenv

pipenv install -r requirements.txt

# pipenv run python3 fix_logs.py
# pipenv run python3 merge_failed.py
```


___


## Quick Start
[heading__quick_start]:
  #quick-start
  "&#9889; Perhaps as easy as one, 2.0,..."


Make a place to clone this repository and download the source code...


```Bash
mkdir -vp ~/git/hub/git-utilities


cd ~/git/hub/git-utilities


git clone git@github.com:git-utilities/fix_logs.git
```


Customize configuration file...


```Bash
cd fix_logs


vim config.json
```


**`config.json`**


```JSON
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
      "source": "git@github.com:jaungiers/Multidimensional-LSTM-BitCoin-Time-Series.git"
    }
  ]
}
```

> Example of adding to the list of `repos`...


```JSON
{
  "fixed": "fixed.json",
  "failed": "failed.json",
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
      "source": "git@github.com:jaungiers/Multidimensional-LSTM-BitCoin-Time-Series.git"
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
```


------


> **Note, `defaults` may be overwritten for individual `repos`**


```JSON
    "repos": [
      {
        "dir": "",
        "source": "",
        "origin_branch": "master",
        "origin_remote": "hub",
        "source_branch": "tests",
        "source_remote": "source",
        "fix_branch": "fix-merge",
        "fix_commit": "Fixes logs",
        "keep_fix_branch": false,
        "no_push": true
      }
    ]
```


------


Run the `fix_logs.py` script...


```Bash
python3 fix_logs.py --help


python3 fix_logs.py --config ./config.json
```

___


## Notes
[notes]:
  #notes
  "&#x1F5D2; Additional notes and links that may be worth clicking in the future"


This project is **not** feature complete and is intended as a quick-fix/starting-point for those that didn't Fork repositories correctly. [Pull Requests][pull_requests__fix_logs] are welcomed for fixing bugs or adding features, or [Open an Issue][issues__fix_logs] if assistance is needed with resolving bugs or adding features.


Success and failure logs are saved under `./fixed.json` and `./failed.json` by default. Though this may be modified by editing the `config.json` file to point to different paths.


Example **`fixed.json`** data...


```JSON
{
  "fixed": [
    {
      "dir": "~/git/hub/account-name/Bitcoin_Trading_Bot",
      "source": "https://github.com/jaungiers/Multidimensional-LSTM-BitCoin-Time-Series.git",
      "origin_branch": "master",
      "origin_remote": "origin",
      "source_branch": "master",
      "source_remote": "source",
      "fix_branch": "fix",
      "fix_commit": "Fixes logs",
      "keep_fix_branch": false,
      "no_push": false,
      "code": 0,
      "err": "",
      "out": "Finished fixing /home/user-name/git/hub/account-name/Bitcoin_Trading_Bot"
    }
  ]
}
```


Example **`failed.json`** data...


```JSON
{
  "failed": [
    {
      "dir": "/home/user-name/git/hub/account-name/repo-name",
      "source": "https://github.com/author/project.git",
      "origin_branch": "master",
      "origin_remote": "hub",
      "source_branch": "tests",
      "source_remote": "source",
      "fix_branch": "fix-merge",
      "fix_commit": "Fixes logs",
      "keep_fix_branch": false,
      "no_push": true,
      "message": "Cannot auto-merge <remote> <hash>",
      "code": "1",
      "err": "e.run['err']",
      "out": ""
    }
  ]
}
```


... It's a good idea to double check that _`fixed`_ repositories genuinely have their logs corrected. And anything logged as _`failed`_ should have Git logs corrected manually; check the [Command Line Examples][heading__command_line_examples] section of this document for hints on that.


___


## Command Line Examples
[heading__command_line_examples]:
  #command-line-examples
  "&#x1F41A; Bash example for correcting a single git log"


Bash example for correcting a single git repository


```Bash
cd ~/git/hub/llSourcell/Bitcoin_Trading_Bot

# Add `source` remote and fetch `master` branch history
git remote add source git@github.com:jaungiers/Multidimensional-LSTM-BitCoin-Time-Series.git
git fetch source master

# Last commit ref (git hash) of source/master
git checkout a8aaab3

# Use a temporary `fix` branch to _quarantine_ possible conflicts
git checkout -b fix-fork

# Merge last commit ref (git hash) of origin/master
git merge 91d9d98
# git merge -X theirs 91d9d98
# Note, using `-X theirs` strategy instead may reduce chances of conflict

#
## Handle any marge conflicts before proceeding
#

git commit -m 'Fixes logs'

# Checkout default branch and merge _fixes_
git checkout master
git merge fix-fork

# Delete _quarantine_ branch and force push to remote
git branch --delete fix-fork
git push --force origin master
```


Regardless of checked-out status one may use the following format...


```Bash
# git log -1 --format='%h' <remote>/<branch>
```


... to obtain last hash for `<remote>/<branch>`


Note, above example's merge to last commit (hash `91d9d98`) process will _fast-forward_ any commits between detected divergence.


Merge conflicts may occur in which case `vimdiff` is an excellent command line utility for resolving differences manually; hint check for [_`vimdiff` cheat sheets_](https://gist.github.com/azadkuh/5d223d46a8c269dadfe4) with preferred web search service.


___


## Attribution
[heading__attribution]:
  #attribution
  "&#x1F4C7; Resources that where helpful in building this project so far."


- [Git documentation -- merge strategies](https://git-scm.com/docs/merge-strategies)

- [StackOverflow -- storing python dictionaries](https://stackoverflow.com/questions/7100125)

- [StackOverflow -- python try else](https://stackoverflow.com/questions/855759)

- [StackOverflow -- how do you append to a file in python](https://stackoverflow.com/questions/4706499)

- [StackOverflow -- proper way to declare custom exceptions in modern python](https://stackoverflow.com/questions/1319615)

- [StackOverflow -- manually raising throwing an exception in python](https://stackoverflow.com/questions/2052390)

- [StackOverflow -- get exit code and stderr from subprocess call](https://stackoverflow.com/questions/16198546)

- [StackOverflow -- how to retrieve the hash for the current commit in git](https://stackoverflow.com/questions/949314)

- [StackOverflow -- catch multiple exceptions in one line except block](https://stackoverflow.com/questions/6470428)

- [StackOverflow -- how to resolve merge conflicts in git](https://stackoverflow.com/questions/161813)

- [StackOverflow -- How to get an absolute file path in Python](https://stackoverflow.com/a/54190233)

- [StackOverflow -- Convert bytes to a string](https://stackoverflow.com/questions/606191)

- [StackOverflow -- How can I find scripts directory with Python](https://stackoverflow.com/questions/4934806)

- [StackOverflow -- Bash -- Read a file line by line assigning the value to a variable](https://stackoverflow.com/questions/10929453)

- [StackOverflow -- Retroactively forking a project on GitHub](https://stackoverflow.com/questions/48120641)

- [Python Docs -- `argparse`](https://docs.python.org/3/howto/argparse.html)

- [Gist Cheat Sheet -- `vimdiff`](https://gist.github.com/azadkuh/5d223d46a8c269dadfe4)

- [Python Guide -- `virtualenvs`](https://docs.python-guide.org/dev/virtualenvs/)

___


## License
[heading__license]:
  #license
  "&#x2696; Legal bits of Open Source software"


Legal bits of Open Source software. Note the following license does **not** necessarily apply to any dependencies of this repository.


```
Fix Git Logs documentation
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
```


------

- [:arrow_up: Top of ReadMe File][heading__title]

------



[badge__commits__fix_logs__master]:
  https://img.shields.io/github/last-commit/git-utilities/fix_logs/master.svg

[commits__fix_logs__master]:
  https://github.com/git-utilities/fix_logs/commits/master
  "&#x1F4DD; History of changes on this branch"


[fix_logs__community]:
  https://github.com/git-utilities/fix_logs/community
  "&#x1F331; Dedicated to functioning code"


[badge__issues__fix_logs]:
  https://img.shields.io/github/issues/git-utilities/fix_logs.svg

[issues__fix_logs]:
  https://github.com/git-utilities/fix_logs/issues
  "&#x2622; Search for and _bump_ existing issues or open new issues for project maintainer to address."


[badge__pull_requests__fix_logs]:
  https://img.shields.io/github/issues-pr/git-utilities/fix_logs.svg

[pull_requests__fix_logs]:
  https://github.com/git-utilities/fix_logs/pulls
  "&#x1F3D7; Pull Request friendly, though please check the Community guidelines"


[badge__master__fix_logs__source_code]:
  https://img.shields.io/github/repo-size/git-utilities/fix_logs

[fix_logs__master__source_code]:
  https://github.com/git-utilities/fix_logs
  "&#x2328; Project source code!"
