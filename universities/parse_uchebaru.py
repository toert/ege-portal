import re
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from parse_graduate import fetch_universities_list, fetch_university_info, fetch_university_programs, try_reconnect

SEARCH_URL = 'https://www.ucheba.ru/for-abiturients/vuz?eq[0]=__s:{query}'


@try_reconnect
def fetch_soup(url, **kwargs):
    page = requests.get(url, params=kwargs)
    return BeautifulSoup(page.content, 'html.parser')


def fetch_universities_by_query(query):
    soup = fetch_soup(SEARCH_URL.format(query=query))
    links = []
    for result in soup.find_all('h2', {'class': 'search-results-title'}):
        links.append(result.find('a', href=True)['href'])
    return links


def dict_to_file(data, filepath='data.json'):
    with open(filepath, 'w', encoding='UTF-8') as file:
        json.dump(data, file)


def file_to_dict(filepath):
    with open(filepath, 'r', encoding='UTF-8') as file:
        return json.loads(file.read())


def collate_universities(universities, done_universities, filepath='universities.json'):
    mapping = []
    for num, university in enumerate(universities):
        print(university['name'])
        if university['id'] in [x['graduate_id'] for x in done_universities]:
            print('Found!')
            mapping.append({
                'graduate_id': university['id'],
                'ucheba_url': [x['ucheba_url'] for x in done_universities if university['id'] == x['graduate_id']][0]
            })
            continue
        univ_url = input('URL:')
        if univ_url == 'exit':
            print('Закончили на университете №{}'.format(num))
            break
        mapping.append({
            'graduate_id': university['id'],
            'ucheba_url': univ_url or None
        })
    dict_to_file(mapping, filepath)


def extract_id_from_url(university_url):
    regex = re.search(r'uz/(\d+)', university_url)
    return university_url.replace(regex.group(0), '').replace(' ', ''), regex.group(1)


def collect_programs(soup):
    programs = []
    for program in soup.find_all('section', {'class': 'search-results-info-item'}):
        header = program.find('h3', {'class': 'search-results-title'}).find('a', href=True)
        name = header.text
        url = 'https://www.ucheba.ru' + header['href']
        faculty = program.find('h4', {'class': 'search-results-info-big'})
        raw_score = program.find('section', {'class': 'sro-point'}).find('div').text
        score = re.sub(r'[^\d\.]', '', raw_score)
        programs.append({'name': name,
                         'url': url,
                         'faculty': faculty.text if faculty is not None else None,
                         'score': float(score) if score != '' else None})
    return programs


def fetch_program_list(domain, university_id):
    url = '{domain}for-abiturients/vuz/programs/{id}?eq%5B0%5D=__u%3A{id}'.format(
        domain=domain,
        id=university_id)
    soup = fetch_soup(url)
    return collect_programs(soup)


def normalize_number(string):
    string = re.sub(r'[^\d]', '', string)
    try:
        return int(string)
    except ValueError as e:
        print(e)
        return None


def process_exam_section(divs):
    ege_exams_as_string = divs[1].text
    custom_exams_as_string = divs[3].text if len(divs) > 2 else ''
    ege_exams = ege_exams_as_string.replace(' (профильный)', '').split(', ')
    custom_exams = custom_exams_as_string
    return {'ege': ege_exams,
            'custom': custom_exams or None}


def collect_program_info(soup):
    info_table = {}
    info_table['full_name'] = soup.find('h1', {'class': 'head-announce__title'}).text
    name_and_level = soup.find('span', {'class': 'mr-10'}).text
    info_table['common_name'], info_table['level'] = name_and_level.replace('«', '').split('», ')
    table = soup.find('table', {'class': 'table-bordered'})
    rows = table.find_all('tr')
    for row in rows:
        param_name = row.find('td', {'class': 'ttf-col-1'}).text
        value_column = row.find('td', {'class': 'ttf-col-2'})
        if param_name == 'Форма обучения':
            info_table['form'] = value_column.find_all('div')[1].text
        elif param_name == 'Стоимость':
            info_table['cost'] = normalize_number(value_column.find_all('div')[1].text)
        elif param_name == 'Проходной балл':
            info_table['score'] = normalize_number(value_column.find_all('div')[1].text)
        elif param_name == 'Бюджетных мест':
            info_table['places'] = normalize_number(value_column.find_all('div')[1].text)
        elif param_name == 'Срок обучения':
            info_table['duration'] = normalize_number(value_column.find_all('div')[1].text)
        elif param_name == 'Экзамены':
            info_table['exams'] = process_exam_section(value_column.find_all('div'))
    return info_table


def parse_program_info(program):
    soup = fetch_soup(program['url'])
    print(program['url'])
    program_info = collect_program_info(soup)
    collected_programs.append(program_info)
    program_salary = [salary for salary in salary_data if salary['d'] == program_info['common_name']] \
                     or [salary for salary in salary_data if salary['d'] == program_info['full_name']]

    program_salary = program_salary[0]
    program_info['сode'] = program_salary['s']
    program_info['salary'] = float(program_salary['i'][2]) * 1000
    program_info['employment'] = float(program_salary['i'][3])
    return program_info


if __name__ == '__main__':
    programs_urls = []
    collations = file_to_dict('moscow.json')
    for collation in collations:
        if collation['ucheba_url'] is None:
            continue

        graduate_info = fetch_university_programs(collation['graduate_id'])['data']['data']
        salary_data = graduate_info[0]
        salary_data.extend(graduate_info[1])
        print('Start new University')

        domain, id = extract_id_from_url(collation['ucheba_url'])
        programs = fetch_program_list(domain, id)
        collected_programs = []

        for program in programs:
            collected_programs.append(parse_program_info(program))