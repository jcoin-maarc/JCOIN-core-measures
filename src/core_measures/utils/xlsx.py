import pandas as pd 
from frictionless import Schema
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

def combine_schemas_to_excel(csvpaths,excelpath,separate_sheets=True):
    csvpaths = list(csvpaths)
    schemasheet = []
    with pd.ExcelWriter(excelpath,engine="openpyxl") as writer:
        
        ###generate README with non-fields properties ### 
        for path in csvpaths:
            schema = Schema(str(path).replace("csvs","schemas").replace(".csv",".json")).to_dict()
            del schema["fields"]
            schema = {name:(",\n".join(item) if isinstance(item,list) else item) for name,item in schema.items()}
            schema['name'] = path.stem
            schemasheet.append(schema)

        schemasheetdf = pd.DataFrame(schemasheet)
        cols = ['name','description']
        cols.extend([c for c in schemasheetdf.columns if not c in cols])
        schemasheetdf[cols].to_excel(writer,sheet_name="README")
        # wrap text of all cells
        worksheet = writer.sheets["README"]
        for row in worksheet.iter_rows(min_row=1, max_col=worksheet.max_column, max_row=len(schemasheetdf)):
            for cell in row:
                cell.alignment = cell.alignment.copy(wrap_text=True)
        _increase_colwidth(schemasheetdf, worksheet)

        #### add the table schema csvs as sheets or as one combined sheet ###
        if separate_sheets:
            for path in csvpaths:
                df = pd.read_csv(path)
                df.to_excel(writer,sheet_name=path.stem,index=False)
                # style sheet
                worksheet = writer.sheets[path.stem]
                _format_headers(worksheet)
                _increase_colwidth(df, worksheet)
        else:

                df = pd.concat([pd.read_csv(path).assign(schema=path.stem) for path in csvpaths])
                df.to_excel(writer,sheet_name="schemas",index=False)
                # style sheet
                worksheet = writer.sheets["schemas"]
                _format_headers(worksheet)
                _increase_colwidth(df, worksheet)



    