#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import click

from kmexpert.base.input_converters import InputConverter

EXAMPLES = ['e', 'examples']
QUIT = ['q', 'quit']
BACKWARD = ['b', 'goback']
STEPS = ['s', 'steps']
NEXT = ['n', 'next']
GOTO = ['g', 'goto']
HISTORY = ['hi', 'history']


class Validator(click.ParamType):
    def __init__(self, converters, *args, **kwargs):
        # type: (List[InputConverter]) -> Validator
        super(Validator, self).__init__()
        self._input_converters = converters

    def convert(self, value, param, ctx):
        return NotImplemented

    @property
    def converters(self):
        return self._input_converters

    def help_short(self):
        return NotImplemented

    def help_long(self):
        return NotImplemented

    def __add__(self, other):
        """Return a validator that is a combination of the two input validators"""
        return self.__class__(flags=self.converters + other.converters)


class InputValidator(Validator):
    def __init__(self, converters, *args, **kwargs):
        super(InputValidator, self).__init__(converters=converters, *args, **kwargs)

    def convert(self, value, param, ctx):
        # type: (Any, Any, Any) -> InputConverter
        for converter in self._input_converters:
            res = converter.convert(value)
            if res:
                return res

        self.fail("%s. Help: %s\n" % (value, self.help_long()), param, ctx)

    def help_long(self):
        return '; '.join([converter.help() for converter in self._input_converters])
