# cli/main.py
import click
from cli.analyze import analyze
from cli.query import query
from cli.show import show

@click.group()
def cli():
    """⚖️  Judgment Reasoning Analyzer — Legal NLP Pipeline"""
    pass

cli.add_command(analyze)
cli.add_command(query)
cli.add_command(show)