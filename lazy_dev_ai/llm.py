from enum import Enum
from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from lazy_dev_ai.files import load_file, load_template, write_file

default_template = None
client = None


class OpenAIRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class SEVERITY(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ChatGPTMessage(BaseModel):
    role: OpenAIRole
    content: str


class CodeChangeResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    change_required: bool
    content: str | None = Field(None)
    change_explanation: str | None = Field(None)
    severity: SEVERITY | None = Field(None)


def getClient(
    api_key: str = None, organization: str = None, project: str = None
) -> OpenAI:
    """Create and return a new client instance if not already created, using provided credentials."""
    global client
    if client is None:
        client = OpenAI(api_key=api_key, organization=organization, project=project)
    return client


def apply_code_template(
    code_file: str | Path,
    prompt_file: str | Path = None,
    prompt: str = None,
    model: str = "gpt-4-turbo",
    template_file: str | Path = None,
    max_retries: int = 3,
) -> CodeChangeResponse:
    """Apply a template to the content of a code file using a specified or loaded prompt and handle potential changes."""
    if prompt is None and prompt_file is None:
        raise ValueError("Must provide either a prompt or a prompt file")
    prompt = prompt or load_file(prompt_file)
    template = load_template(template_file)
    code = load_file(code_file)
    messages = [
        ChatGPTMessage(
            role=OpenAIRole.SYSTEM,
            content=template.substitute({"file_contents": code, "prompt": prompt}),
        ),
    ]
    code_changes = None
    attempt_count = 0
    while code_changes is None and attempt_count < max_retries:
        try:
            response = getClient().chat.completions.create(
                model=model, messages=messages
            )
            code_changes = CodeChangeResponse.model_validate_json(
                response.choices[0].message.content
            )
            if code_changes.change_required and code_changes.content is not None:
                write_file(file=code_file, contents=code_changes.content)
            return
        except ValidationError as e:
            print(str(e))

    raise AssertionError("Exceeded max retries with AI integration")
