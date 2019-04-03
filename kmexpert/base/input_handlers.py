#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import click

from kmexpert.base.input_converters import InputConverter, YES, NO, HELP, HISTORY, STEPS, \
    INT, STR, STEP_BACK, PositiveIntConverter


class InputHandler(object):
    def __init__(self):
        self._next_handler = None

    def append(self, next_handler):
        self._next_handler = next_handler
        return next_handler

    def input_converters(self):
        # type: () -> List[InputConverter]
        """Return a list of input converters that the handler will match"""
        if self._next_handler:
            return self._next_handler.input_converters()
        else:
            return []

    def handle(self, input_):
        # type: (InputConverter) -> None
        if self._next_handler:
            return self._next_handler.handle(input_)
        else:
            raise NotImplementedError()

    @classmethod
    def chain(cls, flat_handlers):
        """Create handlers chain from handlers list"""
        handler = flat_handlers[0]
        for next_handler in flat_handlers[1:]:
            handler = handler.append(next_handler)
        return flat_handlers[0]


class EmptyHandler(InputHandler):
    """
    Can be used to terminate the handling sequence without the NotImplementedError
    """
    def __init__(self):
        # type: (Callable) -> EmptyHandler
        super(EmptyHandler, self).__init__()

    def input_converters(self):
        return []

    def handle(self, input_):
        return None


class HelpHandler(InputHandler):
    def __init__(self, help_texts):
        super(HelpHandler, self).__init__()
        self._help_texts = help_texts

    def input_converters(self):
        return [HELP] + super(HelpHandler, self).input_converters()

    def input_options_help(self):
        return "(Command line options: %s)" % '; '.join([converter.help() for converter in self.input_converters()])

    def help(self):
        return self._help_texts

    def style(self, text):
        return click.style(text, fg='cyan')

    def drill_down_help(self):
        return [self.style(text) for text in self.help()]

    def echo_help_short(self):
        ddhelp = self.drill_down_help()
        if ddhelp:
            click.echo(ddhelp[0])

    def echo_help(self, level):
        click.echo("%s\n" % self.input_options_help())
        ddhelp = self.drill_down_help()
        level = min(len(ddhelp)-1, level)
        for l in range(level+1):
            click.echo(ddhelp[l])
        if level < len(ddhelp) - 1:
            to_be_continued = self.style("...\n[---enter h%s to show more help---]" % (level + 1))
            click.echo(to_be_continued)

    def handle(self, input_):
        if input_.kind_of(HELP):
            self.echo_help(input_.level())
        return super(HelpHandler, self).handle(input_)


class NotifyOnHandler(InputHandler):
    def __init__(self, on, msg):
        # type: (InputConverter, str) -> NotifyOnHandler
        super(NotifyOnHandler, self).__init__()
        self._on = on
        self._msg = msg

    def input_converters(self):
        return [self._on] + super(NotifyOnHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(self._on):
            click.echo("   %s" % self._msg)
        return super(NotifyOnHandler, self).handle(input_)


class HistoryHandler(InputHandler):
    """
    Show the execution history
    """
    def __init__(self, get_history):
        # type: (Callable) -> HistoryHandler
        super(HistoryHandler, self).__init__()
        self._get_history = get_history

    def input_converters(self):
        return [HISTORY] + super(HistoryHandler, self).input_converters()

    def echo_history(self):
        click.echo(self._get_history())

    def handle(self, input_):
        if input_.kind_of(HISTORY):
            self.echo_history()
        return super(HistoryHandler, self).handle(input_)


class StepsHandler(InputHandler):
    """
    Show the steps graph as given by the passed handle
    """
    def __init__(self, get_steps):
        # type: (Callable) -> StepsHandler
        super(StepsHandler, self).__init__()
        self._get_steps = get_steps

    def input_converters(self):
        return [STEPS] + super(StepsHandler, self).input_converters()

    def echo_steps(self):
        click.echo(self._get_steps())

    def handle(self, input_):
        if input_.kind_of(STEPS):
            self.echo_steps()
        return super(StepsHandler, self).handle(input_)


class StepBackHandler(InputHandler):
    """
    Show the steps graph as given by the passed handle
    """
    def __init__(self, step_back):
        # type: (Callable) -> StepsHandler
        super(StepBackHandler, self).__init__()
        self._step_back = step_back

    def input_converters(self):
        return [STEP_BACK] + super(StepBackHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(STEP_BACK):
            self._step_back()
        return super(StepBackHandler, self).handle(input_)


class IntHandler(InputHandler):
    def input_converters(self):
        return [INT] + super(IntHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(INT):
            return input_.value()
        else:
            return super(IntHandler, self).handle(input_)


class PositiveIntHandler(InputHandler):
    def input_converters(self):
        return [PositiveIntConverter()] + super(PositiveIntHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(PositiveIntConverter()):
            return input_.value()
        else:
            return super(PositiveIntHandler, self).handle(input_)


class BoolHandler(InputHandler):
    def input_converters(self):
        return [YES, NO] + super(BoolHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(YES):
            return True
        elif input_.kind_of(NO):
            return False
        else:
            return super(BoolHandler, self).handle(input_)


class YesHandler(InputHandler):
    def input_converters(self):
        return [YES] + super(YesHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(YES):
            return True
        else:
            return super(YesHandler, self).handle(input_)


class NoHandler(InputHandler):
    def input_converters(self):
        return [NO] + super(NoHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(NO):
            return True
        else:
            return super(NoHandler, self).handle(input_)


class StrHandler(InputHandler):
    def input_converters(self):
        return [STR] + super(StrHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(STR):
            return input_.value()
        else:
            return super(StrHandler, self).handle(input_)


class ConverterHandler(InputHandler):
    def __init__(self, converter):
        super(ConverterHandler, self).__init__()
        self._converter = converter

    def input_converters(self):
        return [self._converter] + super(ConverterHandler, self).input_converters()

    def handle(self, input_):
        if input_.kind_of(self._converter):
            return input_.value()
        else:
            return super(ConverterHandler, self).handle(input_)
