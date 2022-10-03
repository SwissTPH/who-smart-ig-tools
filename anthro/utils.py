
import pandas as pd
import io



def read_tsv_file(input_file_path):
    try:
        df = pd.read_csv(input_file_path, sep='\t')
    except Exception as e:
        print("Error while opening the from the file {0} with error {1}".format(input_file_path, e) )
        return None
    return df

def read_tsv_buffer(buffer):
    try:
        tsv_string = io.BytesIO(buffer)
        df = pd.read_csv(tsv_string, sep='\t')
    except Exception as e:
        print("Error while opening the from the file {0} with error {1}".format(buffer, e) )
        return None
    return df
