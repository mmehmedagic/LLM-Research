import ast  # Documentation: https://docs.python.org/3/library/ast.html
import json
import os
import re
from typing import Dict, List, Tuple

from utils import Path

def get_create_calls(tree: ast.Module) -> List[Dict[str, str]]:
    calls = list()
    
    for statement in ast.walk(tree):
        if isinstance(statement, ast.Call) and isinstance(statement.func, ast.Attribute) and statement.func.attr == 'create':
            for (i, word) in enumerate(statement.keywords):
                if word.arg == "messages":
                    break
            
            calls.append({
                "func": ast.unparse(statement.func.value),
                "input": word.value
            })
            
    return calls

def find_assignment(tree: ast.Module, var_name: str) -> None:
    print(var_name)
    
def find_function_call(tree: ast.Module, func_name: str, param_id: int) -> None:
    print(func_name)

# Maybe bring in an ML algorithm to know when to stop?
def trace_back_input(tree: ast.Module, input) -> None:
    if type(input) == ast.List:        
        dict_elements = ast.unparse(input)[1:-1]
        dict_elements = re.split("}, {|{|}|', '", dict_elements)[1:-1]
        
        for elt in input.elts:
            prompt = elt.values[1]
            if type(prompt) == ast.Name:
                find_assignment(tree, prompt.id)
        
        print(dict_elements)
            
for i in range(9)[0:1]:
    with open(f"code_trace/holdout/tmp{i}.py", 'r') as f:
        tree = ast.parse(f.read())

    with open("code_trace/ast.txt", 'w') as f:
        f.write(str(
            ast.dump(tree, indent = 4)
        ))
    
    calls = get_create_calls(tree)
    for call in calls:
        trace_back_input(tree, call["input"])
