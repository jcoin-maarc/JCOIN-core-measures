import json
from pathlib import Path
from collections.abc import MutableMapping
import pandas as pd
import frictionless 
def json_to_df(path_or_schema):
    # convert json to csv
    if isinstance(path_or_schema,(Path,str)):
        table_fields = pd.json_normalize(json.loads(Path(path_or_schema).read_text())['fields']).convert_dtypes()
    else:
        table_fields = pd.json_normalize(frictionless.Schema.from_descriptor(path_or_schema).fields).convert_dtypes()
    headers = table_fields.columns.to_list()
    cols = [c for c in ['section','name','title','type','description','trueValues','falseValues',
        'constraints.enum'] if c in headers]
    cols.extend([c for c in headers if not c in cols])
    #format
    table_fields_formatted = (
        table_fields
        [cols] # order
        .applymap(lambda v: "|".join(map(str,v)) if isinstance(v,list) else v) #stringify lists
    )  
    return table_fields_formatted

        
