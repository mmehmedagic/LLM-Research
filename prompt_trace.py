import openai
import urllib.request

openai.api_key = "token"
url_list = [
   f"https://raw.githubusercontent.com/project-baize/baize-chatbot/master/collect.py",
]  # Testing

url = url_list[0]

# EXPAND OUT INTO LOOP WITH URL_LIST

read_file = urllib.request.urlopen(url)  # read_file = open("code_search/test.py", "r")
code = read_file.read().decode("utf-8")  # code = read_file.read()
read_file.close()

write_file = open("code_search/test.py", "w")
write_file.write(code)
write_file.close()

messages = []
messages.append({
    "role": "user", 
    "content": f"Tell me what the function ChatCompletion.create uses as a user prompt in the following code:\n\n'''\n{code}\n'''"
})
completion1 = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo", 
    messages = messages
)
response1 = completion1.choices[0].message

messages.append(response1)
messages.append({
    "role": "user", 
    "content": "Give me an example of a user prompt with the dynamic tokens filled in"  # Trace back what the variable is, in string format
})
completion2 = openai.ChatCompletion.create(
    model = "gpt-3.5", 
    messages = messages
)
response2 = completion2.choices[0].message

messages.append(response2)
messages.append({
    "role": "user", 
    "content": "Format the user prompt into one string yourself now"
})
completion3 = openai.ChatCompletion.create(
    model = "gpt-3.5", 
    messages = messages
)
response3 = completion3.choices[0].message

messages.append(response3)

print(messages)

# NEED TO SORT OUT RATES FOR OPENAI KEY
