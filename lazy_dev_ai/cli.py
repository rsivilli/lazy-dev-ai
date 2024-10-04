import click
import os
from lazy_dev_ai.llm import getClient, apply_code_template
from dotenv import load_dotenv
from pathlib import Path
from lazy_dev_ai.prompts.defaults import load_default_prompt

# Load .env file and override with values from .env.local if present
load_dotenv('.env')
load_dotenv('.env.local', override=True)

@click.group()
@click.option('--api-key', envvar='OPENAI_API_KEY', help='API Key for authentication')
@click.option('--project', envvar='OPENAI_PROJECT', default=None, help='Project identifier (optional)')
@click.option('--organization', envvar='OPENAI_ORGANIZATION', default=None, help='Organization identifier (optional)')
def cli(api_key, project=None, organization=None):
    """Initialize the CLI with options for API key, project, and organization."""
    if not api_key:
        click.echo("API key not provided. Use --api-key option or set API_KEY in environment variables or .env file.")
    getClient(api_key=api_key, project=project, organization=organization)


@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True, path_type=Path))
def improve_comments(paths):
    """Improve or refactor comments in the specified code files using a model-based template."""
    client = getClient()
    prompt = load_default_prompt('comment')

    for f in paths:
        if f.is_file():
            click.echo(f"Refactoring comments in {f.as_posix()}")
            apply_code_template(code_file=f, prompt=prompt)
@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True, path_type=Path))
def generate_docstrings(paths):
    """Generate docstrings for functions in the specified code files using a model-based template."""
    client = getClient()
    prompt = load_default_prompt('docstring')

    for f in paths:
        if f.is_file():
            click.echo(f"Generating docstring for {f.as_posix()}")
            apply_code_template(code_file=f, prompt=prompt)
if __name__ == '__main__':
    cli()
