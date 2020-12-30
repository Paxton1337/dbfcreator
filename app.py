from codecs import encode
from datetime import date
import os
from flask import Flask, request
import dbf
import json
from flask.helpers import send_file, send_from_directory
from flask.templating import render_template
# import pandas as pd
from flask_cors import CORS
from whitenoise import WhiteNoise
import whitenoise
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static/')

@app.route('/')
def home():
    return "OK", 200

@app.route('/dbf', methods=['POST'])
def pyfoo():
    x = lambda val: dbf.Date(int(val[11:15]), int(val[8:10]), int(val[5:7])) if (isinstance(val, str) and val.startswith('date:')) else val
    req_body = request.get_json()
    filename = req_body['filename']
    data = req_body['data']
    # df = pd.DataFrame.from_dict(req_body['data'])
    field_specs = req_body['specs']
    # print(field_specs)
    table = dbf.Table('static/' + filename + '.dbf', field_specs, codepage='cp1251')
    # table = dbf.Table(filename + '.dbf', 'name N(1,0)', codepage='cp866')
    table.open(mode=dbf.READ_WRITE)
    for key in data:
        for index, (_key, value) in enumerate(key.items()):
            if isinstance(value, str):
                key[_key] = x(value[:28])
            else:
                print(x(value))
                key[_key] = x(value)
        table.append(key)
    table.close();
    #     print(data)
    # table.open(mode=dbf.READ_WRITE)
    # dict_sample = dict({1:'mango', 2:'pawpaw'})
    # columns = req_body['columns']
    # df = pd.read_json(data_as_string, typ='series')
    # df.columns = columns
    # df.to_csv('static/' + filename + '.csv', index = None, header=True)
    # dbf.from_csv(csvfile='static/' + filename + '.csv', to_disk=True, filename='static/' + filename + '.dbf', encoding='utf8')
    return "200", 200

@app.route('/dbf/<filename>')
def first_file(filename):
    return send_from_directory('static', filename + '.dbf', as_attachment=True)

# @app.route('/dbt/<filename>')
# def second_file(filename):
#     return send_from_directory('static', filename + '.dbt', as_attachment=True)

@app.route('/dbf/remove/<filename>')
def remove_all(filename):
    os.remove('static/' + filename + '.dbf')
#     os.remove('static/' + filename + '.dbt')
#     os.remove('static/' + filename + '.csv')
    return "Done", 200


# @app.route('/test')
# def test():
#     table = dbf.Table('test1.dbf', 'name C(30); age N(3,0); birth D')
    # table.open(mode=dbf.READ_WRITE)
#     for datum in (
#             ('John Doe', 20, '1974.09.19'),
#             ('Ethan Furman', 102, dbf.Date(1909, 4, 1)),
#             ('Jane Smith', 57, dbf.Date(1954, 7, 2)),
#             ('John Adams', 44, dbf.Date(1967, 1, 9)),
#             ):
#         table.append(datum)
# x = 'date:1979.01.12'
# print(x[5:9] + ':' + x[10:12] + ':' + x[13:])


if __name__ == "__main__":
    app.run()
