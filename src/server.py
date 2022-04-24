#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import lib
import multiprocessing


def main():
    lib.run()
    return True


if __name__ == '__main__':
    multiprocessing.freeze_support()
    if not main():
        sys.exit(1)
    sys.exit(0)
