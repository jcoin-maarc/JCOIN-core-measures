import streamlit as st 
import requests
from pathlib import Path
import time
import pandas as pd
import io 
import sys
import json
import re
from collections.abc import MutableSequence
from core_measures.app.utils import unflatten_from_jsonpath
def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s

st.set_page_config(layout="wide")
GITREPO_DIR = "https://api.github.com/repos/jcoin-maarc/JCOIN-Core-Measures/contents"
SCHEMA_DIR = f"{GITREPO_DIR}/schemas/combined"
EXCELPATH = f"{GITREPO_DIR}/xlsx/core_measures.xlsx"
study_name = "JCOIN Core Measures"
field_propname = "fields"
current_date = time.strftime("%Y_%m_%d")

@st.cache_data
def getschemas():
    schemas = []
    for schema in requests.get(SCHEMA_DIR).json():
        schema_download = requests.get(schema["download_url"]).json()
        schemas.append(schema_download)
    return schemas

@st.cache_data
def getexcel():
    # TODO: compile from schemas
    excel = requests.get(EXCELPATH).json()["download_url"]
    return requests.get(excel).content

excel = getexcel()
schemas = getschemas()
# Study title 
st.markdown(f"# {study_name}")

st.download_button(
    f"Click here to download an excel file with all {study_name} data dictionaries",
    data=getexcel(),
    file_name=study_name.replace(" ","-").lower()+"_"+"v"+schemas[0]["version"]+".xlsx")

## Select schema by title
selected = st.selectbox("Select a data dictionary:",options=[schema["title"] for schema in schemas])
for schema in schemas:
    if selected==schema["title"]:
        selectedschema = dict(schema)

orderedschema = {}
orderedschema["version"] = selectedschema["version"]
for name,item in selectedschema.items():
    orderedschema[name] = item
# Render schema properties
for propname,prop in orderedschema.items():
    if propname == "custom":
        for _prop in prop:
            st.write(_prop)
    ## fields property
    elif propname==field_propname:
        st.markdown(f"## `{propname}`")
        
        # Format fields
        fields_tbl = pd.json_normalize(orderedschema[field_propname])
        fields_columns = fields_tbl.columns.tolist()
        ## Toggle how fields are viewed and downloaded
        
        ## Field view type
        field_view_exts = {"table":".csv","json records":".json"}
        fields_view_type = st.radio(
            label="Variable View Format",
            options=field_view_exts.keys(),
            horizontal=True)

        if fields_view_type=="table":
            selected_columns = st.multiselect(label="Select Properties",options=fields_columns,default=["name","type","format","constraints.pattern","description","custom.jcoin:original_name","constraints.enum","custom.jcoin:baseline_only"])
            fields = orderedschema[field_propname] = fields_tbl[selected_columns]
            download_fields = lambda fields: fields.to_csv(index=False).encode('utf-8')
            st_fields = lambda fields: st.dataframe(fields)
        elif fields_view_type=="json records":
            selected_columns = st.multiselect(label="Select Properties",options=fields_columns,default=fields_columns)
            flattened_fields= fields_tbl[selected_columns]
            flattened_fields.fillna("",inplace=True)
            fields = orderedschema[field_propname] = [unflatten_from_jsonpath(field) for field in flattened_fields.to_dict(orient="records")]
            download_fields = lambda fields: json.dumps(orderedschema,indent=2)
            st_fields = lambda fields:st.json(fields)
        else:
            raise Exception("only json and tabular toggle types")
        st_fields(fields)

        ## Download button for data dictionary
         # NOTE: need selected columns so code here but displayed at `download_container`
        st.download_button(f"Download Selected Fields in {fields_view_type} format",
            data=download_fields(fields),
            file_name=f"{slugify(selected)}{field_view_exts[fields_view_type]}")


    ## any schema-level list property such as primaryKeys, missingValues
    elif isinstance(prop,MutableSequence):
        st.markdown(f"## `{propname}`")
        st.markdown("\n".join([f"- {val}" for val in prop]))

    ## other property types (strings, integers etc)
    else:
        st.markdown(f"## `{propname}`")
        st.markdown(prop)