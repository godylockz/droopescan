#!/usr/bin/env python3
# -- coding: utf-8 --
"""Shared output methods for interactive Droopescan controllers."""

from __future__ import print_function

# Imports
from cement.core import handler, controller
import dscan.common.functions as f
import sys

class HumanBasePlugin(controller.CementBaseController):
    def error(self, *args, **kwargs):
        f.error(*args, **kwargs)

    def msg(self, msg, end='\n'):
        print(msg, end=end)
