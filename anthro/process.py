from config import INCLUDE_TEST, GITHUB_TOKEN, CANNONICAL_BASE, OUTPUT_PATH, FHIR_VERSION, LIB_VERSION
from models import anthroModel, anthroRecordModel
import os
from github import Github 
from utils import read_tsv_buffer, read_tsv_file
#https://community.plotly.com/t/how-to-list-existing-files-on-the-url-of-a-github-repository/37297/3
from bs4 import BeautifulSoup
from fhir.resources.library import Library
from fhir.resources.parameterdefinition import ParameterDefinition
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.codesystem import CodeSystem, CodeSystemConcept, CodeSystemConceptProperty,CodeSystemFilter
from fhir.resources.coding import Coding
from fhir.resources.fhirtypes import Canonical
from fhir.resources.datarequirement  import DataRequirement
from fhir.resources.attachment import Attachment

from fhir.resources.relatedartifact import RelatedArtifact

import base64


import re

CLEAN_NAME_LIST = {
"lenanthro":"Lenght",
"weianthro":"Weight",
"bmianthro":"BMI",
"hcanthro":"HeadCircumference",
"acanthro":"ArmCircumference",
"tsanthro":"tricepsSkinfold",
"ssanthro":"subscapularSkinfold",
"wfhanthro":"Weight",
"wflanthro":"Weight"
}





def generate_anthro_concept(row, codeColumn, sexcode):
    if "sex" in row and row["sex"] == sexcode and codeColumn in row and "l" in row and "s" in row and "m" in row: 
        l = row["l"]
        m = row["m"]
        s = row["s"]
        y = int(row[codeColumn]) if codeColumn == "age" else row[codeColumn]
        return anthroRecordModel(l = l, s=s,m=m, y=y)
    else:
        return None

def generate_anthro_concepts(df, sexcode, codeColumn):
    concepts = []
    for index, row in df.iterrows():
        concept = generate_anthro_concept(row, codeColumn, sexcode)
        if concept is not None:
            concepts.append(concept)
    return  concepts

def generate_anthro_libraries(anthroInPath = None):
    df = []
    g =Github(GITHUB_TOKEN)
    cql_base_path = os.path.join(OUTPUT_PATH, 'cql')
    lib_base_path = os.path.join(OUTPUT_PATH, 'resources/library')
    update_lib_version("./anthro/base/anthrobase.cql", os.path.join(cql_base_path,"anthrobase.cql"))
    update_lib_version("./anthro/base/library-anthrobase.json", os.path.join(lib_base_path,"library-anthrobase.json"))
    if INCLUDE_TEST:
        update_lib_version("./anthro/base/anthrotest.cql", os.path.join(cql_base_path,"anthrotest.cql"))
        update_lib_version("./anthro/base/library-anthrotest.json", os.path.join(lib_base_path,"library-anthrotest.json"))
    files_content={}
    if anthroInPath is None:
        print("Get content from Github")

        # URL on the Github where the csv files are stored
        repo = g.get_repo("WorldHealthOrganization/anthro")
        contents = repo.get_contents("data-raw/growthstandards")
        while len(contents) > 0:
            file_desc = contents.pop(0)
            #if file_content.type == "dir":
                #contents.extend(repo.get_contents(file_content.path))
            if file_desc.name.endswith(".txt"):
                print("processing "+file_desc.name)
                files_content[file_desc.name] = read_tsv_buffer(repo.get_contents(file_desc.path).decoded_content)
                #generate_anthro_df(file_desc.name, read_tsv_buffer(file_content.decoded_content),cql_base_path,lib_base_path)     
    elif os.path.exists(anthroInPath):
        print("Get content from local folder "+anthroInPath) 
        for filename in os.listdir(anthroInPath):
            if filename.endswith(".txt"):
                print("processing "+filename)
                f = os.path.join(anthroInPath, filename)
                files_content[filename] =read_tsv_file(f)
    else:
        print("no input found at "+anthroInPath)
    for filename, f in files_content.items():
        generate_anthro_df(filename, f)    
        

