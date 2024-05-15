""" 
script to generate jsonschema and frictionless schemas
 from yaml definitions
"""
import yaml
from pathlib import Path
import os
import re
import json
import copy
from collections.abc import MutableMapping, MutableSequence, MutableSet,Sequence
from functools import reduce

from core_measures.utils import combine_schemas_to_excel,json_to_df
import frictionless

os.chdir(Path(__file__).parent)

# load yaml
def load_yaml(filepath):
    with open(filepath) as f:
        yamlfile = yaml.safe_load(f)

    return yamlfile

# load all yamls
def load_all_yamls(directory="schemas/dictionary"):
    filepaths = Path(directory).glob("*.yaml")
    return {filepath.stem: load_yaml(filepath) for filepath in filepaths}
def resolve_refs(data, definitions):
    """
    Resolve references recursively in a Python dictionary.

    Args:
        data (dict): The dictionary containing references.
        definitions (dict): The dictionary containing definitions.

    Returns:
        dict: The resolved dictionary.
    """
    def resolve_ref(ref):
        parts = ref.split('/')
        if len(parts) < 2 or parts[0] != '#':
            raise ValueError("Invalid reference format")
        current = definitions
        for part in parts[1:]:
            current = current[part]
        return current

    def resolve(obj):
        if isinstance(obj, dict):
            if "$ref" in obj:
                return resolve(resolve_ref(obj["$ref"]),)
            else:
                return {key: resolve(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [resolve(item) for item in obj]
        else:
            return obj

    return resolve(data)
def run_pipeline_step(input, step):
    """function for input into the reduce functool
    function where the input is the instance and fxn is
    a tuple of either length 1 if only param is input
    and greater than eq 1 if there are additional paramters to fxn
    with dict of parameters second item in tuple
    """
    step = [_step for _step in step if _step]
    fxn = step[0]
    if len(step) > 1:
        params = step[1]
        return fxn(input, **params)
    elif len(step) == 1:
        return fxn(input)
    else:
        raise Exception("Step must be at least of length 1")

if __name__ == "__main__":
    ##### COMPILE frictionless schema fields ########
    dictionary = load_all_yamls()

    # compile json schema fields
    json_pipeline = [
        # recursive fxn so need to grab items from overall dictionary for json paths
        (resolve_refs, {"schema": dictionary})
        
    ]
    tblschemas = resolve_refs(dictionary,dictionary)
    del tblschemas["_definitions"]

    ##### WRITEindividual schemas for data package ##########
    for name,schema in tblschemas.items():

        
        path = Path(f"schemas/table-schema-{name}.json").resolve()
        path.write_text(json.dumps(schema, indent=4))
        df = json_to_df(path)
        # write csv versions
        csvpath = path.parent.with_stem("csvs")
        df.to_csv(csvpath / path.with_suffix(".csv").name,index=False)

    ###### COMBINED DDs #######
    # write combined schemas for data discovery and 'joined' product based on schemaType
    Path("schemas/combined").mkdir(parents=True,exist_ok=True)
    Path("csvs/combined").mkdir(parents=True,exist_ok=True)
    definitions = load_yaml("schemas/dictionary/_definitions.yaml")
    combineddescription = (
    "This schema/data dictionary contains all fields collected baseline and follow ups."
        "If marked, `jcoin:baseline_only` = `True`, the field is only collected at baseline (and not follow up interviews)"
    )

    
    ## Client combined data dictionaries
    clientschema = frictionless.Schema(
        title="Client data dictionary",
        description=combineddescription,
        fields=[],
        missing_values=definitions["missingValues"]
    )
    clientschema.custom["version"] = definitions["version"]
    clientschema.custom["jcoin:missingValuesDescription"] = definitions["jcoin:missingValuesDescription"]
    for name in ["baseline","time-points"]:
        path = Path(f"schemas/table-schema-{name}.json").resolve()
        schema = frictionless.Schema(path)
        for field in schema.fields:

            if "baseline" in name:
                custom = field.custom.get("custom",{})
                custom["jcoin:baseline_only"] = True
                field.custom["custom"] = custom
            else:
                if field.custom.get("custom",{}).get("jcoin:baseline_only"):
                    del field.custom["custom"]["jcoin:baseline_only"]
            
            clientschema.set_field(frictionless.Field.from_descriptor(field.to_dict()))

    clientschema.to_json("schemas/combined/table-schema-clients.json")
    json_to_df("schemas/combined/table-schema-clients.json").to_csv("csvs/combined/table-schema-clients.csv",index=False)    
    
    
    ## staff combined data dictionaries
    staffschema = frictionless.Schema(
        title="Staff data dictionary",
        description=combineddescription,
        fields=[],
        missing_values=definitions["missingValues"]
    
    )
    staffschema.custom["version"] = definitions["version"]
    staffschema.custom["jcoin:missingValuesDescription"] = definitions["jcoin:missingValuesDescription"]
    for name in ["staff-baseline","staff-time-points"]:
        path = Path(f"schemas/table-schema-{name}.json").resolve()
        schema = frictionless.Schema(path)

        for field in schema.fields:

            if "baseline" in name:
                custom = field.custom.get("custom",{})
                custom["jcoin:baseline_only"] = True
                field.custom["custom"] = custom
            else:
                if field.custom.get("custom",{}).get("jcoin:baseline_only"):
                    del field.custom["custom"]["jcoin:baseline_only"]
            staffschema.set_field(frictionless.Field.from_descriptor(field.to_dict()))
    staffschema.to_json("schemas/combined/table-schema-staff.json")
    json_to_df("schemas/combined/table-schema-staff.json").to_csv("csvs/combined/table-schema-staff.csv",index=False)
    
    #### Write to excel ###
    Path("xlsx").mkdir(parents=True,exist_ok=True)
    combine_schemas_to_excel(Path("schemas/combined/").resolve(),"xlsx/core_measures.xlsx")


    ### CREATE COLLABORATIVE PROJECT SCHEMAS ##

    Path("schemas/collab-projects/").mkdir(exist_ok=True,parents=True)
    schema = frictionless.Schema("schemas/combined/table-schema-clients.json")
    
    treatment_preferences = [
        "jdc_person_id",
        "currently_incarcerated",
        "prefer_moud_type",
        "race",
        "marital_status",
        "household_people",
        "work_days",
        "last_opioid_overdose",
        "last_used_opioids",
        "last_withdrawal",
        "last_drug_use",
        "age_first_arrest",
        "age_first_convicted",
        "months_daily_bup",
        "months_sublocade",
        "months_weekly_brixadi",
        "months_monthly_brixadi",
        "months_probuphine_implant",
        "months_daily_ntx",	
        "months_monthly_vivitrol",
        "months_methadone"
    ]

    newfields = []
    for field in schema.fields:
        if field.name in treatment_preferences:
            newfields.append(field)

    if not len(treatment_preferences) == len(newfields):
        raise Exception
    schema.fields = newfields
    schema.title = "MOUD treatment preferences"
    schema.description = ("**Research question:** Among people with OUD who have recently been jailed, what are their MOUD treatment preferences,"
        "how likely are they to be receiving their preferred treatment and what factors are associated with preference")
    schema.description += "\n"
    schema.description += "**Outcome variable**: `patient preference alignmnet - made up of prefer_moud_type + y_moud`\n"
    schema.description += "TODO: Write out entire calculation for `patient preference alignmnet - made up of prefer_moud_type + y_moud` based on these variables\n"
    schema.description += "TODO: Write out calculation to get y_moud\n"

    schema.to_yaml("schemas/collab-projects/treatment-preferences.yaml")

    
    

