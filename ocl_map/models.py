# https://docs.openconceptlab.org/

from enum import Enum
from typing import Dict, List, Optional,  Union, Literal
from xml.dom import HIERARCHY_REQUEST_ERR
from xmlrpc.client import Boolean
from pydantic import BaseModel, constr, AnyHttpUrl
from ocldev.oclconstants import OclConstants as OclConstantsBase

OCLId = constr(regex="^.+$")
OCLName = constr(regex="^.+$")
OCLShortName = constr(regex="^.+$")
OCLLocale= constr(regex="^[a-zA-Z\-]{2,7}$")
Uri = constr(regex="^.+$")
OCLMapCode = constr(regex="^.+$")
class OclConstants(OclConstantsBase):
    #OCL Access type
    ACCESS_TYPE_VIEW = 'View'
    ACCESS_TYPE_EDIT = 'Edit'
    ACCESS_TYPE_NONE = 'None'
    ACCESS_TYPES = [
        ACCESS_TYPE_EDIT,
        ACCESS_TYPE_VIEW,
        ACCESS_TYPE_NONE
    ]
    #https://www.hl7.org/fhir/valueset-codesystem-hierarchy-meaning.html
    HIERARCHY_MEANING_IS_A = 'is-a' 
    HIERARCHY_MEANING_GROUP_BY = 'grouped-by'
    HIERARCHY_MEANING_PART_OF = 'part-of'
    HIERARCHY_MEANING_CLASSIFIED_WITH = ' classified-with'
    HIERARCHY_MEANINGS = [
        HIERARCHY_MEANING_IS_A,
        HIERARCHY_MEANING_GROUP_BY,
        HIERARCHY_MEANING_PART_OF,
        HIERARCHY_MEANING_CLASSIFIED_WITH
    ]
    SOURCE_TYPE_DICTIONARY = "Dictionary"
    SOURCE_TYPE_REFERENCE = "Reference"
    SOURCE_TYPE_EXTERNAL_DICTIONARY = "ExternalDictionary"
    SOURCE_TYPES = [
        SOURCE_TYPE_DICTIONARY,
        SOURCE_TYPE_REFERENCE,
        SOURCE_TYPE_EXTERNAL_DICTIONARY 
    ]
    # MAP type found for fever/malaria on OCL app
    MAP_TYPE_SAME_AS = "SAME-AS"
    MAP_TYPE_PART_OF = "PART-OF"
    MAP_TYPE_Q_AND_A = "Q-AND-A"
    MAP_TYPE_NARROWER_THAN = "NARROWER-THAN"
    MAP_TYPE_CONCEPT_SET = "CONCEPT-SET"
    MAP_TYPE_SYSTEM = "SYSTEM"
    MAP_TYPE_BROADER_THAN = "BROADER-THAN"
    MAP_TYPE_HAS_ANSWER = "HAS-ANSWER"
    MAP_TYPE_HAS_ELEMENT = "HAS-ELEMENT"
    MAP_TYPE_MAP_TO = "MAP-TO"
    MAP_TYPES = [
        MAP_TYPE_SAME_AS,
        MAP_TYPE_PART_OF,
        MAP_TYPE_Q_AND_A,
        MAP_TYPE_NARROWER_THAN,
        MAP_TYPE_CONCEPT_SET,
        MAP_TYPE_SYSTEM,
        MAP_TYPE_BROADER_THAN,
        MAP_TYPE_HAS_ANSWER,
        MAP_TYPE_HAS_ELEMENT,
        MAP_TYPE_MAP_TO,
    ]
    DATA_TYPE_BOOLEAN = 'Boolean'
    DATA_TYPE_COMPLEX = "Complex"
    DATA_TYPE_STRUCTURED_NUMERIC = "Structured-Numeric"
    DATA_TYPE_RULE = "Rule"
    DATA_TYPE_DATETIME = "Datetime"
    DATA_TYPE_TIME = "Time"
    DATA_TYPE_DATE = "Date"
    DATA_TYPE_DOCUMENT = "Document"
    DATA_TYPE_CODED = "Coded"
    DATA_TYPE_STRING = "String"
    DATA_TYPE_TEXT = "Text"
    DATA_TYPE_NA = "N/A"
    DATA_TYPE_NUMERIC = "Numeric"
    DATA_TYPE_NONE = "None"
    DATA_TYPES =[
        DATA_TYPE_BOOLEAN,
        DATA_TYPE_CODED,
        DATA_TYPE_STRING,
        DATA_TYPE_TEXT,
        DATA_TYPE_NA,
        DATA_TYPE_NUMERIC,
        DATA_TYPE_NONE,
        DATA_TYPE_COMPLEX,
        DATA_TYPE_STRUCTURED_NUMERIC,
        DATA_TYPE_RULE,
        DATA_TYPE_DATETIME,
        DATA_TYPE_TIME,
        DATA_TYPE_DATE,
        DATA_TYPE_DOCUMENT
    ]
    DESCRIPTION_TYPE_DEFINITION = "Definition"
    DESCRIPTION_TYPE_NONE = "None"
    DESCRIPTION_TYPES = [
        DESCRIPTION_TYPE_DEFINITION,
        DESCRIPTION_TYPE_NONE
                         
    ]
    NAME_TYPE_INDEX_TERM = "Index-Term"
    NAME_TYPE_SHORT = "Short"
    NAME_TYPE_FULLY_SPECIFIED = "Short"
    NAME_TYPE_NONE = "None"
    NAME_TYPES = [
        NAME_TYPE_INDEX_TERM,
        NAME_TYPE_SHORT,
        NAME_TYPE_FULLY_SPECIFIED,
        NAME_TYPE_NONE                   
    ]
