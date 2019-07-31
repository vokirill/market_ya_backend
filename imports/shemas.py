PATCH_SHEMMA = {
    'type': 'object',
        'properties': {
            'town':{
                'type': 'string',
                'minLength': 1,
            },
            'street':{
                'type': 'string',
                'minLength': 1
            },
            'building': {
                'type': 'string',
                'minLength': 1
            },
            'appartment':{
                'type': 'integer',
                'minimum': 1
            },
            'name': {
                'type': 'string',
                'minLength': 3,
            },
            'birth_date':{
                'type': 'string'
            },
            'gender': {
                'type': 'string',
                "enum": ['male', 'female']
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
                        'minLength': 1,
                    },
                    'street':{
                        'type': 'string',
                        'minLength': 1,
                    },
                    'building': {
                        'type': 'string',
                        'minLength': 1,
                    },
                    'appartment':{
                        'type': 'integer',
                        'minimum': 1
                    },
                    'name': {
                        'type': 'string',
                        'minLength': 3,
                    },
                    'birth_date':{
                        'type': 'string'
                    },
                    'gender': {
                        'type': 'string',
                        "enum": ['male', 'female']
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

