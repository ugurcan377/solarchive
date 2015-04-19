#! /usr/bin/python2
from pprint import pprint
import click
from solarchive.lifepath import Lifepath


@click.group()
def cli():
    """The Eclipse Phase Companion Software"""

@cli.command()
def lifepath():
    """Create a character with the lifepath system"""
    path = Lifepath()
    path.start_path()
    pprint(path.char)
    #click.echo(path.char)

if __name__ == '__main__':
    cli()