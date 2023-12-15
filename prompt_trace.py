import interpreter
import json
import openai
import os
import time


CWD = os.getcwd()
URL_DIR = os.path.join(CWD, "data_sets")
URL_FILE = "data_holdout.json"
RET_DIR = os.path.join(CWD, "code_trace")
RET_FILE = "tmp.json"


# Helper functions
def get_prompt(url: str) -> str:
    prompt = """Tell me what the complete system and/or user prompts to the function openai.ChatCompletion.create are in the following code: """ + url + """
    In the openai.ChatCompletion.create call, there will be the parameter "messages", which will roughly follow this format:
        [
            {"role": "system", "content": ...},
            {"role": "user", "content": ...},
        ]
    Here, the two instances of "..." are the system and user prompts, respectively, if they are defined within the messages list. These are what you should be looking for.
    
    Save all the code that you may retrieve from curling the above link only into a file called "tmp.py" in the "code_trace" directory that exists in the current working directory.
    Be sure to manually inspect and trace the prompt(s): do not attempt to parse what you retrieve from the provided URL using code: i.e., you should manually parse it to more quickly inspect and trace the prompt(s).
    Format the prompt(s) into single strings in a Python code block. If the original string of the prompt is not present in this particular file, write N/A into the Python code block.
    One direct call to openai.ChatCompletion.create is present in the code, so please inspect thoroughly: there should not be any cause for an N/A result stemming from openai.ChatCompletion.create not being present in the code."""
    
    return prompt

def get_repo_name(i: int) -> str:
    return "repo" + str(i + 1)  # Placeholder for now


# OpenAI and OpenInterpreter parameter handling
with open("tokens.json", 'r') as f:
    data = json.load(f)
    openai.api_key = data["openai"]["paid"]
    interpreter.api_key = data["openai"]["paid"]

with open(os.path.join(URL_DIR, URL_FILE), 'r') as f:
    data = json.load(f)
    url_list = data["raw_urls"]

interpreter.model = "gpt-4"  # More certain and better-formatted results
interpreter.auto_run = True  # Safety not a concern (only curl in shell is actually run)
interpreter.conversation_filename = os.path.join(RET_DIR, RET_FILE)
interpreter.temperature = 0.7


# Iterate through all URLs
for (i, url) in enumerate(url_list):
    prompt = get_prompt(url)
    ret = interpreter.chat(prompt, display = True)
    print(f"Done running: {url}")
    
    # time.sleep(30)  # Ensure no rate-limit exit
    print(f"Done waiting after: {url}")
    
    print("\n")

# Format the resulting JSON file correctly
with open(os.path.join(RET_DIR, RET_FILE), "r+") as f:
    data = json.load(f)
    f.seek(0)
    json.dump(data, f, indent = 4)
    f.truncate()
