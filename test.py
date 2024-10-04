from lazy_dev_ai.llm import apply_code_template
import os
from dotenv import load_dotenv
load_dotenv(".env")
load_dotenv(".env.local")

print(apply_code_template("./lazy_dev_ai/llm.py",prompt_file="./lazy_dev_ai/prompts/default_cleanup.txt").content)