import click

from cli import commands


@click.group()
def app():
    pass


app.add_command(commands.visual_report)
app.add_command(commands.demo_search)
app.add_command(commands.generate_dataset)
