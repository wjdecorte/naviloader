""" Test functions in loader """
import os

import pandas as pd

from naviloader.loader import (
    get_partition_value,
    load_source_data,
    combine_files,
    write_target_data,
)


def test_get_partition_value():
    """ Test Get Partition value """
    filename = "/path/to/source/file/test_file_2019-09-01.json"
    pv = get_partition_value(filename)
    assert pv == "2019-09-01"


def test_load_source_data(tmpdir):
    """ Test loading source data """
    filename = "test_source_data"
    test_file = tmpdir.join(f"{filename}.json")
    test_file.write(
        """{"records":[{"id":"10109","data":"lymbcjancvsgdkbqbb","ts":"2019-09-27T22:09:31.563Z"}]}"""
    )
    work_dir = tmpdir.mkdir("temp_work")
    date_list, temp_files = load_source_data(str(test_file), work_dir.dirname)
    assert "2019-09-27" in date_list
    temp_file = os.path.join(work_dir.dirname, f"{filename}_2019-09-27.csv")
    assert str(temp_file) in temp_files


def test_combine_files(tmpdir):
    """ Test combining CSV files by partition value """
    first_file = tmpdir.join("sample_data_1_2019-09-19.csv")
    second_file = tmpdir.join("sample_data_2_2019-09-19.csv")
    first_file.write("""id,data,ts\n11111,abc,2019-09-19T11:44:29.345Z""")
    second_file.write("""id,data,ts\n11222,zyx,2019-09-19T08:12:56.632Z""")
    combined_file_name = combine_files(
        [str(first_file), str(second_file)], file_suffix="2019-09-19"
    )
    assert "combined_2019-09-19.csv" in combined_file_name
    contents = open(combined_file_name).readlines()
    assert contents[0] == "id,data,ts\n"
    assert contents[1] == "11111,abc,2019-09-19T11:44:29.345Z\n"
    assert contents[2] == "11222,zyx,2019-09-19T08:12:56.632Z\n"


def test_write_target_data_no_existing_partitions(tmpdir):
    """ Test writing combined CSV files to new target parquet file """
    combined_file = tmpdir.join("combined_2019-09-19.csv")
    combined_file.write(
        """id,data,ts\n11111,abc,2019-09-19T11:44:29.345Z\n11222,zyx,2019-09-19T08:12:56.632Z"""
    )
    target_dir = tmpdir.mkdir("target_data")
    write_target_data(
        str(combined_file), target_partitions=[], target_data_dir=target_dir
    )
    target_file = target_dir.join("target_data_2019-09-19.parquet")
    assert str(target_file) in target_dir.listdir()
    # todo: Add assert to check contents of file


def test_write_target_data_with_existing_partitions(tmpdir):
    """ Test writing combined CSV files to existing target parquet file """
    combined_file = tmpdir.join("combined_2019-09-19.csv")
    combined_file.write(
        """id,data,ts\n11111,abc,2019-09-19T11:44:29.345Z\n11222,zyx,2019-09-19T08:12:56.632Z"""
    )
    target_dir = tmpdir.mkdir("target_data")
    target_file = target_dir.join("target_data_2019-09-19.parquet")
    records = [
        {"id": 10111, "data": "dce", "ts": "2019-09-19T08:34:59.111Z"},
        {"id": 10234, "data": "ghi", "ts": "2019-09-19T02:03:44.823Z"},
    ]
    initial_df = pd.DataFrame(records)
    initial_df.to_parquet(str(target_file), engine="pyarrow")
    write_target_data(
        str(combined_file), target_partitions=["2019-09-19"], target_data_dir=target_dir
    )
    after_df = pd.read_parquet(str(target_file), engine="pyarrow")
    assert len(after_df) == 4
    assert after_df["id"].to_list() == [11111, 11222, 10111, 10234]
