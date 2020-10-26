# SolvabilityInspector

[ISCCTF 2020](https://github.com/ISCCTF2020)の問題を死活監視するやつ

## 使い方

1. `.env`ファイルに必要事項を書き入れる
2. 下記コマンドを実行

```shell-session
$ python --version
Python 3.8.0

$ pip3 -r install requirements.txt
(snip)

$ python3 main.py >> succes.log 2>> error.log
```

