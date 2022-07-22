import getopt
import json
import sys
import pandas as pd

from conceptConverter import df_to_ocl_concept
from mappingConverter import df_to_mappings

def get_input_file_sheets_name(input_file_path):
    try:
        sheets_names = pd.ExcelFile(input_file_path).sheet_names
    except Exception as e:
        print("Error while opening the from the file {0} with error {1}".format(input_file_path, e) )
        return None
    return sheets_names

def read_input_file(input_file_path, sheet_name):
    try:
        df = pd.read_excel(input_file_path,sheet_name = sheet_name, skiprows=2)
    except Exception as e:
        print("Error while opening the from the file {0} with error {1}".format(input_file_path, e) )
        return None
    return df

def print_help():
    print('Script to generate json lines to be iported in OCL')
    print('-i input file path')
    print('-h / --help show this help')
    print('-s / --systems to send the comma separated list of system to convert columnName|Org|Source|Version')
    

def get_col(df, name):
    #clean df
    id_col = None
    cols = df.columns
    for col in cols:
        if col.endswith(name):
            id_col = col
    return id_col
def process_df(input_file_path, systems):
    ocl_concepts = []
    sheets_names = get_input_file_sheets_name(input_file_path)
    filepath_ocl = "./ocl_concept.json"
    with open(filepath_ocl, 'w',  encoding="utf-8") as json_file:
        for sheet in sheets_names:
            df = read_input_file(input_file_path, sheet)
            id_col = get_col(df, 'Data Element ID')
            if id_col is not None:
                df = df.dropna(axis=0, subset=[id_col])
                concepts  = df_to_ocl_concept(df,id_col)
                for concept in concepts:
                    json_file.write(json.dumps(concept.dict(exclude_none=True))+"\n")
                mappings = df_to_mappings(df, id_col, systems)
                for mapping in mappings:
                    json_file.write(json.dumps(mapping.dict(exclude_none=True))+"\n")                
                if concepts is not None:
                    ocl_concepts += concepts
                if mappings is not None:
                    ocl_concepts += mappings 
    


if __name__ == "__main__":
    input_file_path=None
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hi:s:",["help","systems="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            sys.exit()
        elif opt in ("-i"):
            input_file_path = arg
        elif opt in ("-s",'--systems'):
            systems = arg.split(',')
    if input_file_path is not None:
        process_df(input_file_path,systems)
    else:
        print_help()
        sys.exit(2)

