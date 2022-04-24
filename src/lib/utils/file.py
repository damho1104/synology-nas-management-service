#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json

from collections import OrderedDict


class FileUtil:
    @staticmethod
    def get_path(*paths):
        if getattr(sys, 'frozen', False):
            root_dir = os.path.dirname(sys.executable)
        else:
            root_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..')

        return os.path.normpath(os.path.join(root_dir, *paths))

    @staticmethod
    def create_json_from_data(json_data, file_path, text_encoding='utf-8'):
        with open(file_path, 'w', encoding=text_encoding) as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        os.chmod(file_path, 0o777)

    @staticmethod
    def get_json_content_from_path(path, text_encoding='utf-8') -> OrderedDict:
        if os.path.exists(path):
            with open(path, 'r', encoding=text_encoding) as conf:
                json_content = json.load(conf, object_pairs_hook=OrderedDict)
                return json_content
        else:
            raise Exception("Can't find json file : ", path)
