#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

from kmexpert.base.execution_context import ExecCtx


class RepeatStep(RuntimeError):
    """
    A step requesting from the running context to rerun itself, should throw this exception out
    """
    pass


class StepBack(RuntimeError):
    """
    A step requesting from the running context to go one step back, should throw this exception out
    """
    pass

class StopRun(RuntimeError):
    """
    A step requesting from the running context to stop the procedure execution, should throw this exception out
    """
    pass


class StepBaseAbs(object):
    def run(self, execution_context):
        # type: (ExecCtx) -> None
        """Step execution"""
        return NotImplemented

    def next_step(self):
        """
        Return the instance of the step that should be evaluated next
        """
        return NotImplemented

    def history(self):
        # type: () -> List[str]
        """
        Step execution history - required to be available only after the step was run
        Should represent the step meaning and the decisions taken during its execution in a human readable format
        """
        return NotImplemented

    @classmethod
    def Help(cls):
        # type: () -> Dict[str, List[str]]
        """
        Used to enable tracking all class help messages without instantiating the class object.
        The help messages that are defined via the Help variable, can thereafter be collected using the
        track_help method.
        The inheriting class is expected to put some content into the Help describing the step behavior.
        """

    @classmethod
    def track_help(cls):
        # type: () -> Dict[str, str]
        """
        Returns the step help as a dict from a tag to the help's text
        """
        return NotImplemented

    @classmethod
    def static_graph(cls):
        # type: () -> Dict[str, StepBaseAbs]
        """
        Statically links the step to the succeeding steps.
        Enables extracting an approximation of the execution graph without running the step
        """
