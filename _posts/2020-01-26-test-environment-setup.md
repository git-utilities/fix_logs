---
title: Test Environment Setup
layout: post
date:   2020-01-26 12:27:26 -0800
categories: git tests
---



This is a quick guide on testing scripts of this project without pushing results to GitHub.

___


Add `git-tests` host to SSH configurations...


```Bash
tee -a .ssh/config 1>/dev/null <<EOF
Host git-tests
   HostName localhost
   User S0AndS0
   IdentitiesOnly yes
   IdentityFile ~/.ssh/private_key
EOF
```

------


Clone `llSourcell` and push to `git-tests` remote...


```Bash
mkdir -p ~/git/hub/llSourcell
cd ~/git/hub/llSourcell

git clone --origin=llSourcell git@github.com:llSourcell/Bitcoin_Trading_Bot.git

cd Bitcoin_Trading_Bot/

ssh git-tests git-init Bitcoin_Trading_Bot

git remote add origin git-tests:git/Bitcoin_Trading_Bot

git push origin master

```

------


Clone `How-to-Predict-Stock-Prices-Easily-Demo` and push to `git-tests` remote...


```Bash
cd ~/git/hub/llSourcell

git clone --origin=llSourcell git@github.com:llSourcell/How-to-Predict-Stock-Prices-Easily-Demo.git

cd How-to-Predict-Stock-Prices-Easily-Demo/

ssh git-tests git-init How-to-Predict-Stock-Prices

git remote add origin git-tests:git/How-to-Predict-Stock-Prices

git push origin master
```

------


Clone `How_to_simulate_a_self_driving_car` and push to `git-tests` remote...


```Bash
cd ~/git/hub/llSourcell

git clone --origin=llSourcell git@github.com:llSourcell/How_to_simulate_a_self_driving_car.git

cd How_to_simulate_a_self_driving_car/

ssh git-tests git-init simulate_a_self_driving_car

git remote add origin git-tests:git/simulate_a_self_driving_car

git push origin master
```


------


## Test `fix_log.py` script


```Bash
cd ~/git/hub/git-utilities/fix_logs

./fix_logs.py --help
```
