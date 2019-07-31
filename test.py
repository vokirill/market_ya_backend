# -*- coding: utf-8 -*-
import requests
import json

data_ = {
    'citizens': [{
        'citizen_id': 1,
        'town': 'Москва',
        'street': 'Ленинский проспект',
        'building': '1к5стр6',
        'appartment': 7,
        'name': 'Пупкин Иван Петрович',
        'birth_date': '05.02.2001',
        'gender': 'male',
        'relatives': [2,3,4,5,6,7,8,9,10,11,12,13],
    },
    {
        'citizen_id': 2,
        'town': 'Зажопинск',
        'street': 'Ленинский проспект',
        'building': '2к6',
        'appartment': 7,
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
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.03.1980',
        'gender': 'male',
        'relatives': [2,5],
    },
    {
        'citizen_id': 4,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.04.1980',
        'gender': 'male',
        'relatives': [1,13],
    },
{
        'citizen_id': 5,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.05.1980',
        'gender': 'male',
        'relatives': [2,7],
    },
{
        'citizen_id': 6,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.06.1980',
        'gender': 'male',
        'relatives': [1,10],
    },
{
        'citizen_id': 7,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.07.1980',
        'gender': 'male',
        'relatives': [3,4],
    },
{
        'citizen_id': 8,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.08.1980',
        'gender': 'male',
        'relatives': [8,5],
    },
{
        'citizen_id': 9,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.09.1980',
        'gender': 'male',
        'relatives': [10,11],
    },
{
        'citizen_id': 10,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.10.1980',
        'gender': 'male',
        'relatives': [3],
    },
{
        'citizen_id': 11,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.11.1980',
        'gender': 'male',
        'relatives': [7],
    },
{
        'citizen_id': 12,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.12.1980',
        'gender': 'male',
        'relatives': [12,8],
    },
{
        'citizen_id': 13,
        'town': 'Пердюльск',
        'street': 'Пьяных октябрят',
        'building': '2к6',
        'appartment': 10,
        'name': 'Бдышь Адольф Иванович',
        'birth_date': '05.01.1980',
        'gender': 'male',
        'relatives': [6],
    },
    ]
}



data_ = json.dumps(data_, ensure_ascii=False)
r = requests.post('http://127.0.0.1:8000/imports', data=data_.encode('utf-8'))
print(r.text)
'''
data_ = {
    'town': 'Зажопинск-сити',
    'street': 'Гоголя-Моголя'
}
data_ = json.dumps(data_, ensure_ascii=False)

r = requests.patch('http://127.0.0.1:8000/imports/6/citizens/1', data = data_.encode('utf-8'))
print(r.text)


r = requests.get('http://127.0.0.1:8000/imports/13/citizens/birthdays')
print(r.text)


r = requests.get('http://127.0.0.1:8000/imports/13/towns/stat/percentile/age')
print(r.text)
'''