import click
import os
from lazy_dev_ai.llm import getClient, apply_code_template
from dotenv import load_dotenv
from pathlib import Path
from lazy_dev_ai.prompts.defaults import load_default_prompt

# Load environment variables from .env and .env.local files with override enabled for the latter
load_dotenv('.env')
load_dotenv('.env.local', override=True)

@click.group()
@click.option('--api-key', envvar='OPENAI_API_KEY', help='API Key for authentication')
@click.option('--project', envvar='OPENAI_PROJECT', default=None, help='Project identifier (optional)')
@click.option('--organization', envvar='OPENAI_ORGANIZATION', default=None, help='Organization identifier (optional)')
def cli(api_key, project=None, organization=None):
    """Initialize the main CLI group, handling API Key authentication and setting up client configuration."""
    if not api_key:
        click.echo("API key not provided. Use --api-key option or set API_KEY in environment variables or .env file.")
    getClient(api_key=api_key, project=project, organization=organization)


@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True, path_type=Path))
def improve_comments(paths):
    """Improve comments in the specified code files using a given template."""
    client = getClient()
    prompt = load_default_prompt('comment')

    for f in paths:
        if f.is_file():
            click.echo(f"Applying template to {f.as_posix()}")
            apply_code_template(code_file=f, prompt=prompt)

if __name__ == '__main__':
    cli()
