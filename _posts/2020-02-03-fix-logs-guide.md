---
title: Fix Logs Guide
layout: post
date:   2020-02-03 12:27:26 -0800
categories: guide
---



This is a more in-depth guide than what is provided within the [Quick Start](https://github.com/git-utilities/fix_logs#quick-start) section of this project's ReadMe file. Commands within this guide do **not** require `sudo` or _administrative_ permissions, and this project is designed to run entirely within an unprivileged account.


------


- [Clone Project]

- [Change Current Working Directory]

- [Install PIP Dependencies]

- [Review and/or Edit Configuration File]

- [Fix Logs Help]

- [Run Fix Logs]

- [Example fixed.json]

- [Example failed.json]

- [Open an Issue]


------


## Clone Project
[Clone Project]: #clone-project


1. Make a directory path for `git-utilities` repositories

2. Change the shell session's current working directory

3. Clone the source code of this repository


```Bash
mkdir -vp ~/git/hub/git-utilities

cd ~/git/hub/git-utilities

https://github.com/git-utilities/fix_logs.git
```


___


## Change Current Working Directory
[Change Current Working Directory]: #change-current-working-directory


```Bash
cd ~/git/hub/git-utilities/fix_logs
```


```Bash
ls -1 *.py
```

Above lists available Python scripts within the current working directory, and bellow is example output...


```
fix_logs.py
merge_failed.py
```


___


## Install PIP Dependencies
[Install PIP Dependencies]: #install-pip-dependencies


- Option one


```Bash
pip install --user -r requirements.txt
```


- Option two


```Bash
pip3 install --user pipenv

pipenv install -r requirements.txt
```


___


## Review and/or Edit Configuration File
[Review and/or Edit Configuration File]: #review-andor-edit-configuration-file


- Reviewing text files may be done with `more` or `less` command-line utilities


```Bash
more config.json
```


- Editing text files from the command-line is possible with `nano`, `pico`, `vim`, etc...


```Bash
vim config.json
```


> Note, `:wq` may be used to write and quit `vim` from _command mode_, and `:q!` may be used to discard changes while quitting.
>
> Hint, search for `vim cheat sheet` to find various [Gists](https://gist.github.com/ummahusla/98b381e0355e43973085) and web sites that contain useful Vim tips.


**Example `config.json` file**


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


- `fixed` key defines a file path to log repositories that where successfully fixed

- `failed` key defines a file path to log repositories that generated errors or merge conflicts while attempting fixes


> Note, both `fixed` and `failed` files are **overwritten** during the `fix_logs.py` logging process


- `defaults` key defines a dictionary of configurations that each repository defined by `reops` will be merged with, individual configurations within `repos` may overwrite these

  - `origin_branch` Git branch name to merge source `source_branch` with
  - `origin_remote` Git remote name to push changes to
  - `source_branch` Git branch name to _inject_ into `origin_branch`
  - `source_remote` Git remote name to fetch log corrections from
  - `fix_branch` Git branch name for triaging possible merge conflicts
  - `fix_commit` Git commit message for successful automatic merges
  - `keep_fix_branch` If `true` skips deleting `fix_branch` after merge
  - `no_push` If `true` skips attempting to push to `origin_remote` after merge
  - `merge_strategy` Git merge strategy to use, check `git help merge | less -p "-X <option>"`


> Note, `merge_strategy` does **not** need to be defined unless special merge strategies are desired


- `repos` Lists dictionaries of repository data that needs fixed

  - `dir` Local directory path to repository
  - `source` Remote URL to fetch `source_branch` from `source_remote`


> Note, Any `defaults` may be modified per-repository...
>
> **Example `config.json` file**


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
    },
    {
      "dir": "~/git/hub/llSourcell/How-to-Predict-Stock-Prices-Easily-Demo",
      "source": "git@github.com:jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction.git",
      "fix_branch": "fix_logs",
      "fix_commit": "Fixes logs from original author",
      "keep_fix_branch": true,
      "no_push": true
    },
  ]
}
```


> ... which allows for repositories such as `How-to-Predict-Stock-Prices-Easily-Demo`, to `keep_fix_branch` as well as modify other `defaults`


___


## Fix Logs Help
[Fix Logs Help]: #fix-logs-help


- Option one, if dependencies were installed to an account or system wide


```Bash
./fix_logs.py --help
```


- Option two, if dependencies were installed to a virtual environment


```Bash
pipenv run python3 fix_logs.py --help
```


**Example Help Output**


```
usage: fix_logs.py [-h] [--about] [--config CONFIG]
                   [--merge_strategy MERGE_STRATEGY]
                   [--origin_branch ORIGIN_BRANCH]
                   [--origin_remote ORIGIN_REMOTE]
                   [--source_branch SOURCE_BRANCH]
                   [--source_remote SOURCE_REMOTE] [--fix_branch FIX_BRANCH]
                   [--fix_commit FIX_COMMIT] [--no_push] [--keep_fix_branch]
                   [--license] [--verbose]

Simple Python script that attempts to fix git logs/history en-mass

