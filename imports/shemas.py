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
            'apartment':{
                'type': 'integer',
                'minimum': 0
            },
            'name': {
                'type': 'string',
                'minLength': 1,
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
        'additionalProperties': False,
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
                    'apartment':{
                        'type': 'integer',
                        'minimum': 0
                    },
                    'name': {
                        'type': 'string',
                        'minLength': 1,
                    },
                    'birth_date':{
                        'type': 'string',
                        'pattern': "^(0?[1-9]|[12][0-9]|3[01]).(0?[1-9]|1[012]).\d{4}$",
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
                'required': ['citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives'],
                'additionalProperties': False,
            }
        }
    },
    'required':['citizens'],
    'additionalProperties': False,
}

