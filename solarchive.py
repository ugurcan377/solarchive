#! /usr/bin/python2
from pprint import pprint
import click
from solarchive.lifepath import Lifepath
from solarchive.application import app

@click.group()
def cli():
    """The Eclipse Phase Companion Software"""


@cli.command()
@click.option("--step", default=-1, help='Show this step on debug')
@click.option("--debug", is_flag=True, help="Only print the last step")
def lifepath(debug, step):
    """Create a character with the lifepath system"""
    path = Lifepath()
    path.start_path()
    if debug:
        if step > 1:
            pprint(path.char.get(step, {}))
        else:
            pprint(path.char)
    else:
        click.echo(path.char)

@cli.command()
@click.option("--debug", is_flag=True, help="Start server with debug mode")
def web(debug):
    if debug:
        app.run(debug=True)
    else:
        app.run()


if __name__ == '__main__':
    cli()
