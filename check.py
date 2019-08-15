# -*- coding: utf-8 -*-
import requests
import json

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



data = json.dumps(data, ensure_ascii=False)
r = requests.post('http://127.0.0.1:8000/imports', data=data.encode('utf-8'))
print(r.text)
'''
data_ = {
    'town': 'Зажопинск-сити',
    'street': 'Гоголя-Моголя'
}
'''
data = {
            'relatives': [3],
        }
data = json.dumps(data, ensure_ascii=False)

#r = requests.patch('http://127.0.0.1:8000/imports/35/citizens/2', data = data.encode('utf-8'))
#print(r.text)

#r = requests.get('http://127.0.0.1:8000/imports/30/citizens')
#print(r.text)

#r = requests.get('http://127.0.0.1:8000/imports/13/citizens/birthdays')
#print(r.text)



r = requests.get('http://127.0.0.1:8000/imports/36/towns/stat/percentile/age')
print(r.text)
import numpy as np
print(np.percentile(np.array([18,39,39, 54]), [0.5, 0.75, 0.99], interpolation='linear'))