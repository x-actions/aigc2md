# Copyright 2022 xiexianbin.cn
# All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

"""python utils."""
import time
from datetime import datetime

import collections
try:
    from collections import abc
    collections.Counter = abc.Counter  # noqa
except Exception as _:  # noqa
    pass
from typing import List

from prettytable import PrettyTable

from aigc2md import exception


def arg(*args, **kwargs):
    """Decorator for CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


def add_arg(func, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(func, 'arguments'):
        func.arguments = []

    if (args, kwargs) not in func.arguments:
        func.arguments.insert(0, (args, kwargs))


def do_action_on_many(action, resources, success_msg, error_msg):
    """Helper to run an action on many resources."""
    failure_flag = False

    for resource in resources:
        try:
            action(resource)
            print(success_msg % resource)
        except Exception as e:
            failure_flag = True
            print(str(e))

    if failure_flag:
        raise exception.CommandError(error_msg)


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def timestamp() -> int:
    return int(time.time() * 1000)


def sort_dict(d):
    """ sort dict to Z-A

    :param d: {'hello': 1, 'python': 5, 'world': 3}
    :return [('python', 5), ('world', 3), ('hello', 1)]
    """
    return collections.Counter(d).most_common()


def date2timestamp(date_time) -> int:
    """ convert date to millisecond timestamp

    :param date_time: 2020-06-28T11:46:53.539425Z / 2022-10-27T10:54:56Z
    :return timestamp: 1593316013539
    """
    try:
        dt_utc = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        return int(dt_utc.timestamp() * 1000)
    except ValueError:
        dt_utc = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
        return int(dt_utc.timestamp() * 1000)


def pretty_output(field_names: List[str], rows: List[List[any]]):
    pt = PrettyTable()
    pt.field_names = field_names  # table header
    for row in rows:  # table body
        pt.add_row(row)
    print(pt)


def timestamp_to_dateformat(ts: int, format: str = '%Y-%m-%d %H:%M:%S') -> str:
    return time.strftime(format, time.localtime(ts))
