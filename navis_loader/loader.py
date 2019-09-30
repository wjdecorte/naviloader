""" Load source files and Transform into target file"""
import os
import json
import glob
import shutil
import logging
from typing import List, Tuple
from collections import defaultdict
from tempfile import mkdtemp

import pandas as pd
from dateutil.parser import parse


def get_partition_value(filename: str) -> str:
    """
    Extract the partition value from the file name
    :param filename:
    :return:
    """
    return os.path.splitext(filename)[0].split("_")[-1]


def load_source_data(file_path: str, temporary_dir: str) -> Tuple[List, List]:
    """
    Load the records into memory and partition the data and write to temp files
    :param file_path:
    :param temporary_dir:
    :return: List of file names for partitioned data files
    """
    with open(file_path, "r") as infile:
        data = json.load(infile)
    logging.debug(f"Number of Records={len(data['records'])}")
    records = defaultdict(list)
    for rec in data["records"]:
        key = parse(rec["ts"]).date().isoformat()
        records[key].append(rec)
    file_prefix = os.path.splitext(os.path.basename(file_path))[0]
    logging.debug(f"File Prefix={file_prefix}")
    temp_files = []
    date_list = []
    for k, v in records.items():
        df = pd.DataFrame(v)
        logging.debug(f"PV: {k}  Number of Records={len(df)}")
        df.drop_duplicates(subset=["id", "ts"], keep="last", inplace=True)
        logging.debug(f"PV: {k}  Number of Records={len(df)} (After de-dupe)")
        temp_file = os.path.join(temporary_dir, f"{file_prefix}_{k}.csv")
        df.to_csv(temp_file, index=False)
        temp_files.append(temp_file)
        date_list.append(k)
    return date_list, temp_files


def combine_files(file_list: List, file_suffix: str) -> str:
    """
    Merge a list of files
    :param file_list:
    :param file_suffix:
    :return: File path of combined file
    """
    temp_dir = os.path.dirname(file_list[0])
    logging.debug(f"Temp Dir={temp_dir}")
    file_ext = os.path.splitext(file_list[0])[-1]
    logging.debug(f"File Ext={file_ext}")
    combined_file_name = os.path.join(temp_dir, f"combined_{file_suffix}{file_ext}")
    combined_df = pd.concat(pd.read_csv(f) for f in file_list)
    combined_df.to_csv(combined_file_name, index=False)
    logging.debug(f"Combined File Name={combined_file_name}")
    return combined_file_name


def write_target_data(source_file: str, target_partitions: List, target_data_dir: str):
    """
    Write non-duplicated data to partitioned target files
    :param source_file:
    :param target_partitions:
    :param target_data_dir:
    :return:
    """
    date_value = get_partition_value(source_file)
    logging.debug(f"Date Value={date_value}")
    target_file = os.path.join(target_data_dir, f"target_data_{date_value}.parquet")
    if date_value in target_partitions:
        logging.debug("Target Partition Found")
        # Load source data
        source_df = pd.read_csv(source_file)
        # Load target data
        target_df = pd.read_parquet(target_file, engine="pyarrow")
        # Merge data
        merged_df = pd.merge(source_df, target_df, on=["id", "ts"], how="outer")
        # New Data column takes value from target unless it doesn't exist and
        # then it takes it from the source data
        merged_df["data"] = merged_df.data_y.combine_first(merged_df.data_x)
        merged_df.drop(columns=["data_x", "data_y"], inplace=True)
        logging.info(
            f"{str(len(merged_df) - len(target_df))} record(s) added to {target_file}"
        )
    else:
        # write combined file to target dir in parquet format
        merged_df = pd.read_csv(source_file)
        logging.info(f"{str(len(merged_df))} record(s) written to {target_file}")

    merged_df.to_parquet(target_file, engine="pyarrow")


def process_files(source_data_dir: str, target_data_dir: str, file_ext: str) -> int:
    """
    Process source files in data directory and save to target directory
    :param source_data_dir: Data directory for source files
    :param target_data_dir: Data directory for target files
    :param file_ext: Source file extension
    :return:
    """
    # Get list of source data files
    file_list = glob.glob(os.path.join(source_data_dir, f"*.{file_ext}"))
    logging.debug(f"File List={','.join(file_list)}")
    if not file_list:
        logging.info("No source files found to process")
        return 0
    temp_dir = mkdtemp()
    logging.debug(f"Temp Dir={temp_dir}")
    list_of_dates = []
    temp_data_files = []
    for file_path in file_list:
        dates, temp_files = load_source_data(file_path, temp_dir)
        list_of_dates.extend(dates)
        temp_data_files.extend(temp_files)

    list_of_dates = sorted(list(set(list_of_dates)))
    logging.debug(f"Date List={','.join(list_of_dates)}")
    # combine files with same date
    combined_files = []
    for date_value in list_of_dates:
        combined_file_name = combine_files(
            [x for x in temp_data_files if get_partition_value(x) == date_value],
            date_value,
        )
        combined_files.append(combined_file_name)

    # if target file exists, read target file else target is empty
    target_files = glob.glob(os.path.join(target_data_dir, "*.parquet"))
    logging.debug(f"Target Files={','.join(target_files)}")
    target_partitions = [get_partition_value(x) for x in target_files]
    logging.debug(f"Target Partitions={','.join(target_partitions)}")
    for file_path in combined_files:
        write_target_data(file_path, target_partitions, target_data_dir)

    shutil.rmtree(temp_dir)
    [os.remove(f) for f in file_list]
    return 0
