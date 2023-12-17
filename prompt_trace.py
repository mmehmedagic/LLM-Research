import interpreter
import json
import openai
import os
import re
import time
from typing import List


CWD = os.getcwd()
URL_DIR = os.path.join(CWD, "data_sets")
URL_FILE = "data_holdout.json"
RET_DIR = os.path.join(CWD, "code_trace")
RET_FILE = "tmp.json"


# Helper functions
def get_retrieval_prompt(url: str) -> str:
    prompt = """Retrieve the code from the following URL: """ + url + """
    
    Save all the code that you may retrieve from curling the above link only into a file called "tmp.py" in the "code_trace" directory that exists in the current working directory."""
    
    return prompt

def get_analysis_prompt(line: int) -> str:
    prompt = """Tell me what the complete system and/or user prompts to the function openai.ChatCompletion.create are in the following code located in 'code_trace/tmp.py'
    The call should start at the line number """ + str(line) + """ of the code (if you 0-index the lines). Keep in mind that not all parameters and strings will be in this line.
    
    Be sure to manually inspect and trace the prompt(s): do not attempt to parse what you retrieve from the provided URL using code: i.e., you should manually parse it to more quickly inspect and trace the prompt(s).
    Tracing the prompts(s) means that you should also go through the dependency tree of the file as much as possible. Be sure to keep track of dynamic tokens, however.
    
    Format the prompt(s) into single strings in a Python code block. If the original string of the prompt is not present in this particular file, write "N/A" into the Python code block.
    
    To give an idea of tracing the prompts, here are 3 examples:
    
    1.) If this is where the call is:
    ```
    def call_openai(input):
        openai.ChatCompletion.create(messages = [
            {"role": "system", "content": "You are a helpful writing assistant."},
            {"role": "user", "content": f"Make me a story about {input}."},
        ])
    ```
    ...then write out:
    ```
    system_prompt = "You are a helpful writing assistant."
    user_prompt = f"Make me a story about {input}."
    ```
    
    2.) If this is how the call is structured:
    ```
    prompt = "Write me some code to traverse a graph with a depth-first search."
        
    openai.ChatCompletion.create(messages = [
        {"role": "user", "content": prompt},
    ])
    ```
    ...then write out:
    ```
    system_prompt = "N/A"
    user_prompt = "Write me some code to traverse a graph with a depth-first search."
    ```
    
    3.) If this is the call:
    ```
    def call_openai(prompt):
        openai.ChatCompletion.create(messages = [
            {"role": "user", "content": prompt},
        ])
    
    def make_story(topic):
        call_openai(f"Make me a story about {topic}.")
    ```
    ...then write out:
    ```
    system_prompt = "N/A"
    user_prompt = f"Make me a story about {topic}."
    ```
    """
        
    return prompt

def get_line_nums(file_name: str) -> List[int]:
    with open(file_name, 'r') as f:
        text = f.read()
    
    matches = re.finditer("openai.ChatCompletion.create", text, re.MULTILINE)
    
    line_nums = list()
    for instance in matches:
        start, _ = instance.span()
        ln = text[:start].count("\n")
        line_nums.append(ln)
    
    return line_nums

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
for (i, url) in enumerate(url_list[:1]):
    retrieval_prompt = get_retrieval_prompt(url)
    ret = interpreter.chat(retrieval_prompt, display = True)
    print(f"Done retrieving: {url}")
    
    line_nums = get_line_nums("code_trace/tmp.py")
    
    analysis_prompt = get_analysis_prompt(line_nums[0])
    ret = interpreter.chat(analysis_prompt, display = True)
    print(f"Done analyzing: {url}")
    
    time.sleep(3)  # Ensure no rate-limit exit
    print(f"Done waiting after: {url}")
    
    print("\n")

# Format the resulting JSON file correctly
with open(os.path.join(RET_DIR, RET_FILE), "r+") as f:
    data = json.load(f)
    f.seek(0)
    json.dump(data, f, indent = 4)
    f.truncate()
