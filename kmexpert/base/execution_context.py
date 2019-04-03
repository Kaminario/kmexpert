#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#


class ExecCtx(object):
    """execution context"""

    PROCEDURE = 'procedure'

    def __init__(self):
        self.exec_ctx = {}

    def copy(self):
        return ExecCtx.from_dict(self.as_dict())

    def set(self, param, value):
        self.exec_ctx[param] = value

    def get(self, param, default=None):
        return self.exec_ctx.get(param, default)

    def as_dict(self):
        return self.exec_ctx

    @classmethod
    def from_dict(cls, dict_):
        ctx = cls()
        ctx.exec_ctx = dict_
        return ctx



