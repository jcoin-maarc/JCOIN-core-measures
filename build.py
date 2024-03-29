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

from core_measures import schemas as schema_utils

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
    # compile frictionless schema fields
    dictionary = load_all_yamls()

    # compile json schema fields
    json_pipeline = [
        # recursive fxn so need to grab items from overall dictionary for json paths
        (resolve_refs, {"schema": dictionary})
        
    ]
    tblschemas = resolve_refs(dictionary,dictionary)
    del tblschemas["_definitions"]

    for name,schema in tblschemas.items():
        Path(f"schemas/table-schema-{name}.json").write_text(json.dumps(schema, indent=4))

    schema_utils.to_csv()
    schema_utils.to_excel()