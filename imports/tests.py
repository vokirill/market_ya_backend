from django.test import TestCase
import json

# Create your tests here.
from imports.models import Imports

class ImportsTest(TestCase):

    def test_upload_treatments_valid_data(self):
        data = {
        'citizens': [{
            'citizen_id': 1,
            'town': 'Москва',
            'street': 'Ленинский проспект',
            'building': '1к5стр6',
            'apartment': 7,
            'name': 'Пупкин Иван Петрович',
            'birth_date': '05.02.2001',
            'gender': 'male',
            'relatives': [2],
        },
        {
            'citizen_id': 2,
            'town': 'Зажопинск',
            'street': 'Ленинский проспект',
            'building': '2к6',
            'apartment': 7,
            'name': 'Пискосистыq Сидор Сидорович',
            'birth_date': '05.02.1965',
            'gender': 'male',
            'relatives': [1,3],
        },
        {
            'citizen_id': 3,
            'town': 'Пердюльск',
            'street': 'Пьяных октябрят',
            'building': '2к6',
            'apartment': 10,
            'name': 'Бдышь Адольф Иванович',
            'birth_date': '05.03.1980',
            'gender': 'male',
            'relatives': [2],
        },
        ]}

        response = self.client.post('/imports', json.dumps(data), content_type="application/json")

        import_id_ = Imports.objects.get_max_import_id()['import_id__max']

        good_response = {
        "data":{
            "import_id": import_id_
            }
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)