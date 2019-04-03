#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import unittest

from kmexpert.base.input_converters import YES, NO, HISTORY, HELP, INT, STR, \
    YesFlag, NoFlag, HistoryFlag, HelpFlag, IntConverter, StrConverter, PositiveIntConverter


class TestConverters(unittest.TestCase):
    def test_yes(self):
        self.assertTrue(YES.kind_of(YES))
        self.assertTrue(YES.kind_of(YesFlag()))
        self.assertFalse(YES.kind_of(NO))
        self.assertTrue(YES.convert('y').kind_of(YES))
        self.assertTrue(YES.convert('yes').kind_of(YES))
        self.assertEqual(YES.convert('x'), None)
        self.assertEqual(YES.help(), "y - yes")

    def test_no(self):
        self.assertTrue(NO.kind_of(NO))
        self.assertTrue(NO.kind_of(NoFlag()))
        self.assertFalse(NO.kind_of(YES))
        self.assertTrue(NO.convert('n').kind_of(NO))
        self.assertTrue(NO.convert('no').kind_of(NO))
        self.assertEqual(NO.convert('x'), None)
        self.assertEqual(NO.help(), "n - no")

    def test_history(self):
        self.assertTrue(HISTORY.kind_of(HISTORY))
        self.assertTrue(HISTORY.kind_of(HistoryFlag()))
        self.assertFalse(HISTORY.kind_of(YES))
        self.assertTrue(HISTORY.convert('hi').kind_of(HISTORY))
        self.assertTrue(HISTORY.convert('history').kind_of(HISTORY))
        self.assertEqual(HISTORY.convert('x'), None)
        self.assertEqual(HISTORY.help(), "hi - history")

    def test_help(self):
        self.assertTrue(HELP.kind_of(HELP))
        self.assertTrue(HELP.kind_of(HelpFlag()))
        self.assertFalse(HELP.kind_of(NO))
        self.assertTrue(HELP.convert('h').kind_of(HELP))
        self.assertTrue(HELP.convert('h1').kind_of(HELP))
        self.assertTrue(HELP.convert('h2').kind_of(HELP))
        self.assertEqual(HELP.convert('x'), None)
        self.assertEqual(HELP.convert('h').level(), 0)
        self.assertEqual(HELP.convert('h1').level(), 1)
        self.assertEqual(HELP.convert('h2').level(), 2)

    def test_int(self):
        self.assertTrue(INT.kind_of(INT))
        self.assertTrue(INT.kind_of(IntConverter()))
        self.assertFalse(INT.kind_of(STR))
        self.assertTrue(INT.convert('5').kind_of(INT))
        self.assertEqual(INT.convert('10').value(), 10)
        self.assertEqual(INT.convert('x'), None)

    def test_str(self):
        self.assertTrue(STR.kind_of(STR))
        self.assertTrue(STR.kind_of(StrConverter()))
        self.assertFalse(STR.kind_of(INT))
        self.assertTrue(STR.convert('5').kind_of(STR))
        self.assertEqual(STR.convert('10').value(), '10')

    def test_positive_int(self):
        self.assertTrue(PositiveIntConverter().kind_of(PositiveIntConverter()))
        self.assertFalse(PositiveIntConverter().kind_of(INT))
        self.assertTrue(PositiveIntConverter().convert('5').kind_of(PositiveIntConverter()))
        self.assertEqual(PositiveIntConverter().convert('10').value(), 10)
        self.assertEqual(PositiveIntConverter().convert('x'), None)
        self.assertEqual(PositiveIntConverter().convert('-1'), None)
        self.assertEqual(PositiveIntConverter().convert('0'), None)


if __name__ == '__main__':
    unittest.main()
