from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .shemas import *
import json
from django.core import serializers
from django.utils.dateparse import parse_date
from .support_functions import *
from django.db import connection


from .models import Imports

@csrf_exempt
@require_http_methods(["POST"])
def upload_treatments(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        validate(data, IMPORTS_SHEMMA)
    except ValidationError as exc:
        return JsonResponse({'errors': exc.message}, status = 400)
    except json.JSONDecodeError():
        return JsonResponse({'errors': 'Invalid JSON'}, status = 400)

    citezen_list = data['citizens']
    import_id_ = Imports.objects.get_max_import_id()['import_id__max']+1

    for citezen in citezen_list:
        citezen['relatives'] = ','.join(map(str, citezen['relatives']))
        db_row = Imports(import_id = import_id_, **citezen)
        db_row.save()

    response = {
        "data":{
            'import_id': import_id_
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

    changed_row = Imports.objects.get_data_for_patch(imports_id, citizens)[0]
    for key in data.keys():
        if key == 'relatives':
            data[key] = ','.join(map(str, data[key]))
        elif key == 'birth_date':
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
    #data = Imports.objects.get_import_data(imports_id).values('citizen_id', 'birth_date','relatives')

    query = '''
        WITH RECURSIVE split(import_id, citizen_id, relatives_number, rest) AS (
            SELECT import_id, citizen_id, '', relatives || ',' FROM imports_imports  WHERE import_id
            UNION ALL
            SELECT import_id,
                   citizen_id, 
                   substr(rest, 0, instr(rest, ',')),
                   substr(rest, instr(rest, ',')+1)
            FROM split
            WHERE rest <> '')
        SELECT citizen_id, relatives_number 
        FROM split 
        WHERE relatives_number <> '' AND import_id = {}
        ORDER BY citizen_id, relatives_number 
        
    '''.format(imports_id)

    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    #result =
    return HttpResponse(str(data), status = 200)
'''
query = 
        SELECT citizen_id,
               STRFTIME('%m', birth_date) as birt_month,
               relatives
        FROM imports_imports 
        WHERE imports_imports.import_id  = {}
        .format(imports_id)
'''