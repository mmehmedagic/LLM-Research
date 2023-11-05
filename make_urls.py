import json

def get_raw_url(orig_url: str) -> str:
    """
    
    As an example:
    https://github.com/project-baize/baize-chatbot/blob/main/collect.py
    ...is converted into...
    https://raw.githubusercontent.com/project-baize/baize-chatbot/main/collect.py
    """
    
    raw_url = orig_url.replace("github.com", "raw.githubusercontent.com").replace("blob/", "")
    id_index = raw_url.rfind("#")
    raw_url = raw_url[:id_index]
        
    return raw_url

def update_url_file(file_name: str) -> None:
    with open(file_name, 'r') as f:
        data = json.load(f)
        orig_urls = data["orig_urls"]
    
    raw_urls = []
    for orig_url in orig_urls:
        raw_urls.append(get_raw_url(orig_url))
    
    with open(file_name, 'r+') as f:
        data = json.load(f)
        data["raw_urls"] = raw_urls
        
        f.seek(0)
        json.dump(data, f, indent = 4)
        f.truncate()

update_url_file("training_data.json")