import json
from pprint import pprint
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from universities.models import University, Program, RequiredExam

def read_dumped_json_from_file(filepath):
    with open(filepath, 'r', encoding='UTF-8') as file:
        return json.loads(file.read())

class Command(BaseCommand):

    help = 'Add data dump about universities to DB'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Replace new universities and programs',
        )

    def handle(self, *args, **options):
        universities = read_dumped_json_from_file(options['filepath'])
        for university in universities:

            university_in_db = University.objects.filter(
                graduate_id=university['id'],
                year=settings.LAST_EGE_YEAR
            )

            if university_in_db.exists():
                university_in_db = university_in_db.first()
                if options['delete']:
                    university_in_db.delete()
                    university_in_db = self.create_university_object_from_dict(university)
            else:
                university_in_db = self.create_university_object_from_dict(university)

            for program in university['programs']:

                program_in_db = Program.objects.filter(
                    university=university_in_db,
                    full_name=program['full_name'],
                    year=settings.LAST_EGE_YEAR
                )
                if options['delete']:
                    program_in_db.delete()
                if not program_in_db.exists() and 'exams' in program:
                    program_in_db = self.create_program_object_from_dict(program, university_in_db)
                    for exam in program['exams']['ege']:
                        RequiredExam.objects.create(
                            program=program_in_db,
                            exam=[slug for slug, name in RequiredExam.EXAMS if name == exam][0]
                        )

        self.stdout.write(self.style.SUCCESS('Done!'))

    def create_university_object_from_dict(self, data):
        if data['type_id'] == '1':
            type = University.TYPE_GOVERNMENT
        elif data['type_id'] == '2':
            type = University.TYPE_MUNICIPAL
        else:
            type = University.TYPE_PRIVATE

        return University.objects.create(
            average_salary=data['avg_wage'],
            employment_percentage=data['working_percent'],
            graduate_id=data['id'],
            name=data['name'],
            region_name=data['district_name'],
            type=type,
            ucheba_url=data['ucheba_url'],
            year=settings.LAST_EGE_YEAR,
        )

    def create_program_object_from_dict(self, data, university):
        form = [slug for slug, name in Program.FORMS if name==data['form']][0]
        level = [slug for slug, name in Program.LEVELS if name == data['level']][0]
        pprint(data)
        return Program.objects.create(
            university=university,
            code=data.get('code', ''),
            common_name=data['common_name'],
            cost_per_year=data.get('cost', None),
            duration=data['duration'],
            employment_percentage=data.get('employment', None),
            custom_exam=data['exams']['custom'],
            form=form,
            full_name=data['full_name'],
            level=level,
            places=data.get('places', None),
            average_salary=data.get('salary', None),
            second_passing_score=data.get('score', None),
            ucheba_url=data['ucheba_url'],
            year=settings.LAST_EGE_YEAR
        )