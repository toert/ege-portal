import requests
import json
from pprint import pprint

HEADERS = {
        'origin': 'http://vo.graduate.edu.ru',
        'x-csrf-token': 'K4PRF1sHkX+zZiOS5GxvvuFb8GtcmUElGwLfGhL/UgR7JFx2nSjtVkg9LRjN25i2AewAPC6XPqhxAgdLUiupSQ==',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': '_ym_uid=1506167606433236470;'
                  ' _ym_isad=1; _ym_visorc_31062401=w;'
                  ' _vagrant_session=UVNxNnVBWUJQb3lqczdoZCt1VERna1ZuaE9UVWw0aUE3bG15UFN6M0RBekZOSXovc0pKaU5WYUc1Qj'
                  'loemFQR1dLYXRjcHlIdVBNeC91bnJmd2pzSHFxUFBEUENsb3I5VDNKQWMrelUwb2ZiSjNtZjI2SlZ3eXFhZytzK1JiREtvUk'
                  'RBdGxDV3NPNkF3OW1YK21nRlJRPT0tLWg3MncyUjl2NXlBQzloN240VU1mTXc9PQ%3D%3D--988513a9f2e3a5e954c4b11fd'
                  '227cb9e434e5593',
        'x-compress': 'null',
    }

UNIVERSITY_INFO_PAYLOAD_TEMPLATE = """
    {{"id":1,"params":{{"count_affiliates":false,"filters":{{"slice1":["{code}"],"slice23":[{year}]}}}}}}
"""


def fetch_universities_list():
    url = 'http://vo.graduate.edu.ru/slices/getValues'
    payload = '{"id":1}'
    headers = HEADERS
    return requests.post(url, headers=headers, data=payload).json()


def fetch_university_info(code, year):
    print(code)
    url = 'http://vo.graduate.edu.ru/graphs/getGraph'
    payload = UNIVERSITY_INFO_PAYLOAD_TEMPLATE.format(code=code, year=year)
    headers = HEADERS
    return requests.post(url, headers=headers, data=payload).json()


def fetch_university_programs(code, year):
    url = 'http://vo.graduate.edu.ru/graphs/getGraph'
    payload = {'id':2,
               'params':{
                    'count_affiliates': False,
                    'count_attached':False,
                    'filters':{
                        'slice1':[code],
                        'slice23':[str(year-1)],
                        'slice30':[str(year)]}}}
    headers = HEADERS
    return requests.post(url, headers=headers, data=json.dumps(payload)).json()


if __name__ == '__main__':
    #universities = fetch_universities_list()
    pprint(fetch_university_programs('41A3BED4AA80BB95B6A11A07624C26F0', 2016), indent=1)
