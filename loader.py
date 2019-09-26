import pyspark
import json
import glob


# read input files
file_list = glob.glob("./*.json")
input_file = open("./sample.json","r")
data = json.load(input_file)

# if target file exists, read target file else target is empty

# get unique records from target (id, ts)

# Compare input file records to unique list and grab deltas

# merge deltas with target and rewrite the file