import json
import csv
import sys
import io
import os
import ast

from goodtables import validate,check,Error

valid_zips = ['19102', '19103', '19104', '19106', '19107', '19109', '19111', '19112', '19114', '19115', '19116', '19118', '19119', '19120', '19121', '19122', '19123', '19124', '19125', '19126', '19127', '19128', '19129', '19130', '19131', '19132', '19133', '19134', '19135', '19136', '19137', '19138', '19139', '19140', '19141', '19142', '19143', '19144', '19145', '19146', '19147', '19148', '19149', '19150', '19151', '19152', '19153', '19154']
valid_tracts = ['94', '95', '96', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '152', '153', '156', '190', '191', '192', '197', '198', '199', '200', '202', '203', '204', '205', '206', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '29', '31', '50', '54', '55', '56', '60', '61', '62', '63', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '157', '158', '160', '161','162', '163', '164', '165', '166', '168', '39.01', '169.02', '169.01', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '241', '242', '243', '244', '245', '246', '247', '248', '249', '252', '253', '254', '255', '256', '283', '284', '285', '286', '287', '288', '290', '291', '292', '293', '294', '298', '333', '334', '335', '336', '338', '339', '340', '341', '342', '9802', '344', '346', '64', '65', '66', '363.01', '364', '366', '348.03', '347.02', '362.02', '38', '83.02', '176.02', '10.02', '10.01', '4.02', '4.01', '122.04', '122.03', '136.02', '345.01', '345.02', '11.02', '9.02', '9.01', '172.01', '172.02', '274.01', '201.01', '201.02', '311.01', '311.02', '195.02', '195.01', '289.01', '289.02', '331.01', '331.02', '315.01', '305.01', '305.02', '98.02', '180.01', '177.02', '177.01', '356.02', '357.01', '357.02', '356.01', '151.01', '151.02', '365.01', '9804', '134.02', '134.01', '136.01', '379', '382', '380', '381', '384', '1', '2', '3', '5', '6', '7', '32', '33', '36', '37.01', '37.02', '41.01', '40.02', '39.02', '40.01', '41.02', '42.02', '42.01', '79', '80', '82', '176.01', '83.01', '84', '85', '90', '91', '92', '93', '67', '69', '70', '72', '73', '74', '77', '78', '115', '117', '118', '119', '120', '121', '125', '131', '132', '133', '135', '137', '170', '171', '173', '174', '175', '178', '179', '183', '184', '188', '217', '218', '219', '220', '9801', '231', '235', '236', '237', '238', '239', '240', '257', '258', '259', '260', '261', '262', '348.01', '263.02', '264', '265', '266', '267', '268', '299', '300', '301', '302', '306', '307', '308', '309', '310', '312', '313', '316', '317', '363.03', '347.01', '348.02', '349', '351', '352', '353.01', '263.01', '8.04', '12.02', '12.01', '8.03', '9809', '27.02', '30.02', '30.01', '28.02', '9807', '27.01', '9806', '337.01', '337.02', '315.02', '314.01', '314.02', '167.01', '167.02', '279.01', '279.02', '81.01', '71.02', '88.02', '87.02', '87.01', '81.02', '86.02', '375', '9808', '180.02', '88.01', '122.01', '98.01', '71.01', '28.01', '9805', '8.01', '11.01', '274.02', '86.01', '365.02', '367', '376', '386', '385', '387', '388', '389', '9800', '269', '270', '271', '272', '273', '275', '276', '277', '278', '280', '281', '282', '318', '319', '320', '321', '323', '325', '326', '9891', '329', '330', '332', '9803', '355', '358', '359', '360', '361', '362.03', '353.02', '362.01', '363.02', '369', '373', '372', '383', '390', '378', '377']


def validation(csv,cust):
    report = validate(csv)
    if not report['valid']:
        for table in report['tables']:
            s = ast.literal_eval(table['datapackage'])
            filename = s['name'] + "_error_dump.txt"
            with open(filename,'w',) as fp:
                for error in table['errors']:
                    row = error['row-number']
                    col = error['column-number']
                    err_str = error['message']
                    for err in cust:
                        if col in err['columns']:
                            err_str = err_str[:err_str.find("\"",err_str.find("\"")+1,)+1]
                            err_str = err_str + " in row " + str(row) + " and column " + str(col) + err['message']
                    fp.write(err_str + "\n")


if len(sys.argv) > 1:
    file_name = sys.argv[1]
    config_file = sys.argv[2]
    schema = {}
    custom_error = [{'name': 'phil_zip', 'columns': [], 'message': ' is not a Philadelphia zip code.'},{'name': 'phil_tract', 'columns': [], 'message': ' is not a Philadelphia Census Tract.'},{'name': 'lat', 'columns': [], 'message': ' is not a latitude near Philadelphia.'},{'name': 'lon', 'columns': [], 'message': ' is not a longitude near Philadelphia.'}]
    col_count = 1
    with open(config_file, 'r') as fp:
        schema = json.load(fp)
        for field in schema['fields']:
            if 'constraints' in field:
                if 'custom' in field['constraints']:
                    custom = field['constraints']['custom']
                    if custom == 'phil_zip': # phil_zip refers to any Philadelphia zip code
                        del field['constraints']['custom']
                        field['constraints']['enum'] = valid_zips
                        custom_error[0]['columns'].append(col_count)
                    elif custom == 'phil_tract': # phil_tract refers to any valid Philadelphia Census Tract
                        del field['constraints']['custom']
                        field['constraints']['enum'] = valid_tracts
                        custom_error[1]['columns'].append(col_count)
                    elif custom == 'lat': # lat refers to any latitude that -could- be in and around Philadelphia
                        del field['constraints']['custom']
                        field['constraints']['minimum'] = 38
                        field['constraints']['maximum'] = 42
                        custom_error[2]['columns'].append(col_count)
                    elif custom == 'lon': # lon refers to any longitude that -could- be in and around Philadelphia
                        del field['constraints']['custom']
                        field['constraints']['minimum'] = 73
                        field['constraints']['maximum'] = 77
                        custom_error[3]['columns'].append(col_count)
            col_count = col_count + 1

    filename, file_extension = os.path.splitext(file_name)
    data_package_json = { "name": filename, "title": filename, "resources": [{"name": filename, "path": file_name, "schema": schema}]}
    # The csv and schema must be loaded together into a datapackage for use with goodtables
    if file_extension == '.csv':
        validation(data_package_json,custom_error)
