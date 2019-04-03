#
# (c) 2019 Kaminario Technologies, Ltd.
#
# This software is licensed solely under the terms of the Apache 2.0 license,
# the text of which is available at http://www.apache.org/licenses/LICENSE-2.0.
# All disclaimers and limitations of liability set forth in the Apache 2.0 license apply.
#

import click

from kmexpert.config import Config
from kmexpert.base.execution_context import ExecCtx


@click.group()
@click.pass_context
def cli(ctx):
    """
    Command Line Tool for running interactive decision trees.
    """


@cli.command()
@click.option('--tag', '-t', multiple=True, type=str, required=False,
              help='Search procedure by tag. Case insensitive. Multiple usage allowed.')
@click.option('--search', '-s', type=str, required=False,
              help='Search procedure by text in the procedure\'s and its steps description')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Show procedures documentation')
@click.option('--show', is_flag=True, default=False,
              help='Show procedures in extended format')
@click.option('--name', '-n', multiple=True, type=str, required=False,
                help='Specify procedure by name. Disables other select optoins.')
@click.pass_context
def procedures(ctx, tag, search, verbose, show, name):
    """
    List the available procedures
    \f
    :param discard: discard any arguments
    """
    procedures_names = set(Config.procedures_names())
    if name:
        procedures_names = procedures_names & set(name)
    else:
        if tag:
            procedures_names = procedures_names & set(Config.procedures_names_by_tags(tag))

        if search:
            procedures_names = procedures_names & set(Config.procedures_names_by_search(search))

    def underline(length):
        click.echo(click.style(''.join(['-']) * length, fg='cyan'))

    for procedure_name in procedures_names:
        execution_context = ExecCtx()
        procedure = Config.get_procedure(procedure_name)(execution_context=execution_context)
        if show:
            click.echo(procedure.static_repr())
            underline(len(procedure_name))
        else:
            click.echo(click.style(procedure_name, fg='cyan'))
            if verbose:
                click.echo(procedure.help())
        underline(len(procedure_name))


@cli.command()
@click.pass_context
def tags(ctx):
    """
    List the available procedures tags
    """
    for tag in Config.tags():
        click.echo(tag)


def validate_procedure_name(ctx, param, value):
    value = ' '.join(value)
    if value in Config.procedures_names():
        matching = True
    else:
        lowercase_matching = [name for name in Config.procedures_names() if name.lower() == value.lower()]
        if len(lowercase_matching) == 1:
            value = lowercase_matching[0]
            matching = True
        else:
            matching = False

    if not matching:
        available_procedures = '\n'.join(Config.procedures_names())
        raise click.BadParameter("procedure not found\n\n%s\n%s" %
                                 (click.style('Available Procedures:\n', bold=True, fg='cyan'),
                                  click.style(available_procedures, fg='cyan')))
    return value


@cli.command()
@click.argument('procedure_name', callback=validate_procedure_name, nargs=-1)
@click.pass_context
def run(ctx, procedure_name):
    """
    Run the specified procedure
    """
    procedure_cls = Config.get_procedure(procedure_name=procedure_name)
    if procedure_cls:
        execution_context = ExecCtx()
        procedure = procedure_cls(execution_context=execution_context)
        procedure.run()
        print('Finished running: %s' % procedure.name())

