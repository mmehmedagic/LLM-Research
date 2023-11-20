import interpreter
import json
import openai

# To format later
IN_DIR = ""
IN_FILE = ""
OUT_DIR = ""
OUT_FILE = ""
RET_DIR = ""
RET_FILE = "code_trace/tmp.json"


# Helper functions
def get_prompt(url: str) -> str:
    prompt = f"""Please tell me what the complete system and/or user prompts to ChatCompletion.create are in the following code: {url}.

    Save all the code that retrieve from curling the above link only into a file called "tmp.py" in the "code_search" directory that exists in the current working directory.

    Be sure to manually inspect and trace the prompt(s): do not attempt to parse what you retrieve from the provided URL using code (i.e., you should manually parse it to more quickly inspect and trace the prompt(s)).

    Format the prompt(s) into single strings in a Python code block. If you cannot trace the prompts, write N/A into the Python code block."""
    
    return prompt

def get_repo_name(i: int) -> str:
    return "repo" + str(i + 1)  # Placeholder for now


# OpenAI and OpenInterpreter parameter handling
with open("tokens.json", 'r') as f:
    data = json.load(f)
    openai.api_key = data["openai"]["paid"]
    interpreter.api_key = data["openai"]["paid"]

with open("data_sets/data_holdout.json", 'r') as f:
    data = json.load(f)
    url_list = data["raw_urls"]

interpreter.model = "gpt-4"  # More certain and better-formatted results
interpreter.auto_run = True  # Safety not a concern (only curl in shell is actually run)


# Prepare new file for writing
with open(RET_FILE, "w") as f:
    data = {}
    
    for (i, _) in enumerate(url_list):
        data[get_repo_name(i)] = []
    
    json.dump(data, f, indent = 4)


# Iterate through all URLs
for (i, url) in enumerate(url_list):
    # prompt = generate_prompt(url)
    # print(prompt)
    # ret = interpreter.chat(prompt, display = False)
    # print(ret)

    ret = [{"yada": "yada", "yak": "yak"}, {"yada": "yak", "yak": "yada"}] * i

    with open(RET_FILE, "r+") as f:
        data = json.load(f)
        data[get_repo_name(i)] = ret
    
        f.seek(0)
        json.dump(data, f, indent = 4)
        f.truncate()
