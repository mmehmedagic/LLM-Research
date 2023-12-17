import ast  # Documentation: https://docs.python.org/3/library/ast.html
import json
import os

from utils import Path

with open(os.path.join(Path.URL_DIR, Path.URL_FILE), 'r') as f:
    data = json.load(f)
    url_list = data["raw_urls"]


with open("code_trace/holdout/tmp2.py", 'r') as f:
    tree = ast.parse(f.read())

with open("code_trace/ast.txt", 'w') as f:
    f.write(str(
        ast.dump(tree, indent = 4)
    ))

def create_calls(tree):
    for statement in ast.walk(tree):
        if isinstance(statement, ast.Call) and isinstance(statement.func, ast.Attribute) and statement.func.attr == 'create':
            yield {
                'model': ast.unparse(statement.func.value),
                'args': [ast.unparse(j) for j in statement.args],
                'kwargs': {j.arg: ast.unparse(j.value) for j in statement.keywords}
            }

print([*create_calls(tree)])

# for statement in ast.walk(tree):
#     if isinstance(statement, ast.Call) and isinstance(statement.func, ast.Attribute):
#         if statement.func.attr == 'create' and isinstance(statement.func.value, ast.Attribute):
#             if statement.func.value.attr == 'ChatCompletion':
#                 pass