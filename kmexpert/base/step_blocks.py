#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

from kmexpert.base.input_handlers import InputHandler, BoolHandler, YesHandler, NoHandler, EmptyHandler
from kmexpert.base.input_converters import HELP
from kmexpert.base.blocks import Prompt


class StepPrompt(object):
    def __init__(self, step):
        # type: (StepBase) -> StepPrompt
        self._step = step

    def run(self):
        return NotImplemented


class StepPromptBool(StepPrompt):
    """Prompt until receiving a bool answer"""
    def __init__(self, step, msg, help, handlers=None):
        super(StepPromptBool, self).__init__(step=step)
        self._msg = msg
        self._help = help
        self._additional_handlers = handlers or []

    def run(self):
        self._step.help_handler(self._help).echo_help_short()
        handler = InputHandler.chain([
            self._step.help_handler(self._help),
            self._step.history_handler(),
            self._step.steps_handler(),
            self._step.step_back_handler(),
            BoolHandler()] + self._additional_handlers)
        prompt = Prompt(msg=self._msg, handler=handler)
        res = prompt.run()
        self._step.history_append(prompt.history())
        return res


class StepPromptYes(StepPrompt):
    """Prompt until receiving yes answer"""
    def __init__(self, step, msg, help, handlers=None):
        super(StepPromptYes, self).__init__(step=step)
        self._msg = msg
        self._help = help
        self._additional_handlers = handlers or []

    def run(self):
        self._step.help_handler(self._help).echo_help_short()
        handler = InputHandler.chain([
            self._step.help_handler(self._help),
            self._step.history_handler(),
            self._step.steps_handler(),
            self._step.step_back_handler(),
            YesHandler()] + self._additional_handlers)
        prompt = Prompt(msg=self._msg, handler=handler)
        res = prompt.run()
        self._step.history_append(prompt.history())
        return res


class StepPromptNo(StepPrompt):
    """Prompt until receiving no answer"""
    def __init__(self, step, msg, help, handlers=None):
        super(StepPromptNo, self).__init__(step=step)
        self._msg = msg
        self._help = help
        self._additional_handlers = handlers or []

    def run(self):
        self._step.help_handler(self._help).echo_help_short()
        handler = InputHandler.chain([
            self._step.help_handler(self._help),
            self._step.history_handler(),
            self._step.steps_handler(),
            self._step.step_back_handler(),
            NoHandler()] + self._additional_handlers)
        prompt = Prompt(msg=self._msg, handler=handler)
        res = prompt.run()
        self._step.history_append(prompt.history())
        return res

