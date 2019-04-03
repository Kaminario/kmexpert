#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import re
import click


def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


def class_to_name(class_obj):
    return " ".join([token.replace('_', ', ') for token in camel_case_split(class_obj.__name__)])


def bold(text):
    return click.style(text, bold=True, reset=False) + click.style("", bold=False, reset=False)


def underline(text):
    return click.style(text, underline=True, reset=False) + click.style("", underline=False, reset=False)


clean_style_re = re.compile('(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')


def clean_style(text):
    return clean_style_re.sub('', text)
