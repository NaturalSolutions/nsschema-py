import nsschema

from copy import deepcopy

schema = {
    '$schema': "http://json-schema.org/schema#",
    "type": "object",
    'definitions': {
        'step_1': {
            'type': 'object',
            'properties': {
                'field_a': {
                    'type': 'string',
                    'format' : 'starts_by_a'
                },
                'field_b': {
                    'type': 'string'
                }
            },
            'required': ['field_a'],
            'dependencies': {
                'field_b': {
                    "properties": {
                        "field_c": {
                            "type": "number",
                            "exclusiveMinimum": 10,
                            "format"    : "even"
                        }
                    },
                    'dependencies': {
                        'field_c': {
                            'properties': {
                                'field_x': {
                                    "type": "string"
                                }
                            }
                        }
                    }
                }
            }
        },
        'step_2': {
            'allOf': [{
                '$ref': '#/definitions/step_1'
            }, {
                'properties': {
                    'field_d': {
                        'type': 'string'
                    },
                    'field_e': {
                        'type': 'string'
                    }
                },
                'required': ['field_d', 'field_e']
            }]
        },
        'step_3': {
            'type': 'object',
            'properties': {
                'field_f': {
                    'type': 'string'
                }
            }
        }
    },

    'allOf': [{
        '$ref': '#/definitions/step_1'
    }, {
        '$ref': '#/definitions/step_2'
    }, {
        '$ref': '#/definitions/step_3'
    }]
}


validator = nsschema.NsSchema()
validator.add_format_checker('even', checker = lambda value : value % 2 == 0)
validator.add_format_checker('starts_by_a', checker= lambda value : False if len(value) == 0 else value[0] == 'a')

schema = nsschema.build_schema_from_definition(schema, 'step_1')

data = {
    'field_a': 'a1',
    'field_b': '1',
    'field_c': 11,
    'field_x': '1'
}


errors = validator.validate(schema, data)

print(errors)
