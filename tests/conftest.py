# F:\SkyeAnalytics\tests\conftest.py
import pytest
import sys
import os
from pathlib import Path

# Add the project root to PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)