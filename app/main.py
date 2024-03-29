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
SCHEMA_DIR = "https://api.github.com/repos/jcoin-maarc/JCOIN-Core-Measures/contents/schemas"
SCHEMA_DIR = str(Path(__file__).parents[1]/"schemas")
study_name = "JCOIN Core Measures"
fields_propnames = ["fields","data_dictionary"]
field_propname = "fields"
current_date = time.strftime("%Y_%m_%d")

# Study title 
st.markdown(f"# {study_name}")

## Read in schemas

# Via github api
# read_schema_dir = lambda schema_dir_url: requests.get(SCHEMA_DIR).json()
# schemas = [json.loads(requests.get(schema["download_url"]).content) for schema in read_schema_dir(SCHEMA_DIR)]

# Via local directory
schemas = [json.loads(path.read_text()) for path in Path(SCHEMA_DIR).glob("*.json")]

## Download button of all schemas in excel format
## TODO: compile from schemas json array
## TODO: make option of csvs with descriptor
## NOTE: for now just leaving as core meaures
excel = list(Path(SCHEMA_DIR).parent.joinpath("xlsx").glob("*"))[0]
with open(excel,"rb") as f:
    st.download_button(
        f"Click here to download an excel file with all {study_name} data dictionaries",
        data=f,
        file_name="core_measures"+"_"+current_date+".xlsx")

## Select schema by title
selected = st.selectbox("Select a data dictionary:",options=[schema["title"] for schema in schemas])
for schema in schemas:
    if selected==schema["title"]:
        orderedschema = dict(schema)

# Render schema properties

for propname,prop in orderedschema.items():

    ## fields property
    if propname==field_propname:
        st.markdown(f"## `{propname}`")
        
        # Format fields
        fields_tbl = pd.json_normalize(orderedschema[field_propname])
        fields_columns = fields_tbl.columns.tolist()
        ## Toggle how fields are viewed and downloaded
        selected_columns = st.multiselect(label="Select Properties",options=fields_columns,default=fields_columns)
        
        ## Field view type
        field_view_exts = {"table":".csv","json records":".json"}
        fields_view_type = st.radio(
            label="Variable View Format",
            options=field_view_exts.keys(),
            horizontal=True)

        if fields_view_type=="table":
            fields = orderedschema[field_propname] = fields_tbl[selected_columns]
            download_fields = lambda fields: fields.to_csv(index=False).encode('utf-8')
            st_fields = lambda fields: st.dataframe(fields)
        elif fields_view_type=="json records":
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

    ## other property types
    elif isinstance(prop,str):
        st.markdown(f"## `{propname}`")
        st.markdown(prop)
    else:
        st.write(prop)