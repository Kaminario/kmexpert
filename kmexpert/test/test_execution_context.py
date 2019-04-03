#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import unittest

from kmexpert.base.execution_context import ExecCtx


class TestExecCtx(unittest.TestCase):
    def test_set_get(self):
        ctx = ExecCtx()

        ctx.set('x1', '123')
        self.assertEqual(ctx.get('x1'), '123')

        ctx.set('x1', '321')
        self.assertEqual(ctx.get('x1'), '321')

        ctx.set('x2', 5)
        self.assertEqual(ctx.get('x2'), 5)

    def test_as_dict(self):
        ctx = ExecCtx()

        ctx.set('x1', '123')
        ctx.set('x2', 5)
        dict_ = ctx.as_dict()
        self.assertTrue(isinstance(dict_, dict))
        self.assertEqual(dict_['x1'], '123')
        self.assertEqual(dict_['x2'], 5)
        ctx2 = ExecCtx.from_dict(dict_)
        self.assertTrue(isinstance(ctx2, ExecCtx))
        self.assertEqual(ctx2.get('x1'), '123')
        self.assertEqual(ctx2.get('x2'), 5)

    def test_copy(self):
        ctx = ExecCtx()
        ctx.set('x1', '123')
        ctx.set('x2', 5)

        ctx2 = ctx.copy()
        self.assertEqual(ctx.as_dict(), ctx2.as_dict())


if __name__ == '__main__':
    unittest.main()
