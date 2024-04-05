import pandas as pd 
from frictionless import Schema
from pathlib import Path

from .json import json_to_df
#TODO: change csvpaths to schema paths, make json tabular, and then make a frictionless plugin
def _increase_colwidth(df,worksheet,index=False):
    """ 
    widen columns in worksheet object based on length of longest text
    default is no index in worksheet
    """ 
    headers = ['index'] + df.columns.tolist() if index else df.columns.tolist()
    for i, col in enumerate(headers):
        column_len = df[col].astype(str).str.len().max()

        if col in ['description','title','constraints.enum','encodings']:
            column_len = max(column_len, len(col))/2
        elif col=='type':
            column_len = max(column_len,len(col)) + 3
        else:
            column_len = max(column_len,len(col))

        worksheet.column_dimensions[chr(65 + i)].width = column_len


def _format_headers(worksheet,freeze=True,wrap=True):
    """ wrap header text in a pandas dataframe worksheet object
    inplace
    """ 
    if freeze:
        worksheet.freeze_panes = 'A2' # freeze headers

    if wrap:
        # wrap text (right now just header text) 
        for row in worksheet.iter_rows(min_row=1, max_col=worksheet.max_column, max_row=1):
            for cell in row:
                cell.alignment = cell.alignment.copy(wrap_text=True)

def combine_schemas_to_excel(schemadir,excelpath):
    """ takes a directory of frictionless schemas (in json format) and combines into an
    excel package, writing to an excel file (table level properties in a README and subsequent sheets
        containings fields for each schema)"""
    schemasheet = []
    with pd.ExcelWriter(excelpath,engine="openpyxl") as writer:
        
        ###generate README with non-fields properties ### 
        for path in Path(schemadir).glob("*.json"):
            schema = Schema(path).to_dict()
            del schema["fields"]
            schema = {name:(",\n".join(item) if isinstance(item,list) else item) for name,item in schema.items()}
            schema['name'] = path.stem
            schemasheet.append(schema)

        schemasheetdf = pd.DataFrame(schemasheet)
        cols = ['name','description']
        cols.extend([c for c in schemasheetdf.columns if not c in cols])
        schemasheetdf.filter(items=cols).to_excel(writer,sheet_name="README")
        # wrap text of all cells
        worksheet = writer.sheets["README"]
        for row in worksheet.iter_rows(min_row=1, max_col=worksheet.max_column, max_row=len(schemasheetdf)):
            for cell in row:
                cell.alignment = cell.alignment.copy(wrap_text=True)
        _increase_colwidth(schemasheetdf, worksheet)

        #### add the table schema csvs as sheets or as one combined sheet ###
        for path in Path(schemadir).glob("*.json"):
            df = json_to_df(path)
            df.to_excel(writer,sheet_name=path.stem,index=False)
            # style sheet
            worksheet = writer.sheets[path.stem]
            _format_headers(worksheet)
            _increase_colwidth(df, worksheet)


    