optional arguments:
  -h, --help            show this help message and exit
  --about               Prints info about this script and exits
  --config CONFIG       Path to config.json file
  --merge_strategy MERGE_STRATEGY
                        Git merge strategy to use, check `git help merge |
                        less -p "-X <option>"`
  --origin_branch ORIGIN_BRANCH
                        Git branch name to merge source `source_branch` with
  --origin_remote ORIGIN_REMOTE
                        Git remote name to push changes to
  --source_branch SOURCE_BRANCH
                        Git branch to _inject_ into `origin_branch`
  --source_remote SOURCE_REMOTE
                        Git remote name to fetch log corrections from
  --fix_branch FIX_BRANCH
                        Git branch name for triaging possible merge conflicts
  --fix_commit FIX_COMMIT
                        Git commit message for successful automatic merges
  --no_push             Skips attempting to push to `origin_remote` after
                        merge
  --keep_fix_branch     Skips deleting `fix_branch` after merge
  --license             Prints script license and exits
  --verbose             Prints command standard out if set
```


___


## Run Fix Logs
[Run Fix Logs]: #run-fix-logs


- Option one, if dependencies were installed to an account or system wide


```Bash
./fix_logs.py
```


- Option two, if dependencies were installed to a virtual environment


```Bash
pipenv run python3 fix_logs.py
```


___


## Example `fixed.json`
[Example fixed.json]: #example-fixedjson


```JSON
"fixed": [
  {
    "name": "Bitcoin_Trading_Bot",
    "dir": "~/git/hub/llSourcell/Bitcoin_Trading_Bot",
    "source": "git@github.com:jaungiers/Multidimensional-LSTM-BitCoin-Time-Series.git",
    "code": 0,
    "err": "",
    "out": "Finished fixing ~/git/hub/llSourcell/Bitcoin_Trading_Bot",
    "origin_branch": "master",
    "origin_remote": "origin",
    "source_branch": "master",
    "source_remote": "source",
    "fix_branch": "fix",
    "fix_commit": "Fixes logs",
    "keep_fix_branch": false,
    "no_push": false
  }
]
```


Double-checking those that are logged as _fixed_ is likely a good idea...


```Bash
cd ~/git/hub/llSourcell/Bitcoin_Trading_Bot

git log

ls -ahl ./
```


... for the most part _should_ have missing files and logs restored.


Use Git to remove any files that are not required within the current branch, eg...


```Bash
git rm some_file.ext

git commit -m ':fire: removes some_file.ext'

git push origin master
```


... because this allows contributors to restore files if/when needed in the future.


___


## Example `failed.json`
[Example failed.json]: #example-failedjson


```JSON
"failed": [
  {
    "name": "How-to-Predict-Stock-Prices-Easily-Demo",
    "dir": "~/git/hub/llSourcell/How-to-Predict-Stock-Prices-Easily-Demo",
    "source": "git@github.com:jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction.git",
    "message": "How-to-Predict-Stock-Prices-Easily-Demo cannot fetch `source_remote` or `source_branch`",
    "code": 1,
    "err": "Permission denied (publickey).\nfatal: The remote end hung up unexpectedly",
    "out": "",
    "origin_branch": "master",
    "origin_remote": "origin",
    "source_branch": "master",
    "source_remote": "source",
    "fix_branch": "fix_logs",
    "fix_commit": "Fixes logs from original author",
    "keep_fix_branch": true,
    "no_push": true
  }
]
```


Inspect the `err` and `message` values for why a repository was unable to be fixed automatically.


Common causes of failure;


- _`Permission denied (publickey)`_; check [GitHub help documentation](https://help.github.com/en/github/authenticating-to-github/error-permission-denied-publickey) for suggestions.

- Network timeout; may be because of rate-limiting, try again after an hour or two.


> Note, aborting previous merge attempts may be necessary...


```Bash
cd ~/git/hub/llSourcell/How-to-Predict-Stock-Prices-Easily-Demo

git merge --abort

git checkout master

git branch -D fix
```


> ... to prevent the `fix_logs.py` script from generating new errors.


- Merge conflicts; often _`git mergetool`_ is the easiest course of action...


```Bash
cd ~/git/hub/llSourcell/How-to-Predict-Stock-Prices-Easily-Demo

git mergetool

git commit -m 'Resolves conflicts merging `source` into `master`'

git checkout master

git merge fix_logs

git push origin master
```


... In the future the `merge_failed.py` script may be of use to hasten the above process.


___


## Open an Issue
[Open an Issue]: #open-an-issue


To expedite assistance when opening a new [Issue](https://github.com/git-utilities/fix_logs/issues) please include any relevant logs along with links to public repositories...


```
    Repositories cannot be automatically fixed;


    - `origin` [Some-Repo](https://github.com/_account_/_Some-Repo_) <- `source` [Some-Repo](https://github.com/_author_/_repo_)

    - `origin` [anotherRepo](https://github.com/_account_/_anotherRepo_) <- `source` [Some-Repo](https://github.com/_author_/_repo_)


    **`failed.json`**


    ```JSON
    "failed": [
      ...
    ]
    ```
```
