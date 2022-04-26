#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from collections import OrderedDict
from lib import FileUtil


class ConfigLoader:
    def __init__(self):
        self.config_path = FileUtil.get_path('config.json')
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(self.config_path)
        self.config_dict = FileUtil.get_json_content_from_path(self.config_path)
        self.default_server: OrderedDict = None

    def get_ip(self):
        return self.config_dict.get('ip', '0.0.0.0')

    def get_port(self):
        return self.config_dict.get('port', '28081')

    def get_servers(self) -> OrderedDict:
        return self.config_dict.get('servers', {})

    def get_server(self, name: str) -> OrderedDict:
        return self.get_servers().get(name, {})

    def get_ip_whitelist(self):
        return self.config_dict.get('ip_whitelist', ['localhost', '127.0.0.1', '192.168.0.96'])

