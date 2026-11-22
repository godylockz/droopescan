#!/usr/bin/env python3
# -- coding: utf-8 --
"""Internal test command."""

# Imports
from cement.core import handler, controller
from dscan.plugins import HumanBasePlugin
from subprocess import call
import os, sys, dscan

BASE_FOLDER = '/var/www/drupal/'
UPDATE_MAJOR = ['6', '7']

def recursive_grep(directory, needle):
    return_file = None
    for f in os.listdir(directory):
        if f.endswith('.py'):
            with open(directory + f, 'r') as fh:
                for line in fh:
                    if needle in line:
                        return_file = f

            if return_file:
                break

    return return_file

class Tests(HumanBasePlugin):
    class Meta:
        label = 'test'
        stacked_on = 'base'
        stacked_type = 'nested'
        hide = True
        arguments = [
            (['-s', '--single-test'], dict(action='store', help='Name of test to run',
                required=False, default=None)),
            (['-c', '--with-coverage'], dict(action='store_true', help='Do test coverage',
                required=False, default=False)),
        ]

    @controller.expose(help='', hide=True)
    def default(self):
        env = {}
        single_test = self.app.pargs.single_test
        with_coverage = self.app.pargs.with_coverage
        if single_test and with_coverage:
            self.error('Cannot run with both -c and -s.')

        if not single_test:
            call_base = [sys.executable]
            if with_coverage:
                call_base += ['-m', 'coverage', 'run', '--source=dscan']
            call_base += [
                '-m', 'unittest', 'discover', '-s', 'dscan/tests',
                '-p', '*_tests.py'
            ]
            exit = call(call_base, env=env)

        else:
            test_file = recursive_grep(dscan.PWD + 'tests/', single_test + "(")
            if not test_file:
                self.error('No test found with name "%s"' % single_test)

            appendix = 'tests.py'
            tna = test_file[0:-1 * len(appendix) - 1].split('_')
            underscore = '_'.join(tna)
            upper = "".join(w.capitalize() for w in tna)

            test = 'dscan.tests.%s_tests.%sTests.%s' % (underscore, upper, single_test)
            exit = call([sys.executable, '-m', 'unittest', test], env=env)

        sys.exit(exit)

def load(app=None):
    handler.register(Tests)

