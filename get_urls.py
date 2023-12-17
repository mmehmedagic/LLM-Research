import json
from typing import Dict, List
import os

from utils import Path

def get_orig_urls(in_file: str, out_file: str) -> None:
    orig_urls = []
    
    with open(in_file, 'r') as f:
        data: Dict[str, Dict[str, str]] = json.load(f)
        
        for (_, info) in data.items():
            orig_url = info.get("file_url")
            orig_urls.append(orig_url)

    with open(out_file, 'r+') as f:
        data = json.load(f)
        data["orig_urls"] = orig_urls
        
        f.seek(0)
        json.dump(data, f, indent = 4)
        f.truncate()
    
    return orig_urls


def get_raw_urls(file_name: str) -> None:
    orig_urls = []
    raw_urls = []
    
    with open(file_name, 'r') as f:
        data = json.load(f)
        orig_urls = data["orig_urls"]
    
    for orig_url in orig_urls:
        """
        As an example:
        https://github.com/project-baize/baize-chatbot/blob/main/collect.py#L__
        ...is converted into...
        https://raw.githubusercontent.com/project-baize/baize-chatbot/main/collect.py
        """
        raw_url = orig_url.replace("github.com", "raw.githubusercontent.com").replace("blob/", "")
        id_index = raw_url.rfind("#")
        id_index = len(raw_url) if id_index == -1 else id_index

        raw_urls.append(raw_url[:id_index])
    
    with open(file_name, 'r+') as f:
        data = json.load(f)
        data["raw_urls"] = raw_urls
        
        f.seek(0)
        json.dump(data, f, indent = 4)
        f.truncate()

# Holdout data (manually add orig_urls)
get_raw_urls(
    os.path.join(Path.DATA_DIR, Path.HOLDOUT_FILE)
)

# All data
get_orig_urls(
    os.path.join(Path.SEARCH_DIR, Path.FILE_1000),
    os.path.join(Path.DATA_DIR, Path.COMPLETE_FILE)
)
get_raw_urls(
    os.path.join(Path.DATA_DIR, Path.COMPLETE_FILE)
)