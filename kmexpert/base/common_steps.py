#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import os
import datetime
import click

from kmexpert.base.step_base import StepBase


class EndIteration(StepBase):
    def evaluate(self):
        self.stop_iteration()


class StoreHistory(StepBase):
    def store_history(self):
        dirpath = os.getcwd()
        file_name = "%s__%s.history" % (self.procedure.name().replace(' ', '_'),
                                        datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '_'))
        output_path = os.path.join(dirpath, file_name)
        click.echo("Writing the history into:%s" % output_path)
        try:
            with open(output_path, 'w') as f:
                f.writelines("Procedure: %s" % self.procedure.name())
                f.writelines(datetime.datetime.now().isoformat())
                f.writelines("%s" % self.procedure.history())
                f.writelines("\n")
        except Exception as ex:
            click.echo(click.style("Failed writing the history log: %s" % ex.message))
            click.echo("Echoing the history:")
            click.echo("%s" % self.procedure.history())
