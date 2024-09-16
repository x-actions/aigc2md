# Copyright 2024 xiexianbin.cn
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

from aigc2md import utils
from aigc2md.v1.users import Users
from aigc2md.v1.chats import Chats


@utils.arg(
    '--limit', dest='limit', metavar='<integer>', type=int, default=50,
    help='page size.')
@utils.arg(
    '--skip', dest='skip', metavar='<integer>', type=int, default=0,
    help='skip.')
def do_users(args):
    """list users."""
    Users().show(limit=args.limit, skip=args.skip)


@utils.arg(
    '--page', dest='page', metavar='<integer>', type=int, default=1,
    help='page number.')
@utils.arg(
    '--skip', dest='skip', metavar='<integer>', type=int, default=0,
    help='skip.')
def do_chats(args):
    """chats actions."""
    Chats().list(page=args.page)
