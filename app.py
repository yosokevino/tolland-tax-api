from flask import *
import pyodbc
from credentials import Creds
#import collections

creds = Creds()

def query_data(query):
    conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}',
        server = creds['server'],
        database = creds['database'],
        uid = creds['uid'],
        pwd= creds['pwd'])

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    objects_list = []

    for row in rows:
        
        #d = collections.OrderedDict()
        d = {}
        
        d["url"] = row[0]
        d["year"] = row[1]
        d["count"] = row[2]
        d["unique_id"] = row[3]
        d["bill_number"] = row[4]
        d["gross_asessment"] = row[5]
        d["exemptions"] = row[7]
        d["district"] = row[8]
        d["net_assessment"] = row[9]
        d["name"] = row[10]
        d["town_mil_rate"] = row[11]
        d["care_of"] = row[12]
        d["address"] = row[13]
        d["property_location"] = row[14]
        d["mbl"] = row[15]
        d["town_benefit"] = row[16]
        d["volume_page"] = row[17]
        d["elderly_benefit"] = row[18]
        d["installment_01_due_date"] = row[19]
        d["installment_01_amount"] = row[20]
        d["installment_02_due_date"] = row[21]
        d["installment_02_amount"] = row[22]
        d["installment_03_due_date"] = row[23]
        d["installment_03_amount"] = row[24]
        d["installment_04_due_date"] = row[25]
        d["installment_04_amount"] = row[26]
        d["adjustment"] = row[27]
        d["total"] = row[28]
        d["total_payments"] = row[29]
        d["tax_princ_bint_due"] = row[30]
        d["interest_due"] = row[31]
        d["lien_due"] = row[32]
        d["fee_due"] = row[33]
        d["total_due_now"] = row[34]
        d["payment_01_pay_date"] = row[35]
        d["payment_01_type"] = row[36]
        d["payment_01_tax_princ"] = row[37]
        d["payment_01_interest"] = row[38]
        d["payment_01_lien"] = row[39]
        d["payment_01_fee"] = row[40]
        d["payment_01_total"] = row[41]
        d["payment_02_pay_date"] = row[42]
        d["payment_02_type"] = row[43]
        d["payment_02_tax_princ"] = row[44]
        d["payment_02_interest"] = row[45]
        d["payment_02_lien"] = row[46]
        d["payment_02_fee"] = row[47]
        d["payment_02_total"] = row[48]
        d["total_due_yearly_change"] = row[49]
        d["lat"] = row[50]
        d["lon"] = row[51]
        
        objects_list.append(d)

    return objects_list

def create_query(table, args):
    query_starter = f"SELECT * FROM {table}"
    if args:
        if len(args) > 1:
            query = query_starter + ' WHERE'
            for key, value in args.items():
                query += f" [{key}] LIKE '%{value}%' AND"
            query = query[:-4]
        if len(args) == 1:
            query = query_starter + ' WHERE'
            for key, value in args.items():
                query += f" [{key}] LIKE '%{value}%'"
    else:
        query = query_starter
    return query

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def access_param():

    args = request.args.to_dict()

    data = query_data(create_query('tolland_taxes', args))

    response = jsonify({'result': data})

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    #app.run(debug = True, port=2001)
    app.run()