def generate_anthro_df(filename,df):
    
    cql_base_path = os.path.join(OUTPUT_PATH, 'cql')
    lib_base_path = os.path.join(OUTPUT_PATH, 'resources/library') 
    valuset_base_path=os.path.join(OUTPUT_PATH, 'vocabulary/valueset')
    codesystem_base_path = os.path.join(OUTPUT_PATH, 'vocabulary/codesystem')
    if not os.path.exists(cql_base_path):
        os.makedirs(cql_base_path)
    if not os.path.exists(lib_base_path):
        os.makedirs(lib_base_path)
    if not os.path.exists(valuset_base_path):
        os.makedirs(valuset_base_path)
    if not os.path.exists(codesystem_base_path):
        os.makedirs(codesystem_base_path)
    name = filename.split(".")[0]
    if df is not None:
        model = generate_anthro_model(name,df)
        generate_anthro_library(model,cql_base_path,lib_base_path)
        generate_anthro_codesystems(model,codesystem_base_path)
        generate_anthro_valuesets(model,valuset_base_path)
        
        
def update_lib_version(src,dst):
    with open(src, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("{{LIB_VERSION}}",LIB_VERSION)
    filedata = filedata.replace("{{FHIR_VERSION}}",FHIR_VERSION)

    # Write the file out 
    with open(dst, 'w') as file:
        file.write(filedata)
     
def  generate_anthro_codesystems(model,codesystem_base_path):
    # generate 1 valueset per column and df
    name = "{}For{}".format(model.clean_name, model.y_name.capitalize())
    codesystem = CodeSystem(
        content = 'complete',
        id = name ,
        name = name,
        version = LIB_VERSION,
        status= "active",
        url=CANNONICAL_BASE+"")
    
    codesystem_male = []
    for row in model.data_male:
        codesystem_male.append(
            CodeSystemConcept(
            code = row.y,
            property=[CodeSystemConceptProperty(code="sex",valueCode="male")],
            concept=[CodeSystemConcept(
                code = row.s,
                property=[CodeSystemConceptProperty(code="column",valueCode="s")]
            ),CodeSystemConcept(
                code = row.l,
                property=[CodeSystemConceptProperty(code="column",valueCode="l")]
            ),CodeSystemConcept(
                code = row.m,
                property=[CodeSystemConceptProperty(code="column",valueCode="m")]
            )]
        ))
        
    codesystem_female = []
    for row in model.data_female:
        codesystem_female.append(
            CodeSystemConcept(
            code = row.y,
            property=[CodeSystemConceptProperty(code="sex",valueCode="female")],
            concept=[CodeSystemConcept(
                code = row.s,
                property=[CodeSystemConceptProperty(code="column",valueCode="s")]
            ),CodeSystemConcept(
                code = row.l,
                property=[CodeSystemConceptProperty(code="column",valueCode="l")]
            ),CodeSystemConcept(
                code = row.m,
                property=[CodeSystemConceptProperty(code="column",valueCode="m")]
            )]
        ))
    codesystem.concept = codesystem_female + codesystem_male

 
    with open(os.path.join(codesystem_base_path, "codesystem-{0}.json".format(name) ), 'w') as file:
        file.write(codesystem.json(indent=4))
        
    
def  generate_anthro_valuesets(model, valuset_base_path):
    pass
    
def generate_anthro_model(name,df):
    y_name = getColumnName(df)
    return      anthroModel(
        name = name,
        y_name=y_name, 
        clean_name = CLEAN_NAME_LIST[name] if name in CLEAN_NAME_LIST else name,
        data_male=generate_anthro_concepts(df,1,y_name),
        data_female=generate_anthro_concepts(df,2,y_name)
    )
     
     

def  generate_anthro_library(model, cql_base_path,lib_base_path):


    filepath = os.path.join(cql_base_path,model.name+".cql")
    filepath_lib = os.path.join(lib_base_path,'library-'+model.name+".json")
    # write file
    cql_buffer = get_lib_header(model) +'\n' + model.print_data()+'\n' + add_zscore_functions(model) +'\n'
    library = generate_libraries_def(model, cql_buffer)
    
    with open(filepath, 'w') as file:
        file.write(cql_buffer)
    with open(filepath_lib, 'w') as file:
        file.write(library.json(indent=4))


def getColumnName(df):
    # make sure indexes pair with number of rows
    df.reset_index() 
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
    return    codeColumn      
    
def add_zscore_functions(model):
    return """define function Zscore{0}For{1}tables(sex String, {1} Decimal):
		if sex = 'female' then  First({0}Female c where c.y = {1} )
		else First({0}Male c where  c.y = {1})
            
define function generateZScore{0}For{1}(sex System.String, {1} System.Decimal, weight  System.Decimal)  : 
	base.computeZScore(
		weight,
		(Zscore{0}tablesFor{1}(sex,{1}).m ), 
		(Zscore{0}tablesFor{1}(sex,{1}).l ),
		(Zscore{0}tablesFor{1}(sex,{1}).s )
	)

define function generate{0}From{1}(sex System.String, {1} System.Decimal, zscore  System.Decimal) : 
	base.computeReverseZScore(
		zscore,
		(Zscore{0}tablesFor{1}(sex,{1}).m ), 
		(Zscore{0}tablesFor{1}(sex,{1}).l ),
		(Zscore{0}tablesFor{1}(sex,{1}).s )
	)
        

    """.format(model.clean_name, model.y_name.capitalize())




        
def get_lib_header(model):
    return """
library {0} version '{2}'
using FHIR version '{1}'
include anthrobase version '{2}' called base
include FHIRHelpers version '{1}' called FHIRHelpers
// Antrho library for {0} Z-Score 
codesystem "administrative-gender": 'http://hl7.org/fhir/administrative-gender'
//code "Female" : 'female' from "administrative-gender"  display 'Female'

""".format(model.name,FHIR_VERSION, LIB_VERSION)

def generate_libraries_def(model, cql):
    name = "{}For{}".format(model.clean_name, model.y_name.capitalize())
    return Library(
        id =  name,
        name = name,
        status='active',
        version = LIB_VERSION,
        url = CANNONICAL_BASE +'Library/'+name,
        type = CodeableConcept(
            coding= [Coding(                
                system = "http://hl7.org/fhir/ValueSet/library-type",
                code = 'logic-library'
                )]
        ),
        parameter=get_lib_parameters(model),
        dataRequirement= get_data_requirement(model),
        content= get_cql_content(model,cql),
        relatedArtifact = get_relatedArtifact()
        
    )
    
def get_relatedArtifact():
    return [
        RelatedArtifact(
            type = "depends-on",
            resource = CANNONICAL_BASE +'Library/anthrobase'
        )
    ]

def get_lib_parameters(model):
    return None
    parameters = [
        ParameterDefinition(
            name = "zscore",
            use='in',
            type='decimal'
        ),
        ParameterDefinition(
            name = model.y_name.capitalize(),
            use='in',
            type='decimal'
        ),ParameterDefinition(
            name = "sex",
            use='in',
            type='decimal'
        ),
        ParameterDefinition(
            name = "generate{0}From{1}".format(model.clean_name, model.y_name.capitalize()),
            use='out',
            type='decimal'
        ),
        ParameterDefinition(
            name = "generateZScore{0}For{1}".format(model.clean_name, model.y_name.capitalize()),
            use='out',
            type='decimal'
        ),
        ParameterDefinition(
            name = "Zscore{0}For{1}tables_s".format(model.clean_name, model.y_name.capitalize()),
            use='out',
            type='decimal'
        ),
        ParameterDefinition(
            name = "Zscore{0}For{1}tables_m".format(model.clean_name, model.y_name.capitalize()),
            use='out',
            type='decimal'
        ),
        ParameterDefinition(
            name = "Zscore{0}For{1}tables_l".format(model.clean_name, model.y_name.capitalize()),
            use='out',
            type='decimal'
        ),
    ]
    
    return parameters

def get_data_requirement(model):
    return [
        DataRequirement(
                    type = "Patient",
                    profile = [ Canonical("http://hl7.org/fhir/StructureDefinition/Patient") ]
                )
        
    ]

def get_cql_content(model,cql):
    return [Attachment(
        id = "ig-loader-" + str(model.name) + ".cql",
        contentType = "text/cql",
        data = base64.b64encode(cql.encode())
    )]

if __name__ == "__main__":
    generate_anthro_libraries( './l2/anthro/')
