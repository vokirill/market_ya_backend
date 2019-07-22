PATCH_SHEMMA = {
    'type': 'object',
        'properties': {
            'town':{
                'type': 'string',
                'minLength': 2,
                'maxLength': 100
            },
            'street':{
                'type': 'string',
                'minLength': 2,
                'maxLength': 100
            },
            'building': {
                'type': 'string',
                'minLength': 1,
                'maxLength': 100
            },
            'appartment':{
                'type': 'integer',
                'minimum': 1
            },
            'name': {
                'type': 'string',
                'minLength': 5,
                'maxLength': 1000
            },
            'birth_date':{
                'type': 'string',
                'format': 'date'
            },
            'gender': {
                'type': 'string',
                'minLength': 4,
                'maxLength': 6
            },
            'relatives': {
                'type': 'array',
                'items': {
                    'type': 'number'
                }

            },
        },
}


IMPORTS_SHEMMA = {
    'type' : 'object',
    'properties': {
        'citizens': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'citizen_id':{
                        'type': 'integer',
                        'minimum': 0,
                    },
                    'town':{
                        'type': 'string',
                        'minLength': 2,
                        'maxLength': 100
                    },
                    'street':{
                        'type': 'string',
                        'minLength': 2,
                        'maxLength': 100
                    },
                    'building': {
                        'type': 'string',
                        'minLength': 1,
                        'maxLength': 100
                    },
                    'appartment':{
                        'type': 'integer',
                        'minimum': 1
                    },
                    'name': {
                        'type': 'string',
                        'minLength': 5,
                        'maxLength': 1000
                    },
                    'birth_date':{
                        'type': 'string',
                        'format': 'date'
                    },
                    'gender': {
                        'type': 'string',
                        'minLength': 4,
                        'maxLength': 6
                    },
                    'relatives': {
                        'type': 'array',
                        'items': {
                            'type': 'number'
                        }

                    },
                },
                'required': ['citizen_id','town','street','building', 'appartment', 'name', 'birth_date','gender','relatives']
            }
        }
    },
    'required':['citizens']
}

