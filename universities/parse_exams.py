import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, parse_qs
import re


URL = 'http://postyplenie.ru/results_of_admission/{}/'
EXAMS_URL = 'http://postyplenie.ru/calculator.php?' \
            'Vuz={}&obzestvoznanie=100&russkiy=100&informatika=100&biologiya=100&geografiya=100' \
            '&ximiya=100&fizika=100&literatura=100&history=100&matematika=100&lang=100'


def fetch_soup(url, **kwargs):
    page = requests.get(url, params=kwargs).content
    return BeautifulSoup(page, 'html.parser')


def collect_universities_slugs_from_page(soup):
    for university_info in soup.find_all('div', {'class': 'news-vuz-item'}):
        for link in university_info.find_all('a'):
            query = urlsplit(link.get('href')).query
            params = parse_qs(query)
            yield params['CODE'][0]


def get_pages_amount(soup):
    navbar = soup.find('div', {'class': 'modern-page-navigation'})
    if navbar is None:
        return 1
    return sum([1 for a in navbar.find_all('a')]) + 1


def fetch_slugs_for_year(base_url, year):
    slugs = []
    soup = fetch_soup(base_url.format(year))
    for page_number in range(1, get_pages_amount(soup) + 1):
        if page_number != 1:
            soup = fetch_soup(base_url.format(year), PAGEN_1=page_number)
        slugs.extend(collect_universities_slugs_from_page(soup))
    return slugs


def collect_info_about_university(soup):
    info_box = soup.find('div', {'id': 'vuz_description'})
    header = info_box.find('h1').text
    name = ' '.join(word for word in header.split()[:-1])
    city = header.split()[-1]
    return {
        'name': name,
        'city': city
        # TODO add more information
    }

structure = {
    'fu': {
        'full_name': 'Финансовый',
        'site': 'www.fa.ru',
        'faculties': {
            'АРиЭБ':
                [{'code': '10.03.01',
                  'name': 'Информационная безопасность'},
                 {'code': '38.03.01',
                  'name': 'Экономика'}]
        }
    }
}

def fetch_exams(slug):
    codes_and_exams = []
    soup = fetch_soup(EXAMS_URL.format(slug))
    table = soup.find('table', {'class': 'result_table'})
    for tr in table.find_all('tr', {'class': 's'}):
        columns = tr.find_all('td')
        code = columns[1].text.replace(' ', '')
        exams = columns[2].find('div').text.split(', ')
        codes_and_exams.append((code, exams))
    return codes_and_exams


def collect_programs(soup):
    programs = []
    current_faculty = 'None'
    score_table = soup.find('div', id='param_true_ball')
    for tr in score_table.find_all('tr')[1:]:
        if tr.find('b') is not None:
            current_faculty = tr.find('b').text
            if re.match('Программы подготовки', current_faculty):
                current_faculty = None
            continue
        columns = tr.find_all('td')
        program = {'code': columns[0].text.replace('\xa0', ''),
                   'program': columns[1].text,
                   'first_score': normalize_score(columns[2].text),
                   'second_score': normalize_score(columns[-1].text),
                   'faculty': current_faculty
                   }
        program = {**program}
        programs.append(program)
    return programs


def normalize_score(score):
        if re.findall('БВИ', score):
            return 1000
        elif re.findall('целев', score):
            return 0
        else:
            return score


if __name__ == '__main__':
    years = ['2016']
    universities = {}
    programs_set = []
    for year in years:
        slugs = fetch_slugs_for_year(URL, year)
        for slug in slugs:
            print(slug)
            soup = fetch_soup(URL.format(year), CODE=slug)
            universities[slug] = collect_info_about_university(soup)
            universities[slug] = collect_programs(soup)
            try:
                codes_and_exams = fetch_exams(slug)
            except AttributeError:
                print('Fetching error')
                continue
            for program in universities[slug]:
                print([exams for code, exams in codes_and_exams if code == program['code']])
