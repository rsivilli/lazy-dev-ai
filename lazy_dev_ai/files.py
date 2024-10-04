
import importlib
from pathlib import Path
from string import Template

# Load default base template for use from an internal resource file
with importlib.resources.open_text("lazy_dev_ai.templates", "default_base.txt") as file:
    default_template = Template(file.read())

def load_template(file: str | Path|None =None) -> Template:
    # Use the default template if no specific file is given
    if file is None: 
        return default_template
    # Ensures the file path is valid and can be read
    file_path = Path(file)
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
   
    with file_path.open("r", encoding="utf-8") as f:
        template_content = f.read()
    
    return Template(template_content)


def load_file(file:str | Path) -> str:
    file_path = Path(file)
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with file_path.open("r", encoding="utf-8") as f:
        content = f.read()
    return content


def write_file(file:str|Path, contents:str):
    file_path = Path(file)
    with file_path.open("w", encoding="utf-8") as f:
        f.write(contents)

