import numpy as np

def date_string(date_string):
    date = date_string.split('.')
    return '{0}-{1}-{2}'.format(date[2], date[1], date[0])

def relativies_validation(data):
    id_to_index = {}
    amount_of_citizens = len(data)
    matrix = np.zeros((amount_of_citizens,amount_of_citizens))
    cur_index = 0 # составляем матрицу смежности и проверяем
    for elem in data:
        if elem['citizen_id'] not in id_to_index.keys():
            id_to_index[elem['citizen_id']] = cur_index
            cur_index+=1
        for relative in elem['relatives']:
            if relative not in id_to_index.keys():
                id_to_index[relative] = cur_index
                cur_index += 1
            matrix[id_to_index[elem['citizen_id']], id_to_index[relative]] = 1
    return np.allclose(matrix, matrix.T, rtol=1e-05, atol=1e-08) and sum(matrix.diagonal()) == 0

# test не забыть чтобы главная диагональ была нулево
data = [
    {'citizen_id':1,
     'relatives':[2,3]},
    {'citizen_id':2,
     'relatives':[1,4]},
    {'citizen_id':3,
     'relatives':[1,4]},
    {'citizen_id':4,
     'relatives':[2,3]},
]
print(relativies_validation(data))