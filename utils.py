import os

class Path:
    CWD = os.getcwd()
    URL_DIR = os.path.join(CWD, "data_sets")
    URL_FILE = "data_holdout.json"
    RET_DIR = os.path.join(CWD, "code_trace")
    RET_FILE = "tmp.json"
