#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import re


class InputConverter(object):
    """
    Provides a dual functionality of converting the input value - compatible with click libraty prompt method,
    and of keeping the converted value in an object which type can be recognized by an InputHandler object -
    that should decide if it should handle this input
    """
    def convert(self, value):
        # type: (Any) -> Union[InputConverter, None]
        raise NotImplementedError()

    def kind_of(self, other):
        """Enable recognising converters by InputHandler.
        An input handler will decide if to handle the input using the kind_of method"""
        return self.__class__ == other.__class__

    def help(self):
        return ""

    def value(self):
        return NotImplemented


class Flag(InputConverter):
    def __init__(self, short_, long_):
        super(Flag, self).__init__()
        self.short_ = short_
        self.long_ = long_

    def convert(self, value):
        try:
            if value.lower() in [self.short_, self.long_]:
                return self
        except:
            pass

        return None

    def help(self):
        return "%s - %s" % (self.short_, self.long_)

    def value(self):
        return self.long_


class YesFlag(Flag):
    def __init__(self):
        super(YesFlag, self).__init__(short_='y', long_='yes')


class NoFlag(Flag):
    def __init__(self):
        super(NoFlag, self).__init__(short_='n', long_='no')


class HistoryFlag(Flag):
    def __init__(self):
        super(HistoryFlag, self).__init__(short_='hi', long_='history')


class StepsFlag(Flag):
    def __init__(self):
        super(StepsFlag, self).__init__(short_='s', long_='steps')


class StepBackFlag(Flag):
    def __init__(self):
        super(StepBackFlag, self).__init__(short_='b', long_='back')


class HelpFlag(InputConverter):
    def __init__(self, res=None):
        self._rex = re.compile("(^h(\d)?$)|^help$")
        self._res = res

    def convert(self, value):
        res = self._rex.match(value.lower())
        if res:
            return HelpFlag(res=res)
        else:
            return None

    def level(self):
        if self._res is None:
            raise RuntimeError()
        help_level = self._res.group(2)
        if help_level is None:
            return 0
        else:
            return int(help_level)

    def help(self):
        return "h|h1|h2... - show help level"

    def value(self):
        return self._res


class IntConverter(InputConverter):
    def __init__(self, value=None):
        # type: (int) -> IntConverter
        self._value = value

    def convert(self, value):
        try:
            return IntConverter(int(value))
        except:
            return None

    def value(self):
        return self._value

    def help(self):
        return "Integer value is expected"


class StrConverter(InputConverter):
    def __init__(self, value=None):
        # type: (str) -> StrConverter
        self._value = value

    def convert(self, value):
        try:
            return StrConverter(value)
        except:
            return None

    def value(self):
        return self._value

    def help(self):
        return "String value is expected"


class PositiveIntConverter(IntConverter):
    """Convert positive int"""
    def convert(self, value):
        try:
            value = int(value)
            if value < 1:
                raise
            return PositiveIntConverter(value)
        except:
            return None

    def help(self):
        return "Positive integer value is expected"


YES = YesFlag()
NO = NoFlag()
HISTORY = HistoryFlag()
STEP_BACK = StepBackFlag()
STEPS = StepsFlag()
HELP = HelpFlag()
INT = IntConverter()
STR = StrConverter()
