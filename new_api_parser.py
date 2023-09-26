import requests
import json

import pandas as pd
import sqlite3

con = sqlite3.connect("adata_sqlite_erd.db")
cursor = con.cursor()




def parser():

    url = 'https://xarid-api-trade.uzex.uz/Lib/GetDishonestSuppliers'
    headers = {
        'accept' : 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    payload = {
        'from' : 1,
        'to' : 100,
        'keyword': ""
    }
    response_API = requests.request("POST", url=url, json=payload, headers=headers)
    table = []

    for items in response_API.json():
        table.append({
            'ID': items.get('rn'),
            'Organization_name': items.get('resident_name'),
            'Full_name': items.get('name'),
            'Territory': items.get('region_name').replace('\n', ''),
            'IIN': items.get('resident_inn'),
            'Court_decision': items.get('court_decision_id').replace('\n', ''),
            "Registration_date": items.get('date_becoming_dishonest').replace('T00:00:00', ''),
            "Deregistration_date": items.get('date_ending_dishonest').replace('T00:00:00', '')})
    results = pd.DataFrame(table, columns=['ID', 'Organization_name', 'Full_name', 'Territory', 'IIN', 'Court_decision',
                               'Registration_date', 'Deregistration_date' ])
    return results.to_sql('API_table_1', con, if_exists='replace', index=False)

if __name__ == "__main__":
    (parser())
