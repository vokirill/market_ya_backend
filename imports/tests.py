from django.test import TestCase
import json

# Create your tests here.
from imports.models import Imports

class ImportsTest(TestCase):
    maxDiff = None
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

    def test_upload_treatments_presence_of_all_data(self):
        data = {
            'citizens': [{
                'citizen_id': 1,
                'street': 'Ленинский проспект',
                'building': '1к5стр6',
                'apartment': 7,
                'name': 'Пупкин Иван Петрович',
                'birth_date': '05.02.2001',
                'gender': 'male',
                'relatives': [2],
            },
            ]}
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        good_response = {'errors': "'town' is a required property"}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

    def test_upload_treatments_unique_citizen_id(self):
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
                'relatives': [],
            },
            {
                'citizen_id': 1,
                'town': 'Зажопинск',
                'street': 'Ленинский проспект',
                'building': '2к6',
                'apartment': 7,
                'name': 'Пискосистыq Сидор Сидорович',
                'birth_date': '05.02.1965',
                'gender': 'male',
                'relatives': [],
            },
        ]}
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        good_response = {'errors': 'bad relatives or citizen_id dependencies'}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

    def test_upload_treatments_birth_day(self):
        #  wrong date string
        data = {
            'citizens': [{
                'citizen_id': 1,
                'town': 'Москва',
                'street': 'Ленинский проспект',
                'building': '1к5стр6',
                'apartment': 7,
                'name': 'Пупкин Иван Петрович',
                'birth_date': 'some_wrong_string',
                'gender': 'male',
                'relatives': [],
            },
            ]}
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        good_response = {'errors': "'some_wrong_string' does not match " "'^(0?[1-9]|[12][0-9]|3[01]).(0?[1-9]|1[012]).\\\\d{4}$'"}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)
        # wrong date
        data = {
            'citizens': [{
                'citizen_id': 1,
                'town': 'Москва',
                'street': 'Ленинский проспект',
                'building': '1к5стр6',
                'apartment': 7,
                'name': 'Пупкин Иван Петрович',
                'birth_date': '31.02.2018',
                'gender': 'male',
                'relatives': [],
            },
            ]}
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        good_response = {'errors': 'wrong date 31.02.2018'}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

    def test_upload_treatments_gender(self):
        data = {
            'citizens': [{
                'citizen_id': 1,
                'town': 'Москва',
                'street': 'Ленинский проспект',
                'building': '1к5стр6',
                'apartment': 7,
                'name': 'Пупкин Иван Петрович',
                'birth_date': '25.02.2018',
                'gender': 'elefant',
                'relatives': [],
            },
            ]}
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        good_response = {'errors': "'elefant' is not one of ['male', 'female']"}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

    def test_upload_treatments_realtive_realtion_validation(self):
        #right_values
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
                'relatives': [2,3,4],
            },
                {
                    'citizen_id': 2,
                    'town': 'Зажопинск',
                    'street': 'Ленинский проспект',
                    'building': '2к6',
                    'apartment': 7,
                    'name': 'Пискосисты Сидор Сидорович',
                    'birth_date': '05.02.1965',
                    'gender': 'male',
                    'relatives': [1,5],
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
                    'relatives': [4,1],
                },
                {
                    'citizen_id': 4,
                    'town': 'Пердюльск',
                    'street': 'Пьяных октябрят',
                    'building': '2к6',
                    'apartment': 10,
                    'name': 'Бдышь Адольф Иванович',
                    'birth_date': '05.04.1980',
                    'gender': 'male',
                    'relatives': [3,6,1],
                },
                {
                    'citizen_id': 5,
                    'town': 'Пердюльск',
                    'street': 'Пьяных октябрят',
                    'building': '2к6',
                    'apartment': 10,
                    'name': 'Бдышь Адольф Иванович',
                    'birth_date': '05.05.1980',
                    'gender': 'male',
                    'relatives': [6,2],
                },
                {
                    'citizen_id': 6,
                    'town': 'Пердюльск',
                    'street': 'Пьяных октябрят',
                    'building': '2к6',
                    'apartment': 10,
                    'name': 'Бдышь Адольф Иванович',
                    'birth_date': '05.06.1980',
                    'gender': 'male',
                    'relatives': [5,4],
                },
            ]
        }
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        import_id_ = Imports.objects.get_max_import_id()['import_id__max']

        good_response = {
            "data": {
                "import_id": import_id_
            }
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

        # wrong data_format
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
                    'name': 'Пискосисты Сидор Сидорович',
                    'birth_date': '05.02.1965',
                    'gender': 'male',
                    'relatives': '1,3',
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

            ]
        }
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        good_response = {'errors': "'1,3' is not of type 'array'"}
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

        #wrong relations between
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
                'relatives': [1],
            },
            {
                'citizen_id': 2,
                'town': 'Зажопинск',
                'street': 'Ленинский проспект',
                'building': '2к6',
                'apartment': 7,
                'name': 'Пискосисты Сидор Сидорович',
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
            ]
        }
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        good_response = {'errors': 'bad relatives or citizen_id dependencies'}
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

    #Add some excced data
    def test_upload_treatments_excceed_data(self):
        data = {
            'citizens': [{
                'citizen_id': 1,
                'town': 'Москва',
                'street': 'Ленинский проспект',
                'some_wrong_field':'some_wrong_date',
                'building': '1к5стр6',
                'apartment': 7,
                'name': 'Пупкин Иван Петрович',
                'birth_date': '05.02.2001',
                'gender': 'male',
                'relatives': [],
            },
            ]
        }
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        good_response = {'errors': "Additional properties are not allowed ('some_wrong_field' was " 'unexpected)'}
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

    def test_upload_treatments_increment_import_id(self):
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
                'relatives': [],
            },
            ]
        }
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        import_id_ = Imports.objects.get_max_import_id()['import_id__max']
        self.assertEqual(import_id_, 1)
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        import_id_ = Imports.objects.get_max_import_id()['import_id__max']
        self.assertEqual(import_id_, 2)
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        import_id_ = Imports.objects.get_max_import_id()['import_id__max']
        self.assertEqual(import_id_, 3)

    def test_normal_patch(self):
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
                'name': 'Пискосистый Сидор Сидорович',
                'birth_date': '05.02.1965',
                'gender': 'male',
                'relatives': [1, 3],
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
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)


        patch_data = {
            'town': 'Москва',
            'street': 'улица',
        }
        response = self.client.patch('/imports/1/citizens/2', json.dumps(patch_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        good_response = {
            "data": {
                'citizen_id': 2,
                'town': 'Москва',
                'street': 'улица',
                'building': '2к6',
                'apartment': 7,
                'name': 'Пискосистый Сидор Сидорович',
                'birth_date': '05.02.1965',
                'gender': 'male',
                'relatives': [1, 3],
            }
        }
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)
        patch_data = {
            'town': '',
            'street': 1,
        }
        response = self.client.patch('/imports/1/citizens/2', json.dumps(patch_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        good_response = {'errors': "'' is too short"}
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

        patch_data = {
            'relatives': [3],
        }
        response = self.client.patch('/imports/1/citizens/2', json.dumps(patch_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        good_response = {
            "data": {
                'citizen_id': 2,
                'town': 'Москва',
                'street': 'улица',
                'building': '2к6',
                'apartment': 7,
                'name': 'Пискосистый Сидор Сидорович',
                'birth_date': '05.02.1965',
                'gender': 'male',
                'relatives': [3],
            }
        }
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)
        #test_changes in other rows
        other_citizens = Imports.objects.get_data_for_patch_relatives(imports_id=1).values('relatives')
        answer = [{'relatives': ''}, {'relatives': '3'}, {'relatives': '2'}]
        self.assertEqual(list(other_citizens), answer)

        patch_data = {
            'relatives': [1,3],
        }
        response = self.client.patch('/imports/1/citizens/2', json.dumps(patch_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        good_response = {
            "data": {
                'citizen_id': 2,
                'town': 'Москва',
                'street': 'улица',
                'building': '2к6',
                'apartment': 7,
                'name': 'Пискосистый Сидор Сидорович',
                'birth_date': '05.02.1965',
                'gender': 'male',
                'relatives': [1,3],
            }
        }
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)
        other_citizens = Imports.objects.get_data_for_patch_relatives(imports_id=1).values('relatives')
        answer = [{'relatives': '2'}, {'relatives': '1,3'}, {'relatives': '2'}]
        self.assertEqual(list(other_citizens), answer)

        patch_data = {
            'town': None,
        }
        response = self.client.patch('/imports/1/citizens/2', json.dumps(patch_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_imports(self):
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
                'name': 'Пискосистый Сидор Сидорович',
                'birth_date': '05.02.1965',
                'gender': 'male',
                'relatives': [1, 3],
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
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")

        response = self.client.get('/imports/1/citizens')
        self.assertEqual(response.status_code, 200)
        good_response =  {
            'data': [{
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
                'name': 'Пискосистый Сидор Сидорович',
                'birth_date': '05.02.1965',
                'gender': 'male',
                'relatives': [1, 3],
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
        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

    def test_birth_date(self):
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
                'relatives': [2,3,4],
            },
            {
                'citizen_id': 2,
                'town': 'Зажопинск',
                'street': 'Ленинский проспект',
                'building': '2к6',
                'apartment': 7,
                'name': 'Пискосистый Сидор Сидорович',
                'birth_date': '05.03.1965',
                'gender': 'male',
                'relatives': [1, 5],
            },
            {
                'citizen_id': 3,
                'town': 'Пердюльск',
                'street': 'Пьяных октябрят',
                'building': '2к6',
                'apartment': 10,
                'name': 'Бдышь Адольф Иванович',
                'birth_date': '05.04.1980',
                'gender': 'male',
                'relatives': [4,1],
            },
                {
                    'citizen_id': 4,
                    'town': 'Пердюльск',
                    'street': 'Пьяных октябрят',
                    'building': '2к6',
                    'apartment': 10,
                    'name': 'Бдышь Адольф Иванович',
                    'birth_date': '05.10.1980',
                    'gender': 'male',
                    'relatives': [3,6,1],
                },
                {
                    'citizen_id': 5,
                    'town': 'Пердюльск',
                    'street': 'Пьяных октябрят',
                    'building': '2к6',
                    'apartment': 10,
                    'name': 'Бдышь Адольф Иванович',
                    'birth_date': '05.02.1980',
                    'gender': 'male',
                    'relatives': [6,2],
                },
                {
                    'citizen_id': 6,
                    'town': 'Пердюльск',
                    'street': 'Пьяных октябрят',
                    'building': '2к6',
                    'apartment': 10,
                    'name': 'Бдышь Адольф Иванович',
                    'birth_date': '05.02.1980',
                    'gender': 'male',
                    'relatives': [5,4],
                },
            ]}

        response = self.client.post('/imports', json.dumps(data), content_type="application/json")
        response = self.client.post('/imports', json.dumps(data), content_type="application/json")

        response = self.client.get('/imports/1/citizens/birthdays')
        good_response = {"data":
                             {"1": [],
                              "2": [{"citizen_id": 2, "presents": 2},
                                    {"citizen_id": 3, "presents": 1},
                                    {"citizen_id": 4, "presents": 2},
                                    {"citizen_id": 5, "presents": 1},
                                    {"citizen_id": 6, "presents": 1}],
                              "3": [{"citizen_id": 1, "presents": 1},
                                    {"citizen_id": 5, "presents": 1}],
                              "4": [{"citizen_id": 1, "presents": 1},
                                    {"citizen_id": 4, "presents": 1}],
                              "5": [],
                              "6": [],
                              "7": [],
                              "8": [],
                              "9": [],
                              "10": [{"citizen_id": 1, "presents": 1},
                                     {"citizen_id": 3, "presents": 1},
                                     {"citizen_id": 6, "presents": 1}],
                              "11": [],
                              "12": []}}

        self.assertEqual(json.loads(response.content.decode('utf-8')), good_response)

    def test_percentile(self):
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
                    'town': 'Москва',
                    'street': 'Ленинский проспект',
                    'building': '2к6',
                    'apartment': 7,
                    'name': 'Пискосистый Сидор Сидорович',
                    'birth_date': '05.03.1965',
                    'gender': 'male',
                    'relatives': [1],
                },
                {
                    'citizen_id': 3,
                    'town': 'Москва',
                    'street': 'Пьяных октябрят',
                    'building': '2к6',
                    'apartment': 10,
                    'name': 'Бдышь Адольф Иванович',
                    'birth_date': '05.04.1980',
                    'gender': 'male',
                    'relatives': [4],
                },
                {
                    'citizen_id': 4,
                    'town': 'Москва',
                    'street': 'Пьяных октябрят',
                    'building': '2к6',
                    'apartment': 10,
                    'name': 'Бдышь Адольф Иванович',
                    'birth_date': '05.10.1980',
                    'gender': 'male',
                    'relatives': [3],
                },
            ]}

        response = self.client.post('/imports', json.dumps(data), content_type="application/json")

        response = self.client.get('/imports/1/citizens')
        self.assertEqual(response.status_code, 200)





