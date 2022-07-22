
import pandas as pd


def read_tsv_file(input_file_path):
    try:
        file = pd.read_csv(input_file_path, sep='\t')
    except Exception as e:
        print("Error while opening the from the file {0} with error {1}".format(input_file_path, e) )
        return None
    return file