#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

from kmexpert.base.execution_context import ExecCtx
from kmexpert.base.tooling import class_to_name


class ProcedureBaseAbs(object):
    def __init__(self, execution_context, **kwargs):
        # type: (ExecCtx, Dict[Any]) -> ProcedureBaseAbs
        self.ctx = execution_context

    def run(self):
        raise NotImplementedError()

    @classmethod
    def name(cls):
        return class_to_name(cls)

    def repr(self):
        """
        Return the textual procedure representation
        """
        return NotImplemented