from typing import Literal
import importlib

default_prompts = Literal["comment","cleanup"]

def load_default_prompt(prompt_name:default_prompts)->str:
    file = None
    if prompt_name == "cleanup":
        file = "default_cleanup.txt"
    elif prompt_name == "comment":
        file= "default_comment.txt"
    with importlib.resources.open_text("lazy_dev_ai.prompts", file) as file:
        return file.read()