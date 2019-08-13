from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from jsonschema import validate
from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
from .shemas import *
import json

from .support_functions import date_format
from .support_functions import relativies_validation
from django.db import connection

from .models import *
import numpy as np
import datetime


from .models import Imports

@csrf_exempt
@require_http_methods(["POST"])
def upload_treatments(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        validate(data, IMPORTS_SHEMMA, format_checker=FormatChecker())
    except ValidationError as exc:
        return JsonResponse({'errors': exc.message}, status=400)
    except json.JSONDecodeError():
        return JsonResponse({'errors': 'Invalid JSON'}, status=400)

    citizen_list = data['citizens']
    if not relativies_validation(citizen_list):
        return JsonResponse({'errors': 'bad relatives or citizen_id dependencies'}, status = 400)

    import_id_ = Imports.objects.get_max_import_id()['import_id__max']
    if import_id_:
        import_id_+=1
    else:
        import_id_ = 1

    for citizen in citizen_list:
        citizen['relatives'] = ','.join(map(str, citizen['relatives']))
        try:
            date = citizen['birth_date'].split('.')
            date = '{0}-{1}-{2}'.format(date[2], date[1], date[0])
            citizen['birth_date'] = datetime.datetime.strptime(date, date_format)
        except:
            return JsonResponse({'errors': 'wrong date {}'.format(citizen['birth_date'])}, status=400)
        db_row = Imports(import_id = import_id_, **citizen)
        db_row.save()

    response = {
        "data":{
            "import_id": import_id_
        }
    }
    return JsonResponse(response, status = 201)


@csrf_exempt
@require_http_methods(["PATCH"])
def patch_imports(request, imports_id, citizens):
    try:
        data = json.loads(request.body.decode('utf-8'))
        validate(data, PATCH_SHEMMA)
    except ValidationError as exc:
        return JsonResponse({'errors': exc.message}, status = 400)
    except json.JSONDecodeError():
        return JsonResponse({'errors': 'Invalid JSON'}, status = 400)

    if 'relatives' in data.keys():
        changed_row = Imports.objects.get_data_for_patch_relatives(imports_id)[0]

    changed_row = Imports.objects.get_data_for_patch(imports_id, citizens)[0]
    for key in data.keys():
        if key == 'relatives':
            data[key] = ','.join(map(str, data[key]))
        if key == 'birth_date':
            data[key] = date_string(data[key])
        setattr(changed_row, str(key), str(data[key]))
    changed_row.save()
    actual_data = Imports.objects.get_data_for_patch(imports_id, citizens).values()[0]
    return HttpResponse(str(actual_data), status = 200)


@require_http_methods(["GET"])
def get_imports(request, imports_id):
    data = Imports.objects.get_import_data(imports_id).values()
    sum_list = []
    for i, elem in enumerate(data):
        del elem['id']
        sum_list.append(elem)

    return HttpResponse(str({'data':sum_list}), status=200)

@require_http_methods(["GET"])
def calc_birthdays(request, imports_id):
    query = fourth_task_query(imports_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    answer = {'data':{
        '1':[],
        '2':[],
        '3':[],
        '4':[],
        '5':[],
        '6':[],
        '7':[],
        '8':[],
        '9':[],
        '10':[],
        '11':[],
        '12':[]
    }}
    for elem in data:
        answer['data'][str(elem[0])].append({'citizen_id':elem[1], 'presents':elem[2]})

    return JsonResponse(answer, status = 200)

@require_http_methods(["GET"])
def age_percentile (request, imports_id):
    query = fifth_task_query(imports_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    answer = {'data':[]}
    for elem in data:
        percentile = np.percentile(list(map(int , elem[1].split(','))), [0.5, 0.75, 0.99], interpolation='linear')
        answer['data'].append({'town':elem[0], 'p50':percentile[0], 'p75':percentile[1], 'p99':percentile[2]})
    return HttpResponse(str(answer), status= 200)