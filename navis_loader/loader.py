""" Load source files and Transform into target file"""
import os
import json
import glob
from typing import List, Dict


def load_file(file_path: str) -> List[Dict]:
    """
    Load the records into memory
    :param file_path:
    :return:
    """
    with open(file_path, "r") as infile:
        data = json.load(infile)

    return data["records"]


def process_files(source_data_dir: str, target_data_dir: str, file_ext: str) -> int:
    """
    Process source files in data directory and save to target directory
    :param source_data_dir: Data directory for source files
    :param target_data_dir: Data directory for target files
    :param file_ext: Source file extension
    :return:
    """
    # read input files
    file_list = glob.glob(os.path.join(source_data_dir, f"*.{file_ext}"))

    for file_path in file_list:
        records = load_file(file_path)
        # process records

    # if target file exists, read target file else target is empty

    # get unique records from target (id, ts)

    # Compare input file records to unique list and grab deltas

    # merge deltas with target and rewrite the file

    return 0
