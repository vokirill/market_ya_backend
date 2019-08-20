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
from .support_functions import datetime_to_date
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
            date = datetime.datetime.strptime(date, date_format).date()
            dt = datetime.datetime.now().date()
            if date >= dt:
                return JsonResponse({'errors': 'person to young'}, status=400)
            else:
                citizen['birth_date'] = date
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

    if data == {}:
        return JsonResponse({'errors': 'empty JSON'}, status = 400)

    changed_row = Imports.objects.get_data_for_patch(imports_id, citizens)[0]

    for key in data.keys():
        if key == 'relatives':
            cur_relatives = Imports.objects.get_data_for_patch(imports_id, citizens).values('relatives')[0]
            cur_relatives = set(map(int, cur_relatives['relatives'].split(',')))
            new_relatives = set(data[key])
            deletion = list(cur_relatives - new_relatives)
            addition = list(new_relatives - cur_relatives)
            if deletion != [] or addition != []:
                relatives_list = Imports.objects.get_data_for_patch_relatives(imports_id).values('citizen_id', 'relatives')
                for i, elem in enumerate(relatives_list):
                    indicator = 0
                    if elem['relatives'] != '':
                        new_relatives = list(map(int, elem['relatives'].split(',')))
                    else:
                        new_relatives = []

                    if elem['citizen_id'] in deletion:
                        try:
                            new_relatives.remove(citizens)
                            indicator+=1
                        except:
                            pass
                    if elem['citizen_id'] in addition:
                        new_relatives.append(citizens)
                        indicator+=1
                    if indicator >0:
                        new_relatives = ','.join(map(str, new_relatives))
                        other_changed = Imports.objects.get_data_for_patch(imports_id, elem['citizen_id'])[0]
                        setattr(other_changed, 'relatives', new_relatives)
                        other_changed.save()

            data[key] = ','.join(map(str, data[key]))
        if key == 'birth_date':
            try:
                date = data[key].split('.')
                date = '{0}-{1}-{2}'.format(date[2], date[1], date[0])
                date = datetime.datetime.strptime(date, date_format).date()
                dt = datetime.datetime.now().date()
                if date >= dt:
                    return JsonResponse({'errors': 'person to young'}, status=400)
                else:
                    data[key] = date
            except:
                return JsonResponse({'errors': 'wrong date {}'.format(data[key])}, status=400)
        setattr(changed_row, str(key), str(data[key]))
    changed_row.save()
    actual_data = Imports.objects.get_data_for_patch(imports_id, citizens).values()[0]
    actual_data['birth_date'] = datetime_to_date(actual_data['birth_date'])
    actual_data['relatives'] = list(map(int, actual_data['relatives'].split(',')))
    actual_data = {
        "data": {
            'citizen_id': actual_data['citizen_id'],
            'town': actual_data['town'],
            'street': actual_data['street'],
            'building': actual_data['building'],
            'apartment': actual_data['apartment'],
            'name': actual_data['name'],
            'birth_date': actual_data['birth_date'],
            'gender': actual_data['gender'],
            'relatives': actual_data['relatives'],
        }
    }
    return HttpResponse(json.dumps(actual_data, ensure_ascii=False), content_type="application/json", status=200)

@require_http_methods(["GET"])
def get_imports(request, imports_id):
    data = Imports.objects.get_import_data(imports_id).values()
    sum_list = []
    for i, elem in enumerate(data):
        del elem['id']
        del elem['import_id']
        elem['birth_date'] = datetime_to_date(elem['birth_date'])
        elem['relatives'] = list(map(int, elem['relatives'].split(',')))
        sum_list.append(elem)

    return HttpResponse(json.dumps({'data': sum_list},ensure_ascii=False), content_type="application/json", status=200)

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
        answer['data'].append({'town':elem[0], 'p50':round(percentile[0],2), 'p75':round(percentile[1],2), 'p99':round(percentile[2],2)})
    return HttpResponse(json.dumps( answer,ensure_ascii=False), content_type="application/json", status=200)

def response_test_view(request):
    return HttpResponse("Welcom to my project test page ")