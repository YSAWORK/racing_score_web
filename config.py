import os, sys

# base dir config
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")

# key path config
sys.path.append("racing_reports_2018")

# app debug config
debug = True
passthrough_errors = True
use_debugger = False
use_reloader = False
