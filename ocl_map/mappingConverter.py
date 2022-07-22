from models import OCLMapping, OclConstants


def df_to_mappings(df, id_col, systems):
    jsonlines = []
    for system in systems:
        system_data = system.split('|')
        # at least the col name, org and source are required
        if len(system_data)<2:
            print("Error, the system {} don't have the mandatory fields ".format(system))
            break
        col = system_data[0]
        org = system_data[1]
        source = system_data[2] if len(system_data)>2 else None
        version = system_data[3] if len(system_data)==4 else None
        #FIXME for testing only
        col = 'ICD-11\nVer 05/2021\nCode'
        if col not in df.columns:
            print("Error, the column {} was not found ".format(col))
            break
        df_mapping =    df.dropna(axis=0, subset=[col])

        for index, row in df_mapping.iterrows():
            line = row_to_mapping(row,id_col,col, org,source,version )
            if line is not None:
                jsonlines.append(line)
    return jsonlines


# dict target Dict[columnName, system URI]
def row_to_mapping(row,id_col,col, org,source,version):
    if source is not None and org is not None and row[col] != 'Not classifiable':
        # internal mapping
        return  OCLMapping(
            owner="SwissTPH",# TODO use config instead
            owner_type=OclConstants.OWNER_STEM_ORGS,
            source = 'emcare',
            #from_concept = row[id_col],
                # FIXME use config
            from_concept_url = "/orgs/{}/sources/{}/concepts/{}/".format("SwissTPH","emcare",row[id_col] ),
            to_concept_url = "/orgs/{}/sources/{}/concepts/{}/".format(org, source,row[col] ),
            #to_source_owner = org,
            #to_source = source,
            #to_concept_code = row[col],
             
            map_type =  OclConstants.MAP_TYPE_SAME_AS,
        )