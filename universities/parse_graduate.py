import requests
import json
import re
from time import sleep
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


def try_reconnect(f):
    def wrapped(*args, **kwargs):
        for _ in range(3):
            try:
                return f(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                sleep(3)
    return wrapped


@try_reconnect
def fetch_universities_list():
    url = 'http://vo.graduate.edu.ru/slices/getValues'
    payload = '{"id":1}'
    headers = HEADERS
    return requests.post(url, headers=headers, data=payload).json()


@try_reconnect
def fetch_university_info(code, year):
    url = 'http://vo.graduate.edu.ru/graphs/getGraph'
    payload = UNIVERSITY_INFO_PAYLOAD_TEMPLATE.format(code=code, year=year)
    headers = HEADERS
    return requests.post(url, headers=headers, data=payload).json()


@try_reconnect
def fetch_university_programs(code):
    url = 'http://vo.graduate.edu.ru/graphs/getGraph'
    payload = {'id': 2,
               'params': {
                    'count_affiliates': False,
                    'count_attached': False,
                    'filters': {
                        'slice1': [code],
                        'slice9': ["1", "9"],
                        'slice23': ["2013", "2014", "2015"]
                    }}}
    headers = HEADERS
    return requests.post(url, headers=headers, data=json.dumps(payload)).json()


def parse_all_university_data(code):
    university_data = fetch_university_info(code, 2015)['data']['data']
    if university_data['avg_wage'] is None:
        university_data = fetch_university_info(code, 2014)['data']['data']
        if university_data['avg_wage'] is None:
            return None
    university_data['avg_wage'] = float(university_data['avg_wage']) * 1000
    university_data['working_percent'] = float(university_data['working_percent']) * 100
    university_data['continued_amount'] = int(university_data['num_continued'])/int(university_data['num_approved'])*100
    programs_data = fetch_university_programs(code)['data']['data']
    all_programs = programs_data[0]
    all_programs.extend(programs_data[1])
    university_data['programs'] = []
    for program in all_programs:
        if re.search(r'\.04\.', program['s']):
            continue
        university_data['programs'].append({
            'name': program['d'],
            'code': program['s'],
            'salary': float(program['i'][2]) * 1000,
            'employment': float(program['i'][3])
        })
    return university_data


if __name__ == '__main__':
    universities = fetch_universities_list()['data']
    for university in universities:
        university_data = fetch_university_info(university['id'], 2015)['data']['data']
        if university_data['avg_wage'] is None:
            university_data = fetch_university_info(university['id'], 2014)['data']['data']
            if university_data['avg_wage'] is None:
                continue
    pprint(universities)
    # pprint(parse_all_university_data('07B9F5809B5031B9A484F4F1525D56B4'))
    pprint(fetch_university_info('028C6D7292E60AAD7453B0799CB59FD8', 2015))
    exit()
    pprint(fetch_university_info('028C6D7292E60AAD7453B0799CB59FD8', 2015))
    universities = fetch_universities_list()
    pprint(len(universities['data']))
    #print([university for university in universities if ])
    pprint(fetch_university_programs('028C6D7292E60AAD7453B0799CB59FD8'), indent=1)
