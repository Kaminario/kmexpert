#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import unittest
import click

from kmexpert.base.input_converters import YES, NO, HELP
from kmexpert.base.prompt_validators import InputValidator
from kmexpert.base.tooling_for_test import redirect_stdout, put_in_stdin


class TestPromptValidators(unittest.TestCase):
    def test_yes(self):
        put_in_stdin('y')
        with redirect_stdout() as output:
            res = click.prompt("", type=InputValidator(converters=[YES, NO, HELP]))
        self.assertTrue(res.kind_of(YES))

    def test_no(self):
        put_in_stdin('n')
        with redirect_stdout() as output:
            res = click.prompt("", type=InputValidator(converters=[YES, NO, HELP]))
        self.assertTrue(res.kind_of(NO))

    def test_not_match(self):
        """First input not match any converter, second does"""
        put_in_stdin('x\ny')
        with redirect_stdout() as output:
            res = click.prompt("", type=InputValidator(converters=[YES, NO]))
        self.assertTrue(res.kind_of(YES))
        self.assertTrue("Error: x. Help: y - yes; n - no" in output.getvalue())


if __name__ == '__main__':
    unittest.main()
