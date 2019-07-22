# -*- coding: utf-8 -*-
import requests
import json
'''
data_ = {
    'citizens': [{
        'citizen_id': 1,
        'town': 'Москва',
        'street': 'Ленинский проспект',
        'building': '1к5стр6',
        'appartment': 7,
        'name': 'Пупкин Иван Петрович',
        'birth_date': '2000-10-05',
        'gender': 'male',
        'relatives': [2,3],
    },
    ]
}

print(data_['citizens'])
data_ = json.dumps(data_, ensure_ascii=False)
r = requests.post('http://127.0.0.1:8000/imports/', data=data_.encode('utf-8'))
print(r.text)
'''
data_ = {
    'town': 'Керчь',
    'street': 'Гоголя'
}
data_ = json.dumps(data_, ensure_ascii=False)

r = requests.patch('http://127.0.0.1:8000/imports/6/citizens/1/', data = data_.encode('utf-8'))
print(r.text)