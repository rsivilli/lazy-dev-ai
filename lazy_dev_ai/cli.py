import os
from pathlib import Path

import click
from dotenv import load_dotenv

from lazy_dev_ai.llm import apply_code_template, getClient
from lazy_dev_ai.prompts.defaults import load_default_prompt

# Load .env file and override with values from .env.local if present
load_dotenv(".env")
load_dotenv(".env.local", override=True)


@click.group()
@click.option("--api-key", envvar="OPENAI_API_KEY", help="API Key for authentication")
@click.option(
    "--project",
    envvar="OPENAI_PROJECT",
    default=None,
    help="Project identifier (optional)",
)
@click.option(
    "--organization",
    envvar="OPENAI_ORGANIZATION",
    default=None,
    help="Organization identifier (optional)",
)
def cli(api_key, project=None, organization=None):
    """Initialize the CLI environment.

    Args:
        api_key (str): The API key for authentication.
        project (str, optional): The project identifier.
        organization (str, optional): The organization identifier.
    """
    if not api_key:
        click.echo(
            "API key not provided. Use --api-key option or set API_KEY in environment variables or .env file."
        )
    getClient(api_key=api_key, project=project, organization=organization)


@cli.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
def improve_comments(paths):
    """Automatically improve or refactor comments in code files.

    Args:
        paths (Tuple[Path]): The paths to the code files needing comment improvements.
    """
    prompt = load_default_prompt("comment")
    for f in paths:
        if f.is_file():
            click.echo(f"Refactoring comments in {f.as_posix()}")
            apply_code_template(code_file=f, prompt=prompt)


@cli.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
def generate_docstrings(paths: list[Path]):
    """Automatically generate docstrings for functions in code files.

    Args:
        paths (Tuple[Path]): The paths to the code files needing docstrings.
    """
    prompt = load_default_prompt("docstring")

    for f in paths:
        if f.is_file():
            click.echo(f"Generating docstring for {f.as_posix()}")
            apply_code_template(code_file=f, prompt=prompt)


@cli.command()
@click.option("--prompt", type=str, default=None)
@click.option(
    "--prompt-file", default=None, type=click.Path(exists=True, path_type=Path)
)
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
def custom_prompt(prompt, prompt_file, paths: list[Path]):
    """Use custom prompts for generating artistic content from code files.

    Args:
        prompt (str, optional): Specified custom prompt as string.
        prompt_file (Path, optional): File containing custom prompts.
        paths (Tuple[Path]): The paths to the code files where content will be generated.
    """
    if prompt is None and prompt_file is None:
        raise ValueError("Must provide a prompt string or prompt-file")
    for f in paths:
        if f.is_file():
            click.echo(f"Applying custom prompt to {f.as_posix()}")
            apply_code_template(code_file=f, prompt=prompt, prompt_file=prompt_file)
        else:
            click.echo(f"{f.as_posix()} is not a file")


if __name__ == "__main__":
    cli()
