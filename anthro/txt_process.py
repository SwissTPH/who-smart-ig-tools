from models import anthroModel, anthroRecordModel
import os

from utils import read_tsv_file


def generate_anthro_valueset_concept(row, codeColumn, sexcode):
    if "sex" in row and row["sex"] == sexcode and codeColumn in row and "l" in row and "s" in row and "m" in row: 
        l = row["l"]
        m = row["m"]
        s = row["s"]
        y = int(row[codeColumn]) if codeColumn == "age" else row[codeColumn]
        return anthroRecordModel(l = l, s=s,m=m, y=y)
    else:
        return None

def generate_anthro_valueset_concepts(df, sexcode):
    # make sure indexes pair with number of rows
    df.reset_index() 
    concepts = []
    codeColumn = "age"
    # generate code
    # rename df colum age to codeColumn
    if 'age' in df.columns:
        codeColumn = "age"
    # rename df colum height to codeColumn
    elif 'height' in df.columns:
        codeColumn = "height"
    # rename df colum length to codeColumn
    elif 'length' in df.columns:
        codeColumn = "length"        
    for index, row in df.iterrows():
        concept = generate_anthro_valueset_concept(row, codeColumn, sexcode)
        if concept is not None:
            concepts.append(concept)
    return codeColumn, concepts

def generate_anthro_codesystems(anthroInPath):
    df = []
    if not os.path.exists(anthroInPath):
        exit(-2) 
    anthroOutPath = os.path.join(anthroInPath,"out")
    if not os.path.exists(anthroOutPath):
            os.makedirs(anthroOutPath) 
    if anthroInPath is not None and os.path.exists(anthroInPath):
        for filename in os.listdir(anthroInPath):
            f = os.path.join(anthroInPath, filename)
            name = filename.split(".")[0]
            df = read_tsv_file(f)
            if df is not None:
                generate_anthro_codesystem(name,df, 1, anthroOutPath)
                generate_anthro_codesystem(name,df, 2, anthroOutPath)
            
def  generate_anthro_codesystem(name,df, sexcode, outpath):
    name = "{0}.{1}".format(name, 'male' if sexcode == 1 else 'female')
    y_name, data = generate_anthro_valueset_concepts(df,sexcode)
    code_system =  anthroModel(
        name = "{0}.{1}".format(name, 'male' if sexcode == 1 else 'female'),
        y_name=y_name, 
        data=data
    )
    filepath = os.path.join(outpath,name+".cql")
    # write file
    with open(filepath, 'w') as json_file:
        json_file.write(get_lib_header(name,y_name,sexcode))
        json_file.write(code_system.print_data())
        
def get_lib_header(name,y_name, sex):
    return """
library {0}
using FHIR version '4.0.0'
include FHIRHelpers version '4.0.0'

// Antrho library for {1} Z-Score for {2}

define '{0}':
""".format(name,y_name,'male' if sex == 1 else 'female')



if __name__ == "__main__":
    generate_anthro_codesystems( 'l2/anthro')