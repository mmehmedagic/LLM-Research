import interpreter
import json
import openai

with open("tokens.json", 'r') as f:
    data = json.load(f)
    openai.api_key = data["openai"]["paid"]
    interpreter.api_key = data["openai"]["paid"]

with open("data_sets/data_holdout.json", 'r') as f:
    data = json.load(f)
    url_list = data["raw_urls"]

interpreter.model = "gpt-4"

# Test with one URL first
url = url_list[0]

prompt = f"""Please tell me what the complete system and/or user prompts to ChatCompletion.create are in the following code: https://raw.githubusercontent.com/project-baize/baize-chatbot/main/collect.py.

Be sure to manually inspect and trace the prompt(s): do not attempt to parse what you retrieve from the provided URL using code (i.e., you should manually parse it to more quickly inspect and trace the prompt(s)).

Format the prompt(s) into single strings in a python code block. """

for chunk in interpreter.chat(prompt, display = False):
    print(chunk)



# read_file = urllib.request.urlopen(url)  # read_file = open("code_search/test.py", "r")
# code = read_file.read().decode("utf-8")  # code = read_file.read()
# read_file.close()

# write_file = open("code_search/tmp.py", "w")
# write_file.write(code)
# write_file.close()