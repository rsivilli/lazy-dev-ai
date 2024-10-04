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