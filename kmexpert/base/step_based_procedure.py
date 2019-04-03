#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import click

from kmexpert.base.step_base import StepBaseAbs
from kmexpert.base.execution_graph import ExecutionGraph
from kmexpert.base.procedure_base_abs import ProcedureBaseAbs
from kmexpert.base.common_steps import EndIteration
from kmexpert.base.tooling import bold


class StepBasedProcedure(ProcedureBaseAbs):
    def __init__(self, execution_context, **kwargs):
        super(StepBasedProcedure, self).__init__(execution_context=execution_context)
        self.execution_graph = ExecutionGraph()

    def run(self):
        self.execution_graph.run(from_step=self.start_step(), execution_context=self.ctx)

    def start_step(self):
        # type: () -> StepBaseAbs
        raise NotImplementedError()

    def create(self, step_cls, *args, **kwargs):
        return step_cls(procedure=self, *args, **kwargs)

    def history(self):
        return self.execution_graph.history()

    @classmethod
    def subclass_steps(cls):
        """
        Deprecated - left for a reference, use static_graph instead
        Builds a list of the steps that are SUBCLASSES of the procedure class
        Steps which declaration is not a subclass of the procedure won't be shown
        """
        steps = []
        for attrname in dir(cls):
            obj = getattr(cls, attrname)
            if isinstance(obj, type) and issubclass(obj, StepBaseAbs):
                steps.append(obj)
        return steps

    @classmethod
    def subclass_track_help(cls):
        """
        Deprecated - left for a reference, use static_repr instead
        Statically extract the help texts from all the steps which are declared as a subclass to the procedure.
        The help accuracy depend on the un-enforced effort during the steps implementation
        for statically documenting the step's behaviour.
        """
        help = []
        for step in cls.subclass_steps():
            help.append((step, step.track_help().values()))
        return help

    @classmethod
    def help(cls):
        return cls.__doc__

    def repr(self):
        return self.static_repr()

    def static_repr(self):
        # type: () -> str
        """
        Represent a statically derived approximation (without running the procedure) for the procedure's steps,
        their order and their help messages.
        The approximation means that the accuracy depends on the un-enforced effort during the steps implementation
        for statically documenting the step's behaviour.
        The actual behaviour can be only derived by running the procedure.
        """
        visited = set()
        res = ""
        res += "%s\n" % click.style(self.name(), fg='cyan', bold=True, underline=True)
        res += "%s\n" % self.help()
        for step_cls, step_graph in self.static_graph():
            if step_cls in [EndIteration]:
                continue
            if step_cls in visited:
                continue
            visited.add(step_cls)
            step_graph_repr = ", ".join(["%s -> %s" % (tag, child_cls.name())
                                        for tag, child_cls in step_graph.items()
                                        if child_cls not in [EndIteration]])

            res += click.style("    %(step_name)s (%(children)s)\n" %
                               {'step_name': bold(step_cls.name()), 'children': step_graph_repr}, fg='cyan')
            for text in step_cls.track_help().values():
                res += "      %s\n" % text.replace('\n', '\n      ')

        return res

    def static_repr_short(self):
        visited = set()
        res = ""
        count = 0
        for step_cls, step_graph in self.static_graph():
            if step_cls in [EndIteration]:
                continue
            if step_cls in visited:
                continue
            visited.add(step_cls)
            step_graph_repr = ", ".join(["%s -> %s" % (tag, child_cls.name())
                                        for tag, child_cls in step_graph.items()
                                        if child_cls not in [EndIteration]])

            res += click.style("    %(step_name)s (%(children)s)\n" %
                               {'step_name': bold(step_cls.name()), 'children': step_graph_repr}, fg='cyan')
        return res

    def static_graph_from_step(self, from_step_cls):
        # type: () -> List[Tuple[type(StepBaseAbs), Dict[str, type(StepBaseAbs)]]]
        """
        Extract the static steps graph starting from the input step
        :return: List[Tuple[Step Class, Dict[Child Step Tag, Child Step Class]]]
        """
        graph_ = []
        # using BFS
        next_steps = [from_step_cls]
        # next_steps = [self.procedure().Start()]
        while next_steps:
            step_cls = next_steps.pop(0)
            step_graph = step_cls.Graph()
            graph_.append((step_cls, step_graph))
            next_steps += step_graph.values()

        return graph_

    def static_graph(self):
        # type: () -> List[Tuple[type(StepBaseAbs), Dict[str, type(StepBaseAbs)]]]
        return self.static_graph_from_step(self.start_step().__class__)
