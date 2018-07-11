from copy import deepcopy
from jsonschema.exceptions import ValidationError

def thesaurus(validator, value, instance, schema):
    url = value['url']
    data = deepcopy(value['data'])
    data['sValue'] = instance

    if data['sValue'] != 'toto':
        yield ValidationError("%r is not 'toto'" % (instance,), validator_value=value['data'])