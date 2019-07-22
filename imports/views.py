from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .shemas import *
import json


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

    if 'relatives' not in  data.keys():
        changeed_row = Imports.objects.get_data_for_patch(imports_id, citizens).values()[0]


    return HttpResponse(str(changeed_row), status = 201)

