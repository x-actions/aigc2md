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

""" open-webui API for https://ai.80.xyz/api/v1/docs """

import os

from pyopenwebui import Pyopenwebui, DefaultHttpxClient


class OpenWebUI:

    def __init__(self, base_url: str, token: str) -> None:
        self.client = Pyopenwebui(
          # Or use the `PYOPENWEBUI_BASE_URL` env var
          base_url=base_url,
          bearer_token=token if token else os.environ.get("PYOPENWEBUI_API_KEY"),
          max_retries=3,
          default_headers={},
          http_client=DefaultHttpxClient(),
      )

    def chats_list(self, user_id: str, limit: int = 1, skip: int = 0):
        """Get Session User Chat List"""
        return self.client.api.v1.chats.list(user_id=user_id, limit=limit, skip=skip)

    def chats_get_by_id(self, id: str):
        """Get Chats By Id"""
        return self.client.api.v1.chats.get_by_id(id=id)

    def chats_tags_get_by_id(self, id: str):
        """Get Chats Tags By Id"""
        return self.client.api.v1.chats.tags.get_by_id(id=id)

    def chats_tags_add(self, chat_id: str, name: str):
        """Add Chat Tag By Id"""
        return self.client.api.v1.chats.tags.add(id=chat_id, name=name)

    def users_get(self, limit: int = 50, skip: int = 0):
        """Get Users"""
        return self.client.api.v1.users.get(limit=limit, skip=skip)
