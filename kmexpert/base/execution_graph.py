#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import click

from kmexpert.base.step_base_abs import StepBaseAbs, RepeatStep, StepBack, StopRun
from kmexpert.base.execution_context import ExecCtx


class StepBackwardFail(RuntimeError):
    def __init__(self, *args, **kwards):
        super(StepBackwardFail, self).__init__("Unable to step back", *args, **kwards)


class ExecutionGraph(object):
    class ExecutionStackEntry(object):
        def __init__(self, step, context):
            self.step = step
            self.context = context

    def __init__(self):
        self._execution_stack = list()
        self._execution_context = None

    @property
    def context(self):
        return self._execution_context

    def current(self):
        return self._execution_stack[-1]

    def append(self, step, context):
        self._execution_stack.append(ExecutionGraph.ExecutionStackEntry(step, context.copy()))

    def restore_context(self):
        self._execution_context = self.current().context.copy()

    def run(self, from_step, execution_context):
        # type: (StepBaseAbs, ExecCtx) -> None
        self.append(from_step, execution_context)
        self._execution_context = execution_context
        while self._execution_stack:
            try:
                self.current().step.run(self.context)
                self.step_next()
            except StopRun:
                self.stop_iteration()
                break
            except RepeatStep:
                self.step_repeat()
            except StepBack:
                self.step_back()

    def step_next(self):
        next_step = self.current().step.next_step()
        if not next_step:
            raise StopRun()
        self.append(next_step, self.context)

    def step_back(self):
        if not (len(self._execution_stack) > 1):
            click.echo("Unable to step back")
            self.step_repeat()
        else:
            self._execution_stack.pop()
            self.restore_context()

    def step_repeat(self):
        self.restore_context()

    def stop_iteration(self):
        pass

    def history(self):
        res = click.style("History", bold=True)
        for entry in self._execution_stack:
            for text in entry.step.history():
                res += "\n" + text
        return res

    def steps(self):
        pass

