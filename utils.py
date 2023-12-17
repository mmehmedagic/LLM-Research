import os

class Path:
    CWD = os.getcwd()
    
    SEARCH_DIR = os.path.join(CWD, "code_search")
    FILE_1000 = "completion_1000.json"
    
    DATA_DIR = os.path.join(CWD, "data_sets")
    HOLDOUT_FILE = "data_holdout.json"
    COMPLETE_FILE = "data_all.json"
    
    TRACE_DIR = os.path.join(CWD, "code_trace")
    TRACE_FILE = "tmp.json"
