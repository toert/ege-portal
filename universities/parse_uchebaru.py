import re
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from universities.parse_graduate import parse_all_university_data, try_reconnect, fetch_universities_list

SEARCH_URL = 'https://{domain}.ucheba.ru/for-abiturients/vuz?eq[0]=__s:{query}'


def parse_specialties(codes_amount, level='03'):
    specialties_groups = {}
    for specialty_code in range(1, codes_amount+1):
        soup = fetch_soup('https://postupi.online/specialnosti/{}.{}.00/'.format(specialty_code, level))
        name = soup.find('div', {'class':'logo_header_inner'})\
            .find('span').text\
            .replace(' - специальности вузов: направления подготовки бакалавриата', '')
        programs = [header.find('a').text for header in soup.find_all('h2', {'class': 'h2_prog'})]

        specialties_groups[specialty_code] = {}
        specialties_groups[specialty_code]['name'] = name
        specialties_groups[specialty_code]['programs'] = programs
    pprint(specialties_groups)
    return specialties_groups


@try_reconnect
def fetch_soup(url, **kwargs):
    page = requests.get(url, params=kwargs)
    print(page.url)
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


def fetch_program_list_from_ucheba(domain, university_id):
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
    ege_exams = re.sub(r' +\(\w+\)', '', ege_exams_as_string).replace('Английский язык', 'Иностранный язык')
    custom_exams = custom_exams_as_string
    return {'ege': ege_exams.split(', '),
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


def union_programs_from_ucheba_and_graduate(ucheba_program, graduate_programs, specialties):
    soup = fetch_soup(ucheba_program['url'])
    program_info = collect_program_info(soup)
    program_info['ucheba_url'] = ucheba_program['url']
    program_info['faculty'] = ucheba_program['faculty']
    program_salary = [salary for salary in graduate_programs if salary['name'] == program_info['common_name']] \
                     or [salary for salary in graduate_programs if salary['name'] == program_info['full_name']]
    if not program_salary:
        try:
            program_info = {**program_info, **find_specialty_group(program_info['common_name'], specialties)}
        except TypeError:
            return program_info
        group = find_specialty_group(program_info['common_name'], specialties)
        program_salary = [salary for salary in graduate_programs if salary['name'] == group['group_name']]
        if not program_salary:
            return program_info
    return {**program_info, **program_salary[0]}


def find_specialty_group(specialty_name, all_specialties):
    print(specialty_name)
    for code, data in all_specialties.items():
        if specialty_name not in data['programs']:
            continue
        return {'code_prefix': code,
                'group_name': [name for name in data['programs'] if name == specialty_name][0]}


def add_specialty(name, filepath='specialties.json'):
    code = input('Code:')
    all_specialties = file_to_dict(filepath)
    pprint(all_specialties)
    all_specialties[code]['programs'].append(name)
    dict_to_file(all_specialties, filepath)


def main():
    universities = []
    city = 'moscow'
    collations = file_to_dict(city + '.json')
    specialties = file_to_dict('data/all_specialties.json')
    for collation in collations:
        if collation['ucheba_url'] is None:
            continue

        graduate_university_info = parse_all_university_data(collation['graduate_id'])
        if graduate_university_info is None:
            continue

        print('Start new University')
        graduate_university_info['ucheba_url'] = collation['ucheba_url']
        print(collation['ucheba_url'])
        domain, id = extract_id_from_url(collation['ucheba_url'])
        ucheba_programs = fetch_program_list_from_ucheba(domain, id)
        unioned_programs = []

        for program in ucheba_programs:
            unioned_programs.append(
                union_programs_from_ucheba_and_graduate(program, graduate_university_info['programs'], specialties)
            )
        graduate_university_info['programs'] = unioned_programs
        pprint(graduate_university_info)
        universities.append(graduate_university_info)
    dict_to_file(universities, 'data/test_{}.json'.format(city))


def auto_collate_universities(graduate_universities, domain):
    print(len(graduate_universities))
    collated = []
    for university in graduate_universities:
        soup = fetch_soup(SEARCH_URL.format(domain=domain,
                                     query=university['name']))
        titles = soup.find_all('h2', {'class':'search-results-title'})
        if len(titles) == 1:
            href = titles[0].find('a', href=True)['href']
        elif len(titles) > 1:
            same_title = [title for title in titles if title.find('a').text == university['name']]
            if same_title:
                href = same_title[0].find('a', href=True)['href']
            else:
                print('________')
                print(university['name'], ':')
                for num, title in enumerate(titles):
                    print(num+1, title.find('a').text)
                choice = input('Your:')
                if choice == 'q':
                    continue
                href = titles[int(choice)-1].find('a', href=True)['href']
        elif len(titles) < 1:
            print('not found {}'.format(university['name']))
            href = input('Enter:')
        collated.append({'graduate_id': university['id'],
                         'ucheba_url': 'https://{}.ucheba.ru{}'.format(domain, href)})
    return collated


if __name__ == '__main__':
    main()
    # done = file_to_dict('auto_spb.json')
    # done_universities_id = [pair['graduate_id'] for pair in done if pair['ucheba_url']]
    # #done_universities_id = []
    # universities = fetch_universities_list()['data']
    # pprint(universities)
    # collated = auto_collate_universities([univer for univer in universities if univer['region_id'] == '40'
    #                            and univer['id'] not in done_universities_id and univer['type_id']=='1'], 'spb')
    # dict_to_file(collated.extend(done), 'auto_spb.json')
