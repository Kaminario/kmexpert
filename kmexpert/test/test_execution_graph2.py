#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import unittest
import mock

from kmexpert.base.execution_graph import ExecutionGraph
from kmexpert.base.step_base import StepBase
from kmexpert.base.step_base_abs import RepeatStep


class MockStep(StepBase):
    def __init__(self, name=None, next_step=None):
        super(MockStep, self).__init__(mock.Mock())
        self.__next_step = next_step
        self.__name = name

    def evaluate(self):
        self._next_step = self.__next_step


class TestExecCtx(unittest.TestCase):

    def validate_run(self, graph, stack):
        self.assertEqual(len(graph._execution_stack), len(stack))
        for val, ref in zip(graph._execution_stack, stack):
            self.assertEqual(val.step, ref[0])

    def test_run_1(self):
        graph = ExecutionGraph()
        step3 = MockStep('step3')
        step2 = MockStep('step2', step3)
        step1 = MockStep('step1', step2)

        graph.run(from_step=step1, execution_context=mock.Mock())
        self.validate_run(graph=graph, stack=[[step1, ],
                                              [step2, ],
                                              [step3, ], ])

    def repeat(self):
        raise RepeatStep()

    def test_repeat(self):
        graph = ExecutionGraph()
        step3 = MockStep('step3')
        step2 = MockStep('step2', step3)
        step1 = MockStep('step1', step2)

        graph.run(from_step=step1, execution_context=mock.Mock())
        self.validate_run(graph=graph, stack=[[step1, ],
                                              [step2, ],
                                              [step3, ], ])


if __name__ == '__main__':
    unittest.main()
