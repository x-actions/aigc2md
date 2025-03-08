# aigc2md

[![PyPI-aigc2md](https://img.shields.io/pypi/v/aigc2md.svg?maxAge=3600)](https://pypi.org/project/aigc2md/)

convert AIGC to hugo markdown, current only support OpenWebUI API
将 AIGC 生产的内容转化为 hugo markdown 格式，当前仅支持调用 OpenWebUI API

## How to Use by Github Actions

```
    - name: convert AIGC to hugo markdown
      uses: x-actions/aigc2md@v1
      env:
        PYOPENWEBUI_BEARER_TOKEN: "<JWT>"
        LOG_LEVEL: "DEBUG"
```

## use as cli

```
$ pip install aigc2md

$ aigc2md --help
usage: aigc2md [--version] [--debug] <subcommand> ...

Command-line interface for convert AIGC to hugo markdown.

Positional arguments:
  <subcommand>
    chats          chats actions.
    render         render actions.
    users          list users.
    bash-completion
                   Prints all of the commands and options to stdout so that the aigc2md.bash_completion script
                   doesn't have to hard code them.
    help           Display help about this program or one of its subcommands.

Options:
  --version        show program's version number and exit
  --debug          Print debugging output.

See "aigc2md help COMMAND" for help on a specific command.

$ aigc2md users
+--------------------------------------+--------+---------------------+---------+------------------------------------------------+------------+----------------+
|                  ID                  |  name  |        email        |   role  |                     system                     | created_at | last_active_at |
+--------------------------------------+--------+---------------------+---------+------------------------------------------------+------------+----------------+
| a856afee-389e-4fc2-9431-dbac432912a1 | 谢先斌 |   me@xiexianbin.cn  |  admin  | 使用中文回答，除代码和专用名词外尽量不使用英文 | 2024-08-11 09:35:00 |   2024-08-11 09:35:00   |
+--------------------------------------+--------+---------------------+---------+------------------------------------------------+------------+----------------+

$ aigc2md chats
+--------------------------------------+---------------------------------+---------------------+---------------------+
|                  ID                  |              title              |      updated_at     |      created_at     |
+--------------------------------------+---------------------------------+---------------------+---------------------+
| ef0bdafc-045c-41eb-aba5-c841e31c2fd8 |          😊 简单问候语          | 2024-09-16 17:20:27 | 2024-09-16 17:20:19 |
+--------------------------------------+---------------------------------+---------------------+---------------------+

$ aigc2md render --id cab178a2-ba80-4008-a72d-1eb41c21e6c4
Lama3.1介绍一下 render to /Users/xiexianbin/workspace/code/github.com/x-actions/aigc2md-python/output/Lama3.1介绍一下.md ...
```

## Dev and Test

- local run

```
# create venv
python3 -m venv .venv
source .venv/bin/activate

# install
pip3 install -r requirements.txt

# set env
export PYOPENWEBUI_BEARER_TOKEN="<JWT>"

# dev
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 aigc2md/shell.py --help
python3 aigc2md/shell.py help xxx
```

- tests

```
python3 -m unittest aigc2md.tests.unit.test_http.HTTPTestCase.test_http_get
```
