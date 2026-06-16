import os
import sys

# Ensure both the project root directory and the 'app' directory are in the Python path
# to prevent ModuleNotFoundError when importing modules within this package.
app_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(app_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
