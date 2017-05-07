#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
import sys

import django
import pytest


def run_tests(*test_args):
    if not test_args:
        test_args = ['-s', 'tests']

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()

    failures = pytest.main(test_args)
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
