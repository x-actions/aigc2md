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

import os
import sys
import time
from typing import List

from jinja2 import Template
import pydantic

from aigc2md.api import openwebui
from aigc2md import config
from aigc2md import utils


post_archetype = """---
title: "{{ post.title }}"
author:
date: "{{ post.date }}"
deprecated:
  enable: false
  reference: []
draft: false
layout: single
mathjax: false
comment: true
keywords: {{ post.keywords }}
description:
aliases: []
categories:
{%- for i in post.categories %}
  - {{ i }}
{%- endfor %}
tags:
{%- for i in post.tags %}
  - {{ i }}
{%- endfor %}
original: true
reference: []
---

> {{ post.content }}

"""


class Post(pydantic.BaseModel):
    title: str
    author: str = ''
    date: str
    keywords: List[str] = []
    categories: List[str] = []
    tags: List[str] = []
    content: str


class Render:

    def __init__(self, force: bool = False):
        self.author_list = {
            'bge': 'b',
            'gemma': 'g',
            'hunyuan': 't',
            'llama3': 'l3',
            'qwen': 'a',
            'SparkDesk': 's',
        }
        self.rendered_tag = 'posted'
        self.client = openwebui.OpenWebUI(
            base_url=config.OPENWEBUI_BASE_URL, token=config.OPENWEBUI_JWT)

        self.force = force

    def _parse_tags(self, chat_id: str, tags: List[dict]) -> List[str]:
        result = []
        _tags = self.client.chats_tags_list(id=chat_id)
        for _tag in _tags:
            result.append(_tag.name)

        for tag in tags:
            if tag:
              result.append(tag.get('name', ''))
        return list(set(result))

    def _parse_author(self, model_name: str):
        for author in self.author_list:
            if author in model_name:
                return self.author_list[author]
        return ''

    def _parse_to_posts(self, messages: List[any]) -> List[Post]:
        result = []
        title: str
        category: str
        for message in messages:
            if message.get('role', '') == 'user':
                title = message.get('content')
                category = self._parse_category(title)
            elif message.get('role', '') == 'assistant':
                post = Post(
                    title=title,
                    author=self._parse_author(message.get('modelName')),
                    date=utils.timestamp_to_dateformat(
                        int(message.get('timestamp')),
                        format='%Y-%m-%d %H:%M:%S+0800',
                    ),
                    keywords=[],
                    categories=[category],
                    tags=[category],
                    content=message.get('content'),
                )
                result.append(post)
        return result

    def _parse_category(self, s: str) -> str:
        for category in config.DEFAULT_CATEGORIES_LIST:
            if category in s:
                return category
        return 'posts'

    def _parse_name(self, s: str) -> str:
        _name = utils.clean_emoji(s)
        if len(_name) > 32:
            _name = _name[:32]
        return _name.replace(' ', '').strip()

    def one(self, chat_id: str, output: str):
        """Render Chat by id

        Args:
            chat_id (str): chat id
        """
        # output directory
        if os.path.exists(output) is False:
            print(f'output directory not exists. auto create ...')
            os.makedirs(output)

        if os.path.isdir(output) is False:
            print(f'{output} is file, expect is dir')
            sys.exit(1)

        # Get Chat By Id
        chat = self.client.chats_retrieve(id=chat_id)

        rendered_flag = self.rendered_tag in self._parse_tags(chat_id, chat.chat.get('tags', []))
        if rendered_flag and self.force is False:
            print(f'chat: {chat.title}({chat_id}) already render with flag({self.rendered_tag}), please use `--force` flag to force render again')
            sys.exit(1)

        posts = self._parse_to_posts(chat.chat.get('messages', {}))
        for post in posts:
            # output dir
            post_dir = os.path.join(output, post.categories[0], self._parse_name(chat.title))
            if os.path.exists(post_dir) is False:
                os.makedirs(post_dir)

            file_path = os.path.join(post_dir, f'{self._parse_name(post.title).replace(" ", "").replace("/", "-")}.md')
            if os.path.exists(file_path) and self.force is False:
                file_path = file_path.replace(
                    '.md',
                    f'-{time.strftime("%Y%m%d-%H%M%S-%s", time.localtime(time.time()))}.md')

            with open(file_path, 'w', encoding='utf8') as out_file:
                tmle = Template(post_archetype)
                out_file.write(tmle.render({'post': post}))
                print(f'{post.title} render to {file_path} ...')

        # add flag
        if rendered_flag is False:
            resp = self.client.chats_tags_create(chat_id=chat_id, tag_name=self.rendered_tag)
            utils.pretty_output(
                field_names=[],
                rows=[
                    ['ID', resp.id],
                    ['chat_id', resp.chat_id],
                    ['tag_name', resp.tag_name],
                    ['timestamp', utils.timestamp_to_dateformat(resp.timestamp)],
                    ['user_id', resp.user_id],
                ],
            )