OCLRessourceType= Literal[tuple(OclConstants.RESOURCE_TYPES)]

class OCLBaseModel(BaseModel):
    type:OCLRessourceType
    id:OCLId
    external_id:Optional[str]
    public_access:Literal[tuple(OclConstants.ACCESS_TYPES)] = OclConstants.ACCESS_TYPE_VIEW
    extras:Dict[str,Union[str,Dict[str,str]]] = []
    url: Optional[Union[AnyHttpUrl,Uri]]
    # enriched data for get
class OclGet(BaseModel):
    created_on:Optional[str]
    created_by:Optional[str]
    updated_on:Optional[str]
    updated_by:Optional[str]
    
class OCLBaseModelBrowsable(OCLBaseModel):
    name:OCLName
    description:Optional[str]
    website:Optional[AnyHttpUrl]
    

class OCLDetailedName(BaseModel):
    name: str
    external_id:Optional[str]
    locale:OCLLocale
    locale_preferred:Optional[Boolean]
    name_type:Literal[tuple(OclConstants.NAME_TYPES)] = OclConstants.NAME_TYPE_SHORT

class OCLDetailedDescription(BaseModel):
    description:str
    external_id:Optional[str]
    locale:OCLLocale
    locale_preferred:Optional[Boolean]
    description_type:Literal[tuple(OclConstants.DESCRIPTION_TYPES)] = OclConstants.DESCRIPTION_TYPE_DEFINITION

class OCLConcept(OCLBaseModel):
    type:OCLRessourceType = OclConstants.RESOURCE_TYPE_CONCEPT
    uuid: Optional[str]
    concept_class: str
    datatype:Literal[tuple(OclConstants.DATA_TYPES)] = OclConstants.DATA_TYPE_NONE
    names:List[OCLDetailedName]
    descriptions: Optional[List[OCLDetailedDescription]]
    retired:Boolean = False
    # not for create
    versions: Optional[str] # TODO version
    source:Optional[OCLId]
    owner:Optional[OCLId]
    owner_type:Optional[Literal[tuple(OclConstants.OWNER_TYPE_TO_STEM.values())]]
    owner_url:Optional[Union[AnyHttpUrl,Uri]]
    versions_url:Optional[Union[AnyHttpUrl,Uri]]
    source_url:Optional[Union[AnyHttpUrl,Uri]]
    owner_url:Optional[Union[AnyHttpUrl,Uri]]
    mappings_url:Optional[Union[AnyHttpUrl,Uri]]
    
