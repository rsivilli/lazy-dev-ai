import importlib.resources
from pathlib import Path
from string import Template

# Load the default base template from an internal resource file
with importlib.resources.open_text("lazy_dev_ai.templates", "default_base.txt") as file:
    default_template = Template(file.read())


def load_template(file: str | Path | None = None) -> Template:
    """
    Load a template file into a Template object, or use the default template if no file is specified.

    :param file: The path to the template file or None to use the default template.
    :type file: str | Path | None
    :return: Template object loaded with file content or default content.
    :rtype: Template
    :raises: FileNotFoundError if the file specified does not exist.
    """
    if file is None:
        return default_template
    file_path = Path(file)
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with file_path.open("r", encoding="utf-8") as f:
        template_content = f.read()

    return Template(template_content)


def load_file(file: str | Path) -> str:
    """
    Read the content of a given file. If the file does not exist, an exception is raised.

    :param file: The path to the file to read.
    :type file: str | Path
    :return: A string containing the content of the file.
    :rtype: str
    :raises: FileNotFoundError if the file specified does not exist.
    """
    file_path = Path(file)
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with file_path.open("r", encoding="utf-8") as f:
        content = f.read()
    return content


def write_file(file: str | Path, contents: str):
    """
    Write contents to a specified file. If the file path does not exist, it will be created.

    :param file: The path where content will be written.
    :type file: str | Path
    :param contents: The content to write to the file.
    :type contents: str
    """
    file_path = Path(file)
    with file_path.open("w", encoding="utf-8") as f:
        f.write(contents)
