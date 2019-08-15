import numpy as np

date_format = '%Y-%m-%d'

def datetime_to_date(date):
    if date.day<10:
        day = '0{}'.format(date.day)
    else:
        day = date.day

    if date.month<10:
        month = '0{}'.format(date.month)
    else:
        month = date.month

    return '{}.{}.{}'.format(day,month,date.year)

def relativies_validation(data):
    id_to_index = {}
    amount_of_citizens = len(data)
    matrix = np.zeros((amount_of_citizens,amount_of_citizens))
    unique_test = []
    cur_index = 0 # составляем матрицу смежности и проверяем
    for elem in data:
        unique_test.append(elem['citizen_id'])
        if elem['citizen_id'] not in id_to_index.keys():
            id_to_index[elem['citizen_id']] = cur_index
            cur_index+=1
        for relative in elem['relatives']:
            if relative not in id_to_index.keys():
                id_to_index[relative] = cur_index
                cur_index += 1
            matrix[id_to_index[elem['citizen_id']], id_to_index[relative]] = 1
    if len(unique_test) != len(set(unique_test)):
        return False
    return np.allclose(matrix, matrix.T, rtol=1e-05, atol=1e-08) and sum(matrix.diagonal()) == 0

# test не забыть чтобы главная диагональ была нулевой
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
print(relativies_validation(data['citizens']))
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

print(relativies_validation(data['citizens']))


