#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

from contextlib import contextmanager
import StringIO
import sys


@contextmanager
def redirect_stdout():
    captured_output = StringIO.StringIO()
    stdout = sys.stdout
    sys.stdout = captured_output
    try:
        yield captured_output
    finally:
        sys.stdout = stdout


def put_in_stdin(value):
    sys.stdin = StringIO.StringIO(value)
