import streamlit as st 
import pandas as pd 
from pathlib import Path
from frictionless import Schema
from collections.abc import MutableSequence
import io
#with a container/tab
REPO_DIR = "https://raw.githubusercontent.com/jcoin-maarc/JCOIN-Core-Measures/main"

def load_csv(url_or_path):
    return pd.read_csv(url_or_path)

def load_schema(schema_name):
    return Schema(f"{REPO_DIR}/schemas/{schema_name}.json").to_dict()


def render_schema_page(fieldsdf,schema,schema_name):

    orderedschema = {}
    for prop in ["title","name","description"]: #items to go first
        if prop in list(schema):
            orderedschema[prop] = schema.pop(prop)
    orderedschema.update(schema)

    for propname,prop in orderedschema.items():
        st.markdown(f"## {propname}")
        if propname=="fields":
            selected_table = make_agrid(fieldsdf)
        elif isinstance(prop,MutableSequence):
            st.markdown("\n".join([f"- {val}" for val in prop]))
        else:
            st.markdown(prop)

    schema['fields'] = selected_table 

    return schema


def download_excel(dictionary):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer,engine="xlsxwriter") as writer:
        for name,item in dictionary.items():
            try:
                df = pd.DataFrame(item)
            except ValueError:
                df = pd.DataFrame([item])

            df.to_excel(writer,sheet_name=name)
    
    return buffer

def makepage(schema_name):
    fieldsdf = load_csv(f"{REPO_DIR}/csvs/{schema_name}.csv")
    schema = load_schema(schema_name)
    schema['fields'] = fieldsdf
    buffer = download_excel(schema)

    st.download_button(f"Download {schema_name} in excel",data=buffer,file_name=f"{schema_name}.xlsx")
    st.download_button(f"Download {schema_name} in json",data=Schema(f"{REPO_DIR}/schemas/{schema_name}.json").to_json(),file_name=f"{schema_name}.xlsx")
    schema = render_schema_page(fieldsdf=fieldsdf,schema=schema,schema_name=schema_name)



def unflatten_from_jsonpath(field,missing_values=[None,""]):
    """
    Converts a flattened dictionary with key names conforming to 
    JSONpath notation to the nested dictionary format.
    """
    field_json = {}

    for prop_path, prop in field.items():
        
        if prop in missing_values:
            continue

        prop_json = field_json

        nested_names = prop_path.split(".")
        for prop_name in nested_names[:-1]:
            if '[' in prop_name:
                array_name, array_index = prop_name.split('[')
                array_index = int(array_index[:-1])
                if array_name not in prop_json:
                    prop_json[array_name] = [{} for _ in range(array_index + 1)]
                elif len(prop_json[array_name]) <= array_index:
                    prop_json[array_name].extend([{} for _ in range(array_index - len(prop_json[array_name]) + 1)])
                prop_json = prop_json[array_name][array_index]
            else:
                if prop_name not in prop_json:
                    prop_json[prop_name] = {}
                prop_json = prop_json[prop_name]

        last_prop_name = nested_names[-1]
        if '[' in last_prop_name:
            array_name, array_index = last_prop_name.split('[')
            array_index = int(array_index[:-1])
            if array_name not in prop_json:
                prop_json[array_name] = [{} for _ in range(array_index + 1)]
            elif len(prop_json[array_name]) <= array_index:
                prop_json[array_name].extend([{} for _ in range(array_index - len(prop_json[array_name]) + 1)])
            if isinstance(prop_json[array_name][array_index], dict):
                prop_json[array_name][array_index].update({array_name: prop})
            else:
                prop_json[array_name][array_index] = {array_name: prop}
        else:
            prop_json[last_prop_name] = prop

    return field_json