#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import click

from kmexpert.base.prompt_validators import InputValidator


class Notification(object):
    def __init__(self, message):
        self._message = message

    def run(self):
        click.echo("   %s" % self._message.replace('\n', '\n   '))


class ProcedureStartNotification(object):
    def __init__(self, procedure):
        self._procedure = procedure

    def run(self):
        return Notification(self._procedure.name()).run()


class PromptBase(object):
    def __init__(self, msg, validator, handler):
        self._msg = msg
        self._handler = handler
        self._validator = validator
        self._prompt_res = None

    def run(self):
        return NotImplemented

    def res(self):
        """the result is valid only after running the prompt"""
        return self._prompt_res

    def history(self):
        """history results are valid only after running the prompt"""
        return "%(msg)s: %(res)s" % {'msg': self._msg,
                                     'res': click.style("%s" % self._prompt_res, fg='green')}


class Prompt(PromptBase):
    """Loop until a legal response received"""
    def __init__(self, msg, handler):
        # type: (str, InputHandler) -> Prompt
        super(Prompt, self).__init__(msg=msg,
                                     validator=InputValidator(handler.input_converters()),
                                     handler=handler)

    def run(self):
        text = click.style(self._msg, fg='green')
        while True:
            prompt_res = click.prompt(text=text, type=self._validator)
            try:
                self._prompt_res = self._handler.handle(prompt_res)
                return self._prompt_res
            except NotImplementedError:
                continue

