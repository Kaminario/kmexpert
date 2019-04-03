#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import unittest
import mock
import sys
import StringIO

from kmexpert.base.execution_graph import ExecutionGraph
from kmexpert.base.step_base_abs import RepeatStep, StepBack


class TestExecCtx(unittest.TestCase):
    def setUp(self):
        captured_output = StringIO.StringIO()
        self.stdout = sys.stdout
        sys.stdout = captured_output

    def tearDown(self):
        sys.stdout = self.stdout

    def step(self, side_effects, next_step=None):
        step = mock.Mock()
        step.run.side_effect = side_effects
        step.next_step.return_value = next_step
        return step

    def context(self):
        class Context(object):
            def __init__(self, index=0):
                self.index = index

            def copy(self):
                return Context(index=self.index + 1)

        return Context()

    def validate_run(self, graph, final_context_index, stack):
        self.assertEqual(graph.context.index, final_context_index)
        for val, ref in zip(graph._execution_stack, stack):
            self.assertEqual(val.step, ref[0])
            self.assertEqual(val.context.index, ref[1])

    def test_run(self):
        graph = ExecutionGraph()
        step1 = self.step(side_effects=[None])

        graph.run(from_step=step1, execution_context=self.context())
        self.assertEqual(step1.run.call_count, 1)
        self.validate_run(graph=graph, final_context_index=0, stack=[[step1, 1]])

    def test_run_step_repeat(self):
        graph = ExecutionGraph()
        step1 = self.step(side_effects=[RepeatStep, None])

        graph.run(from_step=step1, execution_context=self.context())
        self.assertEqual(step1.run.call_count, 2)
        self.validate_run(graph=graph, final_context_index=2, stack=[[step1, 1]])

    def test_run_step_back(self):
        graph = ExecutionGraph()
        step1 = self.step(side_effects=[StepBack, None])

        graph.run(from_step=step1, execution_context=self.context())
        self.assertEqual(step1.run.call_count, 2)
        self.validate_run(graph=graph, final_context_index=2, stack=[[step1, 1]])

    def test_run_step_back_repeat(self):
        graph = ExecutionGraph()
        step1 = self.step(side_effects=[StepBack, RepeatStep, None])

        graph.run(from_step=step1, execution_context=self.context())
        self.assertEqual(step1.run.call_count, 3)
        self.validate_run(graph=graph, final_context_index=2, stack=[[step1, 1]])

    def test_run_next_next(self):
        graph = ExecutionGraph()
        step2 = self.step(side_effects=[None])
        step1 = self.step(side_effects=[None], next_step=step2)

        graph.run(from_step=step1, execution_context=self.context())
        self.assertEqual(step1.run.call_count, 1)
        self.assertEqual(step2.run.call_count, 1)
        self.validate_run(graph=graph, final_context_index=0, stack=[[step1, 1],
                                                                     [step2, 1]])

    def test_run_next_repeat(self):
        graph = ExecutionGraph()
        step2 = self.step(side_effects=[RepeatStep, None])
        step1 = self.step(side_effects=[None], next_step=step2)

        graph.run(from_step=step1, execution_context=self.context())
        self.assertEqual(step1.run.call_count, 1)
        self.assertEqual(step2.run.call_count, 2)
        self.validate_run(graph=graph, final_context_index=2, stack=[[step1, 1],
                                                                     [step2, 1]])

    def test_run_next_back(self):
        graph = ExecutionGraph()
        step3 = self.step(side_effects=[None])
        step2 = self.step(side_effects=[StepBack, RepeatStep, None], next_step=step3)
        step1 = self.step(side_effects=[None, None], next_step=step2)

        graph.run(from_step=step1, execution_context=self.context())
        self.assertEqual(step1.run.call_count, 2)
        self.assertEqual(step2.run.call_count, 3)
        self.assertEqual(step3.run.call_count, 1)
        self.validate_run(graph=graph, final_context_index=4, stack=[[step1, 1],
                                                                     [step2, 3],
                                                                     [step3, 5]])

    def test_run_back_back_back(self):
        graph = ExecutionGraph()
        step3 = self.step(side_effects=[StepBack, None])
        step2 = self.step(side_effects=[None, StepBack, None], next_step=step3)
        step1 = self.step(side_effects=[None, StepBack, None], next_step=step2)

        graph.run(from_step=step1, execution_context=self.context())
        self.assertEqual(step1.run.call_count, 3, msg="step1 calls check failed")
        self.assertEqual(step2.run.call_count, 3, msg="step2 calls check failed")
        self.assertEqual(step3.run.call_count, 2, msg="step3 calls check failed")
        self.validate_run(graph=graph, final_context_index=2, stack=[[step1, 1],
                                                                     [step2, 3],
                                                                     [step3, 3]])




if __name__ == '__main__':
    unittest.main()
