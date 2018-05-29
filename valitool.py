import json
import csv
import sys
import io
import os

import petl as etl
import requests
from openpyxl import load_workbook
from goodtables import validate

def validation(csv):
    report = validate(csv)
    print('Hello?')
    print(report)

def philly_zip_check(tab):
    invalid_zips = []
    valid_zips = ['19102', '19103', '19104', '19106', '19107', '19109', '19111', '19112', '19114', '19115', '19116', '19118', '19119', '19120', '19121', '19122', '19123', '19124', '19125', '19126', '19127', '19128', '19129', '19130', '19131', '19132', '19133', '19134', '19135', '19136', '19137', '19138', '19139', '19140', '19141', '19142', '19143', '19144', '19145', '19146', '19147', '19148', '19149', '19150', '19151', '19152', '19153', '19154']
    if 'zip' in etl.header(tab):
        zips = etl.cut(table, 'zip')
        zip_data = etl.data(zips)
        zip_list = list(zip_data)
        row_num = 0
        for zip in zip_list:
            if zip[0] not in valid_zips:
                if not isinstance(zip, str):
                    reason = "Not a string"
                elif len(zip) > 5:
                    reason = "Too long"
                elif len(zip) < 5:
                    reason = "Too short"
                invalid_zips.append({'row': row_num, 'zip': zip[0], 'reason': reason})
            row_num = row_num + 1
        print(invalid_zips)
        if len(invalid_zips) > 0:
            return False
        else:
            return True

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    config_file = sys.argv[2]
    schema = {}

    with open(config_file, 'r') as fp:
        schema = json.load(fp)
        print(schema)
    filename, file_extension = os.path.splitext(file_name)
    data_package_json = { "name": filename, "title": filename, "resources": [{"name": filename, "path": file_name, "schema": schema}]}

    if file_extension == '.csv':
        print('???')
        table = etl.fromcsv(file_name)
        validation(data_package_json)
    elif file_extension == '.txt':
        table = etl.fromtext(file_name)
    elif file_extension == '.xml':
        table = etl.fromxml(file_name)
    elif file_extension == '.html':
        table = etl.fromhtml(file_name)
    elif file_extension == '.json' or file_extension == '.geojson':
        table = etl.fromjson(file_name)
    elif file_extension == '.xlsx':
        table = etl.fromxlsx(file_name)

    philly_zip_check(table)
