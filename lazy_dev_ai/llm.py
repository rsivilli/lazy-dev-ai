from lazy_dev_ai.files import load_file,load_template,write_file
from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from pathlib import Path
from enum import Enum

default_template=None
client = None


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
    # Create a client instance only if it hasn't been initialized before
    global client
    if client is None:
        client = OpenAI(
            api_key=api_key,
            organization=organization,
            project = project
            
        )
    return client


def apply_code_template(code_file:str|Path,prompt_file:str|Path=None,prompt:str=None,model: str = "gpt-4-turbo",template_file:str|Path=None,max_retries:int = 3)->CodeChangeResponse:
    # Ensure a valid prompt is provided before proceeding
    if prompt is None and prompt_file is None:
        raise ValueError("Must provide either a prompt or a prompt file")
    prompt = prompt or load_file(prompt_file)
    # Load the template for use
    template = load_template(template_file)
    # Load the code content to be modified
    code = load_file(code_file)
    # Prepare system message with file contents and provided prompt
    messages = [
        ChatGPTMessage(role=OpenAIRole.SYSTEM,content=template.substitute({"file_contents":code,"prompt":prompt})),

    ]
    # Initialize change checking variables
    code_changes = None
    attempt_count = 0
    # Attempt to generate code changes up to max allowed retries
    while code_changes is None and attempt_count < max_retries:
        try:
            # Attempt to get code changes with available AI model and included file contents
            response = getClient().chat.completions.create(model=model, messages=messages)
            # Validate the suggested changes from response
            code_changes = CodeChangeResponse.model_validate_json(response.choices[0].message.content)
            if code_changes.change_required and code_changes.content is not None:
                # If changes are required, write them back to the file
                write_file(file=code_file,contents=code_changes.content)
            return
        except ValidationError as e:
            # Handle any validation errors
            print(str(e))

    # If retries exceeded without success, assert error
    raise AssertionError("Exceeded max retries with ai")