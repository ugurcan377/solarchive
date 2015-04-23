#! /usr/bin/python2
from pprint import pprint
import click
from solarchive.lifepath import Lifepath


@click.group()
def cli():
    """The Eclipse Phase Companion Software"""

@cli.command()
@click.option("--debug", is_flag=True, help="Only print the last step")
def lifepath(debug):
    """Create a character with the lifepath system"""
    path = Lifepath()
    path.start_path()
    if debug:
        pprint(path.char.get(path.STEPS, {}))
    else:
        pprint(path.char)
        #click.echo(path.char)

if __name__ == '__main__':
    cli()
