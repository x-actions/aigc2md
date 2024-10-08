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

"""test utils."""

import unittest

from aigc2md import client


class HTTPTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_http_get(self):
        headers = {
            'Content-Type': 'application/text'
        }
        result, resp = client.http_get(
            url='https://httpbin.org/get',
            headers=headers)
        print(result, resp.split('\n'))
