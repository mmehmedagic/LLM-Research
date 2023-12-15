def askChatGPTAPI(query):
    engine = "gpt-3.5-turbo"
    temperature = 0.5
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    prompt = f'Please just return the top-10 related keywords of papers on "{query}" in JSON format with the key named "keywords". The output must start with "```json" and end with "```".'
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for search suggestion of paper in the field of artificial intelligence"},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature
    )
    response = response['choices'][0]['message']['content']
    keywords = re.search("```json(.*)```", response, flags=re.DOTALL).group(1)
    keywords = json.loads(keywords)
    return keywords

def askChatHelper(query):
    engine = os.environ.get("OPENAI_ENGINE") or 'text-davinci-003'
    api_key = os.environ.get("OPENAI_API_KEY")
    proxy = os.environ.get("OPENAI_PROXY")
    temperature = 0.5
    prompt = f'If I want to search for papers on "{query}", what keywords are recommended to me? Please just return the top-10 related keywords of papers in JSON format with the key named "keywords". The output must start with "```json" and end with "```".'
    chatbot = ChatbotOfficial(api_key=api_key, engine=engine, proxy=proxy)
    response = chatbot.ask(prompt, temperature=temperature)["choices"][0]["text"]
    keywords = re.search("```json(.*)```", response, flags=re.DOTALL).group(1)
    keywords = json.loads(keywords)
    return keywords