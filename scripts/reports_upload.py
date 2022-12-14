import csv
import requests
import pandas as pd
import json


df = pd.read_csv('../data/all_df.csv', encoding='utf-8', sep=',')
sellers = df['Контрагент'].unique()
brands = df['ТМ'].unique()
report_type = df['Тип'].unique()
#print(df)


sellers_d = requests.get('http://127.0.0.1:8000/api/sellers/?format=json').json()
sellers_dict = dict((elem['name'], elem['id']) for elem in sellers_d)

for elem in sellers:
    if elem not in sellers_dict.values():
        requests.post('http://127.0.0.1:8000/api/sellers/?format=json', data={'name': elem})


brands_d = requests.get('http://127.0.0.1:8000/api/brands/?format=json').json()
brands_dict = dict((elem['name'], elem['id']) for elem in brands_d)

for elem in brands:
    if elem not in brands_dict.values():
        requests.post('http://127.0.0.1:8000/api/brands/?format=json', data={'name': elem})


report_type_d = requests.get('http://127.0.0.1:8000/api/report-types/?format=json').json()
report_type_dict = dict((elem['name'], elem['id']) for elem in report_type_d)

for elem in report_type:
    if elem not in report_type_dict.values():
        requests.post('http://127.0.0.1:8000/api/report-types/?format=json', data={'name': elem})


reports_d = json.loads(json.dumps(list(df.T.to_dict().values())))
sellers_d = requests.get('http://127.0.0.1:8000/api/sellers/?format=json').json()
sellers_dict = dict((elem['name'], elem['id']) for elem in sellers_d)

brands_d = requests.get('http://127.0.0.1:8000/api/brands/?format=json').json()
brands_dict = dict((elem['name'], elem['id']) for elem in brands_d)

report_type_d = requests.get('http://127.0.0.1:8000/api/report-types/?format=json').json()
report_type_dict = dict((elem['name'], elem['id']) for elem in report_type_d)

for elem in reports_d:
    # print(elem, elem.get('Контрагент'))
    for key_elem in sellers_dict.keys():
        # print(key_elem)
        if elem.get('Контрагент') == key_elem:
            # print(elem, elem.get('Контрагент'))
            elem['Контрагент'] = sellers_dict.get(key_elem)
            # print(sellers_dict.get('key_elem'))


for elem in reports_d:
    # print(elem, elem.get('ТМ'))
    for key_elem in brands_dict.keys():
        # print(key_elem)
        if elem.get('ТМ') == key_elem:
            # print(elem, elem.get('ТМ'))
            elem['ТМ'] = brands_dict.get(key_elem)
            # print(brands_dict.get('key_elem'))


for elem in reports_d:
    # print(elem, elem.get('Тип'))
    for key_elem in report_type_dict.keys():
        # print(key_elem)
        if elem.get('Тип') == key_elem:
            # print(elem, elem.get('Тип'))
            elem['Тип'] = report_type_dict.get(key_elem)
            # print(report_type_dict.get('key_elem'))

# print(reports_d)

# report_dict1 = requests.get('http://127.0.0.1:8000/api/reports/?format=json').json()

for elem in reports_d:
    d = elem.get('Период')
    s = elem.get('Контрагент')
    b = elem.get('ТМ')
    rt = elem.get('Тип')
    t, m = elem.get('Стоимость'), elem.get('Валовый Доход')
    if len(requests.get(f'http://127.0.0.1:8000/api/reports/?format=json&seller={s}&brand={b}&date={d}&report_type={rt}').json()):
        requests.put(f'http://127.0.0.1:8000/api/reports/?format=json&seller={s}&brand={b}&date={d}&report_type={rt}',
                     data={'turnover': t, 'margin': m})

    requests.post('http://127.0.0.1:8000/api/reports/?format=json',
                  data={'date': d, 'seller': s, 'brand': b, 'turnover': t, 'margin': m, 'report type': rt})
print(requests.get('http://127.0.0.1:8000/api/reports/?format=json&seller'))




# with open('plan.csv', 'r', encoding='utf-8') as f:
#     reader = list(csv.reader(f))
#     for row in reader[1:]:
#         d, s, b, t, m, rt = row[0], row[1], row[2], row[3], row[4], row[5]
#         requests.post('http://127.0.0.1:8000/api/reports/?format=json', data={'Date':d, 'Seller':s, 'Brand':b, 'Turnover':t, 'Margin':m, 'Report type':rt})



# req = requests.get('http://127.0.0.1:8000/api/sellers/?format=json')
# sellers = req.json()
# sellers_dict = dict((elem['name'], elem['id']) for elem in sellers)
# print(sellers_dict)
# requests.post('http://127.0.0.1:8000/api/sellers/?format=json', data = {'name':'sssaaaa'})
# print(req.json())
# requests.delete('http://127.0.0.1:8000/api/sellers/4/?format=json', data={'name':'sssaaaa'})
# requests.put('http://127.0.0.1:8000/api/sellers/1/?format=json', data={'name':'dddd'})
# print(requests.get('http://127.0.0.1:8000/api/sellers/?format=json').json())


from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)