class OCLMapping(BaseModel):
    type:OCLRessourceType = OclConstants.RESOURCE_TYPE_MAPPING
    uuid: Optional[str]
    retired:Boolean = False
    map_type: Literal[tuple(OclConstants.MAP_TYPES)]
    from_concept_url:Union[AnyHttpUrl,Uri]
    from_source_url:Optional[Uri]
    from_concept_code:Optional[str]
    from_concept_name:Optional[str]
    to_concept_url:Optional[Union[AnyHttpUrl,Uri]]
    to_source:Optional[str]
    to_concept_code:Optional[str]
    to_source_owner:Optional[OCLId]
    to_source_owner_type:Optional[Literal[tuple(OclConstants.OWNER_TYPE_TO_STEM)]]
    #for bulk
    source:Optional[OCLId]
    owner:Optional[OCLId]
    owner_type:Optional[Literal[tuple(OclConstants.OWNER_TYPE_TO_STEM.values())]]

class OCLCollection(OCLBaseModelBrowsable):
    #TODO https://docs.openconceptlab.org/en/latest/oclapi/apireference/collections.html
    pass

class OCLUser(OCLBaseModelBrowsable):
    #TODO https://docs.openconceptlab.org/en/latest/oclapi/apireference/users.html
    pass 
    
class  OCLMappingInternal(OCLMapping):             
    to_concept_url:Union[AnyHttpUrl,Uri]
    # when there is not URL
    
class  OCLMappingExternal(OCLMapping):   
    to_source_url:Uri
    to_concept_code:str
    to_concept_name:Optional[str]
        
class OCLOrganisation(OCLBaseModelBrowsable):
    type:OCLRessourceType = OclConstants.RESOURCE_TYPE_ORGANIZATION
    company:OCLName
    logo_url:AnyHttpUrl
    location:OCLName
    text:str
    
    

class OCLSource(OCLBaseModelBrowsable):
    type:OCLRessourceType = OclConstants.RESOURCE_TYPE_SOURCE
    short_code:OCLShortName
    full_name:OCLName
    source_type:Literal[tuple(OclConstants.SOURCE_TYPES)] = OclConstants.SOURCE_TYPE_DICTIONARY
    default_locale:OCLLocale = 'en'
    supported_locales:List[OCLLocale] = ['en']
    custom_validation_schema:str = 'None'
    # not for create
    owner:Optional[OCLId]
    owner_type:Optional[Literal[tuple(OclConstants.OWNER_TYPE_TO_STEM)]]
    owner_url:Optional[Union[AnyHttpUrl,Uri]]
    #FHIR
    hierarchy_meaning:Optional[Literal[tuple(OclConstants.HIERARCHY_MEANINGS)]]
    hierarchy_root_url:Optional[Union[AnyHttpUrl,Uri]]
    meta:Optional[str]
    canonical_url:Optional[Union[AnyHttpUrl,Uri]]
    internal_reference_id:Optional[OCLId]
    #collection_reference:Uri
    versions_url:Optional[Union[AnyHttpUrl,Uri]]
    concepts_url:Optional[Union[AnyHttpUrl,Uri]]
    mappings_url:Optional[Union[AnyHttpUrl,Uri]]
    
    versions: Optional[str] # TODO version
    active_concepts:int
    active_mappings:int
    
class OCLSourceVersion(OCLBaseModelBrowsable):
    released: Optional[Boolean]
    previous_version :str
    parent_version :str
