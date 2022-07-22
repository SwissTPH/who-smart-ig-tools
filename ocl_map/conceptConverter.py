from models import *

def fhir_concepts_to_ocl_concepts(concepts, concept_class, ocl_concepts = []):
    for concept in concepts:
        ocl_concept = fhir_concept_to_ocl_concept(concept, concept_class)
        if ocl_concept is not None:
            ocl_concepts.append(ocl_concept)
    return ocl_concepts

   
    
    
def fhir_concept_to_ocl_concept(concept, concept_class):    
    return  OCLConcept(
        owner="SwissTPH",# FIXME use config instead
        owner_type=OclConstants.OWNER_STEM_ORGS,
        source="emcare", # FIXME use config instead
        id = concept.code,
        concept_class = concept_class,
        datatype = OclConstants.DATA_TYPE_CODED,
        
        names = [
            OCLDetailedName(
                name = concept.display,
                locale = "eng",# FIXME use config instead
                locale_preferred = True
            )
        ],
        descriptions = [
            OCLDetailedDescription(
                description = concept.definition,
                locale = "eng",# FIXME use config instead
                locale_preferred = True
            )
        ]
    )
    
    
def df_to_ocl_concept(df, id_col):
    jsonlines= []
    if  id_col is not None:
        df = df.dropna(subset=id_col)
        # for each row
        for index, row in df.iterrows():
            line = row_to_ocl_concept(row,id_col )
            if line is not None:
                jsonlines.append(line)
        return jsonlines
    
def row_to_ocl_concept(row, id_col):
    locale = "eng"# TODO use config instead
    data_type = row['Data Type']
    return  OCLConcept(
        owner="SwissTPH",# TODO use config instead
        owner_type=OclConstants.OWNER_STEM_ORGS,
        source="emcare", # TODO use config instead
        id = row[id_col],
        concept_class = "Questions",
        datatype = data_type  if data_type in OclConstants.DATA_TYPES else OclConstants.DATA_TYPE_CODED,
        
        names = [
            OCLDetailedName(
                name = row['Data Element Label'],
                locale = locale,
                locale_preferred = True
            )
        ],
        descriptions = [
            OCLDetailedDescription(
                description =  row['Description and Definition'],
                locale = locale,
                locale_preferred = True
            )
        ]
    )
    
def codeSystem_to_collection(codesystem):
    pass