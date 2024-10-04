from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from pathlib import Path
from string import Template
from enum import Enum
import importlib.resources

default_template=None
client = None

# Load default base template from resource package
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
    # Allow additional extra fields for greater flexibility
    model_config = ConfigDict(extra="allow")
    change_required:bool
    content:str|None = Field(None)
    change_explanation:str|None = Field(None)
    severity:SEVERITY|None = Field(None)


def getClient(api_key:str=None, organization:str=None, project:str=None)->OpenAI:
    global client
    if client is None:
        client = OpenAI(
            api_key=api_key,
            organization=organization,
            project = project,
            
        )
    return client


def load_template(file: str | Path|None =None) -> Template:
    if file is None: 
        # Return default template if no file is provided
        return default_template
    # Convert the str file path to Path object
    file_path = Path(file)
    
    # Check and raise error if the file does not exist
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Open and read the file to create a template
    with file_path.open("r", encoding="utf-8") as f:
        template_content = f.read()
    
    # Return the new Template object
    return Template(template_content)

def load_file(file:str | Path) -> str:
    # Convert the string path to Path object and check existence
    file_path = Path(file)
    
    # Check and raise error if file does not exist
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Open and read the contents of the file
    with file_path.open("r", encoding="utf-8") as f:
        content = f.read()
    
    # Return the plain text content
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
    if code_changes.change_required() and code_changes.content is not None:
        write_file(file=code_file,contents=code_changes.content)
    
