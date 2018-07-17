from renecovalidator import RenecoValidator
from copy import deepcopy

schema = {
    '$schema': "http://json-schema.org/schema#",
    "type": "object",
    'definitions': {
        'step_1': {
            'type': 'object',
            'properties': {
                'field_a': {
                    'type': 'string'
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
                            "exclusiveMinimum": 10
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


def create_step_schema(global_schema, step):
    if step is None:
        return global_schema
    else:
        schema_step = global_schema.get('definitions', {}).get(step, {})
        schema_step['definitions'] = global_schema.get('definitions', {})
        schema_step['definitions'].pop(step)
        return schema_step


schema = create_step_schema(schema, 'step_1')

data = {
    'field_a': '1',
    'field_b': '1',
    'field_c': 11,
    'field_x': 1
}


errors = RenecoValidator.validate(schema, data)

print(errors)
