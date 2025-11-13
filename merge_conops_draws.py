import os
import json
from glob import glob

CONOPS_DIR = "PARSED_CONOPS"
DRAWS_DIR = "PARSED_DRAWS"
MERGED_DIR = "MERGED_CONOPS_DRAWS"
os.makedirs(MERGED_DIR, exist_ok=True)

def get_json_files(directory):
    return glob(os.path.join(directory, "*.json"))

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_index(files):
    index = {}
    for path in files:
        data = load_json(path)
        dir_id = data.get("source_directory_id")
        if dir_id is not None:
            index[dir_id] = {"data": data, "path": path}
    return index

conops_files = get_json_files(CONOPS_DIR)
draws_files = get_json_files(DRAWS_DIR)
conops_index = build_index(conops_files)
draws_index = build_index(draws_files)

all_dir_ids = set(conops_index.keys()) | set(draws_index.keys())

for dir_id in sorted(all_dir_ids):
    merged = {}
    if dir_id in conops_index:
        merged["conops"] = conops_index[dir_id]["data"]
    if dir_id in draws_index:
        merged["draw"] = draws_index[dir_id]["data"]
    outpath = os.path.join(MERGED_DIR, f"{dir_id:04d}-merged.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"Wrote {outpath}")
