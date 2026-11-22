#!/usr/bin/env python3
# -- coding: utf-8 --
"""Testing helpers that do not depend on the unmaintained nose package."""

# Imports
import functools
import os
import shutil
import unittest
from tempfile import mkdtemp, mkstemp

from cement.core import backend


def raises(expected_exception):
    """Assert that a test method raises the expected exception."""

    def decorator(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            with self.assertRaises(expected_exception):
                function(self, *args, **kwargs)

        return wrapper

    return decorator


class CementTestCase(unittest.TestCase):
    """Minimal replacement for Cement's nose-backed test base class."""

    def setUp(self):
        self.tmp_file_handle, self.tmp_file = mkstemp(prefix="droopescan.tests.")
        self.tmp_dir = mkdtemp(prefix="droopescan.tests.")

    def tearDown(self):
        if self.tmp_file_handle is not None:
            os.close(self.tmp_file_handle)
            self.tmp_file_handle = None
        if self.tmp_file and os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)
        if self.tmp_dir and os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    @staticmethod
    def reset_backend():
        for handler_name in backend.__handlers__.copy():
            del backend.__handlers__[handler_name]
        for hook_name in backend.__hooks__.copy():
            del backend.__hooks__[hook_name]


class _TestHelpers:
    CementTestCase = CementTestCase
    raises = staticmethod(raises)


test = _TestHelpers()
