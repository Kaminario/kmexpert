#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import unittest

from kmexpert.base.input_handlers import HelpHandler
from kmexpert.base.tooling_for_test import redirect_stdout


class TestInputHandlers(unittest.TestCase):
    def test_help(self):
        help = HelpHandler(help_texts=[])
        with redirect_stdout():
            help.help()
            help.echo_help(level=0)
            help.echo_help(level=1)

    def test_help_2(self):
        help = HelpHandler(help_texts=['abc123', 'qwerty987'])

        with redirect_stdout() as captured_output:
            help.echo_help(level=0)
        self.assertTrue('abc123' in captured_output.getvalue())
        self.assertTrue('qwerty987' not in captured_output.getvalue())

        with redirect_stdout() as captured_output:
            help.echo_help(level=1)
        self.assertTrue('abc123' in captured_output.getvalue())
        self.assertTrue('qwerty987' in captured_output.getvalue())

        with redirect_stdout() as captured_output:
            help.echo_help(level=2)
        self.assertTrue('abc123' in captured_output.getvalue())
        self.assertTrue('qwerty987' in captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()
