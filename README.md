# Lazy Dev AI

This tool is being built as a local or pipeline tool for applying general prompts to a chatgpt endpoint and applying responses to the code in question.

The intent is to be flexible enough for users to apply their own prompts while still providing good examples and foundations to be used out of the box.

## Environment

The following environment variables are supported
`OPENAI_API_KEY` - this is your openai key for use with their endpoints. REQUIRED
`OPENAI_PROJECT` - openai project. OPTIONAL
`OPENAI_ORGANIZATION`- openai organization. OPTIONAL

Option flags will override anything provided as environment variables

## Use
After installing, full help and commands can be found by running `lazy-dev-ai` in the terminal

## Example

`lazy-dev-ai improve-comments ./src/*.py` - this will attempt to improve comments for all python files within the folder `./src`

`lazy-dev-ai generate-docstrings ./src/*.py` - this will attempt to generate docstrings for all functions within the files matching the pattern



## Current commands
