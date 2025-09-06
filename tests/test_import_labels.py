import sys
import os
import json

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# Dummy test to ensure import_labels.py can be loaded



def test_json_labels_file_exists():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "../labels_100days.json"
    )
    assert os.path.exists(file_path), "labels JSON file is missing"



def test_labels_json_valid():
    file_path = os.path.join(
        os.path.dirname(__file__),
          "../labels_100days.json"
          )
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list), "Labels JSON should be a list"
