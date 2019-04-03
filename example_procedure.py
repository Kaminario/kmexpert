import click

from kmexpert.base.execution_context import ExecCtx
from kmexpert.config import register_procedure, tag
from kmexpert.base.step_based_procedure import StepBasedProcedure
from kmexpert.base.common_steps import EndIteration, StoreHistory
from kmexpert.base.step_base import StepBase
from kmexpert.base.blocks import Notification
from kmexpert.base.step_blocks import StepPromptBool, StepPromptYes, StepPromptNo
from kmexpert.base.input_handlers import NotifyOnHandler
from kmexpert.base.input_converters import YES, NO
from kmexpert.base.tooling import bold


@register_procedure
class DiagnosePrinter(StepBasedProcedure):
    """
    Printer troubleshooting procedure
    """

    def start_step(self):
        return DiagnosePrinter.Start(self)

    class Start(StepBase):
        @classmethod
        def Graph(cls):
            return {'next': DiagnosePrinter.CheckPower}

        def evaluate(s):
            click.echo("\n")
            Notification(click.style(s.procedure.name(), bold=True)).run()
            click.echo("\n")
            s.create_next_step(s.Graph()['next'])

    class CheckPower(StepBase):
        @classmethod
        def Help(cls):
            return {'h1': ["The printer power cable connection is located on its back",
                           "The power cable is a black cable connected to the socket marked AC"],}

        @classmethod
        def Graph(cls):
            return {'next': DiagnosePrinter.CheckPaper}

        def evaluate(s):
            msg = 'Does your printer is turned on and has power?'
            StepPromptYes(step=s, msg=msg, help=s.Help()['h1'],
                          handlers=[NotifyOnHandler(on=NO, msg="Please connect your printor to a socket and turn it on.")]
                          ).run()
            s.create_next_step(s.Graph()['next'])

    class CheckPaper(StepBase):
        @classmethod
        def Graph(cls):
            return {'yes': DiagnosePrinter.DiagnoseConnection,
                    'no': DiagnosePrinter.AddPaper}

        def evaluate(s):
            msg = 'Do you have paper in the paper tray?'
            if StepPromptBool(step=s, msg=msg, help=[]).run():
                s.create_next_step(s.Graph()['yes'])
            else:
                s.create_next_step(s.Graph()['no'])

    class AddPaper(StepBase):
        @classmethod
        def Help(cls):
            return {'h1': ["Paper tray is located on bottow-front of your printer",
                           "Some thorough instructions for adding paper"],}

        @classmethod
        def Graph(cls):
            return {'next': DiagnosePrinter.DiagnoseConnection}

        def evaluate(s):
            msg = 'Added paper?'
            StepPromptYes(step=s, msg=msg, help=s.Help()['h1'],
                          handlers=[NotifyOnHandler(on=NO, msg="Please add paper.")]
                          ).run()
            s.create_next_step(s.Graph()['next'])

    class DiagnoseConnection(StepBase):
        @classmethod
        def Graph(cls):
            return {'next': DiagnosePrinter.StoreHistory}

        def evaluate(s):
            execution_context = ExecCtx()
            procedure = DiagnoseConnection(execution_context=execution_context)
            procedure.run()
            print('Finished running: %s' % procedure.name())
            s.create_next_step(s.Graph()['next'])

    class FinishedSuccessfully(StepBase):
        @classmethod
        def Graph(cls):
            return {'yes': DiagnosePrinter.StoreHistory,
                    'no': DiagnosePrinter.CallSupport}

        def evaluate(s):
            msg = 'Do you have paper in the paper tray.'
            if StepPromptBool(step=s, msg=msg, help=[]).run():
                s.create_next_step(s.Graph()['yes'])
            else:
                s.create_next_step(s.Graph()['no'])

    class CallSupport(StepBase):
        @classmethod
        def Graph(cls):
            return {'next': DiagnosePrinter.StoreHistory}

        def evaluate(s):
            Notification(click.style("Please call support: 222-222-222", bold=True)).run()
            s.create_next_step(s.Graph()['next'])

    class StoreHistory(StoreHistory):
        def evaluate(s):
            s.store_history()
            s.create_next_step(EndIteration)


@register_procedure
class DiagnoseConnection(StepBasedProcedure):
    """
    Diagnose printer connections
    """

    def start_step(self):
        return DiagnoseConnection.Start(self)

    class Start(StepBase):
        @classmethod
        def Graph(cls):
            return {'next': DiagnoseConnection.MoreSteps}

        def evaluate(s):
            click.echo("\n")
            Notification(click.style(s.procedure.name(), bold=True)).run()
            click.echo("\n")
            s.create_next_step(s.Graph()['next'])

    class MoreSteps(StepBase):
        @classmethod
        def Graph(cls):
            return {'next': DiagnoseConnection.StoreHistory}

        def evaluate(s):
            Notification("\nYou can add %s steps here\n" % bold('MORE')).run()
            s.create_next_step(s.Graph()['next'])

    class StoreHistory(StoreHistory):
        def evaluate(s):
            s.store_history()
            s.create_next_step(EndIteration)
