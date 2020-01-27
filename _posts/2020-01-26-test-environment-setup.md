---
title: Test Environment Setup
layout: post
date:   2020-01-26 12:27:26 -0800
categories: git tests
---



This is a quick guide on testing scripts of this project without pushing results to GitHub.


------

- [Requirements][heading__requirements]

- [Add Git Shell Restricted User][heading__add_git_shell_restricted_user]

- [Append to SSH config][heading__append_to_ssh_config]

- [Setup Repositories for Testing][heading__setup_repositories_for_testing]

- [Test Fix Logs script][heading__test_fix_logs_script]

- [Attribution][heading__attribution]

- [License][heading__license]


------


## Requirements
[heading__requirements]: #requirements ""


This guide makes use of;


- [`git-init`](https://github.com/git-utilities/git-shell-commands/blob/master/git-init) script provided by [`git-utilities/git-shell-commands`](https://github.com/git-utilities/git-shell-commands) repository

- [`jekyll_usermod.sh`](https://github.com/S0AndS0/Jekyll_Admin/blob/master/jekyll_usermod.sh) script from [`S0AndS0/Jekyll_Admin`](https://github.com/S0AndS0/Jekyll_Admin) repository. Documentation specific to [`jekyll_usermod.sh`](https://s0ands0.github.io/Jekyll_Admin/administration/jekyll-usermod/)


Copying and Pasting commands without forethought is discouraged, please review linked to resources, manuals, help output, etc. prior to running anything questionable.


___


## Append to SSH config
[heading__append_to_ssh_config]: #append-to-ssh-config ""


Add `tests` host to SSH configurations...


```Bash
tee -a .ssh/config 1>/dev/null <<EOF
Host tests
   HostName localhost
   User gitname
   IdentitiesOnly yes
   IdentityFile ~/.ssh/private_key
EOF
```


___


## Add Git Shell Restricted User
[heading__add_git_shell_restricted_user]: #add-git-shell-restricted-user ""


```Bash
ssh pi sudo jekyll_usermod.sh\
 --user="gitname"\
 --group="devs"\
 --git-shell-copy-or-link="copy"\
 --ssh-pub-key="'$(<~/.ssh/pub.key)'"\
 --help
```


___


## Setup Repositories for Testing
[heading__setup_repositories_for_testing]: #setup-repositories-for-testing ""


1. Clone `llSourcell` and push to `tests` remote...


```Bash
mkdir -p ~/git/hub/llSourcell
cd ~/git/hub/llSourcell

git clone --origin=llSourcell git@github.com:llSourcell/Bitcoin_Trading_Bot.git

cd Bitcoin_Trading_Bot/

ssh tests git-init Bitcoin_Trading_Bot

git remote add origin tests:git/Bitcoin_Trading_Bot

git push origin master
```


2. Clone `How-to-Predict-Stock-Prices-Easily-Demo` and push to `tests` remote...


```Bash
cd ~/git/hub/llSourcell

git clone --origin=llSourcell git@github.com:llSourcell/How-to-Predict-Stock-Prices-Easily-Demo.git

cd How-to-Predict-Stock-Prices-Easily-Demo/

ssh tests git-init How-to-Predict-Stock-Prices

git remote add origin tests:git/How-to-Predict-Stock-Prices

git push origin master
```


3. Clone `How_to_simulate_a_self_driving_car` and push to `tests` remote...


```Bash
cd ~/git/hub/llSourcell

git clone --origin=llSourcell git@github.com:llSourcell/How_to_simulate_a_self_driving_car.git

cd How_to_simulate_a_self_driving_car/

ssh tests git-init simulate_a_self_driving_car

git remote add origin tests:git/simulate_a_self_driving_car

git push origin master
```


___


## Test Fix Logs script
[heading__test_fix_logs_script]: #test-fix-logs-script ""


```Bash
cd ~/git/hub/git-utilities/fix_logs

./fix_logs.py --help
```


___


## Attribution
[heading__attribution]: #attribution ""


- [Git Docs -- git-shell](https://git-scm.com/docs/git-shell)

- [Docs -- `S0AndS0/Jekyll_Admin`](https://s0ands0.github.io/Jekyll_Admin/)

- [Source -- `S0AndS0/Jekyll_Admin`](https://github.com/S0AndS0/Jekyll_Admin/)


___


## License
[heading__license]: #license "&#x2696; Legal bits of Open Source software"


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
