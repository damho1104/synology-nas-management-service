#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class SingleTone:
    __instance = None

    def initialize(self):
        return

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def delete(cls):
        if cls.__instance is None:
            return
        del cls.__instance
        cls.__instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        assert cls.__instance is None, 'Do not create an instance of this class multiple times.'
        cls.__instance = object.__new__(cls)
        return cls.__instance
