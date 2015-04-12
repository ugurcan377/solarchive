import click

@click.group()
def cli():
    """The Eclipse Phase Companion Software"""

@cli.command()
def lifepath():
    """Create a character with the lifepath system"""
    click.echo("Hello Firewall")

if __name__ == '__main__':
    cli()