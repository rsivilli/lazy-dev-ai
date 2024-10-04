from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from pathlib import Path
from string import Template
from enum import Enum
import importlib.resources

default_template=None
client = None

# Load default base template for use from an internal resource file
with importlib.resources.open_text("lazy_dev_ai.templates", "default_base.txt") as file:
    default_template = Template(file.read())

class OpenAIRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class SEVERITY(str,Enum):
    LOW = "LOW"
    MEDIUM="MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
class ChatGPTMessage(BaseModel):
    role: OpenAIRole
    content: str


class CodeChangeResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    change_required:bool
    content:str|None = Field(None)
    change_explanation:str|None = Field(None)
    severity:SEVERITY|None = Field(None)


def getClient(api_key:str=None, organization:str=None, project:str=None)->OpenAI:
    global client

    # Create a client instance only if it hasn't been initialized before
    if client is None:
        client = OpenAI(
            api_key=api_key,
            organization=organization,
            project = project
            
        )
    return client


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


def apply_code_template(code_file:str|Path,prompt_file:str|Path=None,prompt:str=None,model: str = "gpt-4-turbo",template_file:str|Path=None)->CodeChangeResponse:
    if prompt is None and prompt_file is None:
        raise ValueError("Must provide either a prompt or a prompt file")
    prompt = prompt or load_file(prompt_file)
    template = load_template(template_file)
    code = load_file(code_file)
    messages = [
        ChatGPTMessage(role=OpenAIRole.SYSTEM,content=template.substitute({"file_contents":code,"prompt":prompt})),

    ]
    
    response = getClient().chat.completions.create(model=model, messages=messages)
    code_changes = CodeChangeResponse.model_validate_json(response.choices[0].message.content)
    if code_changes.change_required and code_changes.content is not None:
        write_file(file=code_file,contents=code_changes.content)
    