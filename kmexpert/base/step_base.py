#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import traceback
import click
import copy


from kmexpert.base.execution_context import ExecCtx
from kmexpert.base.tooling import class_to_name
from kmexpert.base.input_handlers import HistoryHandler, StepsHandler, HelpHandler, InputHandler, StepBackHandler
from kmexpert.base.step_base_abs import StepBaseAbs, RepeatStep, StepBack, StopRun


class StepBase(StepBaseAbs):

    def __init__(self, procedure):
        # type: (StepBasedProcedure) -> StepBase
        self._procedure = procedure
        self._exec_ctx = None
        self._next_step = None
        self._history = None
        # keep the track of the help texts, used for showing and searching the procedure
        self._help = None

    @property
    def procedure(self):
        # type: () -> StepBasedProcedure
        return self._procedure

    @property
    def context(self):
        return self._exec_ctx

    def create(self, step_cls, **kwargs):
        return step_cls(procedure=self.procedure, **kwargs)

    def create_next_step(self, step_cls, **kwargs):
        next_step = self.create(step_cls=step_cls, **kwargs)
        self.step_next(next_step=next_step)
        return next_step

    def next_step(self):
        return self._next_step

    def run(self, execution_context):
        # type: (ExecCtx) -> None
        self.set_up(execution_context)
        try:
            self.evaluate()
        except KeyboardInterrupt:
            self.step_repeat()  # Control-C pressed. Try again.
        except EOFError:
            traceback.print_exc()
            self.stop_iteration()  # Control-D pressed.
        self.tear_down()

    def set_up(self, execution_context):
        self._exec_ctx = execution_context
        self._next_step = None
        self._history = []
        self._help = []

    def tear_down(self):
        # keep the final context
        self._exec_ctx = self._exec_ctx.copy()

    def evaluate(self):
        pass

    def step_repeat(self):
        raise RepeatStep()

    def step_next(self, next_step):
        self._next_step = next_step

    def step_back(self):
        raise StepBack()

    def stop_iteration(self):
        raise StopRun()

    def style_step_name(self):
        return click.style(u'[%s]' % self.name(), fg='green')

    def echo_step_name(self):
        click.echo(self.style_step_name())

    def help_header(self):
        return "%s(%s)" % (self.procedure.name(), self.name())

    def history(self):
        """History is initialized after the step evaluation"""
        return self._history

    def history_append(self, text):
        # type: (str) -> None
        self._history.append(text)

    def history_handler(self):
        return HistoryHandler(get_history=self.procedure.history)

    @classmethod
    def name(cls):
        return class_to_name(cls)

    def help_handler(self, texts):
        texts_copy = copy.deepcopy(texts)
        if texts_copy:
            texts_copy[0] = self.help_header() + "\n" + texts_copy[0]
        return HelpHandler(help_texts=texts_copy)

    @classmethod
    def Help(cls):
        # type: () -> Dict[str, List[str]]
        """
        Used to enable tracking all class help messages without instantiating the class object.
        The help messages that are defined via the Help variable, can thereafter be collected using the
        track_help method.
        The inheriting class is expected to put some content into the Help describing the step behavior.
        """
        return {}

    @classmethod
    def track_help(cls):
        # type: () -> Dict[str, str]
        return dict([(tag, '\n'.join(texts)) for tag, texts in cls.Help().items()])

    @classmethod
    def Graph(cls):
        # type: () -> Dict[str, StepBaseAbs]
        """
        Statically links the step to the succeeding steps.
        Enables extracting an approximation of the execution graph without running the step
        """
        return {}

    @classmethod
    def static_graph(cls):
        return cls.Graph()

    def steps_handler(self):
        # type: () -> InputHandler
        return StepsHandler(get_steps=self.procedure.static_repr_short)

    def step_back_handler(self):
        # type: () -> InputHandler
        return StepBackHandler(step_back=self.step_back)
