---
title: Git Merge Conflict
layout: post
date:   2020-01-27 12:27:26 -0800
categories: git tips
---


Throughout this short guide it is a good idea to use the `git log` command to check what branch of commit history is currently being operated upon


------


- [Generating a Merge Conflict]

- [Setup New Repository]

- [Attribution]


------


## Setup New Repository
[Setup New Repository]: #setup-new-repository

Initialize a new `examples` repository and change current working directory to it...


```Bash
git init examples

cd ./examples
```


Checkout a new `test_master` branch, add a ReadMe file, and commit changes...


```Bash
git checkout -b test_master


tee -a README.md 1>/dev/null <<EOF
## Examples
[heading__title]:
  #examples
  "&#x2B06; Top of ReadMe File"


------


- [:card_index: Attribution][heading__attribution]


------


## Attribution
[heading__attribution]:
  #attribution
  "&#x1F4C7; Resources that where helpful in building this project so far."


------

- [:arrow_up: Top of ReadMe File][heading__title]

------
EOF


git add README.md
git commit -m ':tada: Initial commit, adds ReadMe file'
```


Checkout the `master` branch, and merge `test_master` branch changes in...


```Bash
git checkout master || git checkout -b master

git merge test_master
```


Tag current state with a version number and description...


```Bash
git tag --annotate v0.0.1 -m ':tag: Initial Release for Commit'

git tag --list
```


___


## Generating a Merge Conflict
[Generating a Merge Conflict]: #generating-a-merge-conflict


```Bash
tee ./example.sh 1>/dev/null <<'EOF'
#!/bin/bash
_name="$1"

if [ ${#_name} == 0 ]; then
  _name='world'
fi

echo "Hello ${_name}!"
EOF


bash example.sh
bash example.sh 'lifeforms'


git add example.sh
git commit -m ':shell: Adds script'
```


```Bash
git checkout test_master


tee ./example.sh 1>/dev/null <<'EOF'
#!/usr/bin/env bash

printf 'Hello %s!\n' "${1:-world}"
EOF


bash example.sh
bash example.sh 'undefined?'


git add example.sh
git commit -m ':shell: Adds script'
```


```Bash
git checkout master

git merge test_master
```


> Example output from `git merge test_master`


```
Auto-merging example.sh
CONFLICT (add/add): Merge conflict in example.sh
Automatic merge failed; fix conflicts and then commit the result.
```


> Example output from `git status`


```
On branch master
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)

	both added:      example.sh

no changes added to commit (use "git add" and/or "git commit -a")
```

> Example output from `cat example.sh`


```
<<<<<<< HEAD
#!/bin/bash
_name="$1"

if [ ${#_name} == 0 ]; then
  _name='world'
fi

echo "Hello ${_name}!"
=======
#!/usr/bin/env bash

printf 'Hello %s!\n' "${1:-world}"
>>>>>>> test_master
```

___


## Resolving a Merge Conflict
[Resolving a Merge Conflict]: #resolving-a-merge-conflict


- Option 1, _`git show _branch_:_path_`_ may be used to overwrite `example.sh` within the `master` branch with the continence from `test_master` branch...


```Bash
git show test_master:example.sh > example.sh
```


- Option 2, or Awk scripting may be used to selectively keep changes...


```Bash
awk 'BEGIN {
  _matched = 0
}
{
  if (_matched) {
    if ($0 !~ "test_master") {
      print $0
    } else {
      _matched = 0
    }
  } else if ($0 == "=======") {
    _matched = 1
  }
}' <<<"$(<example.sh)" > example.sh
```


- Option 3, `vimdiff` and other IDE tools may be used to select individual _hunks_ of changes to merge...


```Bash
git mergetool --tool-help

git config --local merge.tool vimdiff
git config --local merge.conflictstyle diff3

git mergetool
```


> See [Gist -- Git mergetool tutorial](https://gist.github.com/karenyyng/f19ff75c60f18b4b8149) for quick tips on how to utilize `vimdiff` as well as more examples of resolving merge conflicts.


- Option 4, check documentation [merge strategy](https://git-scm.com/docs/merge-strategies) for the `-Xours` strategy


```Bash
git merge --abort

git merge -Xours test_master

cat example.sh
```

> Example output from `cat example.sh`


```Bash
#!/bin/bash
_name="$1"

if [ ${#_name} == 0 ]; then
  _name='world'
fi

echo "Hello ${_name}!"
```


- Option 5, check documentation [merge strategy](https://git-scm.com/docs/merge-strategies) for the `-Xtheirs` strategy


```Bash
git merge --abort

git merge -Xtheirs test_master

cat example.sh
```


> Example output from `cat example.sh`


```Bash
#!/usr/bin/env bash

printf 'Hello %s!\n' "${1:-world}"
```


------


```Bash
git log --oneline
```


> Example output


```
571ea89 (HEAD -> master) :shell: Adds script
c363a46 (tag: v0.0.1) :tada: Initial commit, adds ReadMe file
```


```Bash
git log --oneline test_master
```


> Example output


```
d449ed3 (test_master) :shell: Adds script
c363a46 (tag: v0.0.1) :tada: Initial commit, adds ReadMe file
```


Add and commit changes to resolve merge conflict...


```Bash
git add example.sh

git commit -m 'Merges d449ed3 onto 571ea89'
```


------


Now it is possible to merge `master` onto `test_master` without conflicts...


```Bash
git checkout test_master

git merge master
```


> Example output


```
Updating d449ed3..327ba52
Fast-forward
```


___


## Attribution
[Attribution]: #attribution


- [Git documentation -- `git mergetool`](https://www.git-scm.com/docs/git-mergetool)

- [Git documentation --  `git merge -X_strategy_`](https://git-scm.com/docs/merge-strategies)

- [Gist -- Git mergetool tutorial](https://gist.github.com/karenyyng/f19ff75c60f18b4b8149)
