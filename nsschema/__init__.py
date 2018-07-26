from copy import deepcopy
from json import JSONEncoder
import collections
import re

from jsonschema import validators, Draft6Validator, FormatChecker

from .renecovalidators import *


def build_schema_from_definition(schema, definition):
    """ Builds a schema from a definition contained inside a schema """
    if definition is None:
        return schema
    else:
        schema_definition = schema.get('definitions', {}).get(definition, {})
        schema_definition['definitions'] = schema.get('definitions', {})
        schema_definition['definitions'].pop(definition)
        return schema_definition


def format_error(error):
    def get_property_name(error):
        return error.message.split("'")[1] \
            if error.validator in ['required', 'dependencies'] \
            else error.schema_path[len(error.schema_path) - 2]
    
    def get_value(error):
        return error.instance \
            if error.validator not in ['required', 'dependencies'] \
            else None

    def get_dependency_name(error):
        """ Retrieves the dependency name from the error message if the error type is 'dependency', 
        otherwise retrieves it from the schema path """
        def _get_dependency_name_from_schemaPath():
            schemaPath = error.schema_path
            schemaPathCopy = deepcopy(schemaPath)
            schemaPathCopy.reverse()

            return schemaPath[len(schemaPath) - schemaPathCopy.index('dependencies')]

        return re.search("\'(.*)\' .* \'(.*)\'", error.message).group(2) \
            if error.validator == 'dependencies' \
            else _get_dependency_name_from_schemaPath() \
                if 'dependencies' in error.schema_path \
                else None

    return {
        'schemaPath': list(collections.deque(error.schema_path)),
        'keyword': error.validator,
        'keywordValue': error.validator_value,
        'property': get_property_name(error),
        'value': get_value(error),
        'dependency': get_dependency_name(error),
        'message': error.message
    }

class NsSchema:
    """ A set of tools for managing json schemas built on top of jsonschema """
    def __init__(self, arg_validators=dict()):
        self.nsvalidators = arg_validators
        self.format_checker = FormatChecker()
    

    def add_validators(self, arg_validators):
        self.nsvalidators.update(arg_validators)
    

    def add_format_checker(self, keyword, checker=lambda value : True):
        @self.format_checker.checks(keyword)
        def custom_map(value):
            return checker(value)

    def validate(self, schema, data):

        SchemaValidator = validators.extend(
            Draft6Validator,
            validators=self.nsvalidators
        )

        schema_validator = SchemaValidator(
            schema, format_checker=self.format_checker
        )

        errors = [format_error(error) for error in schema_validator.iter_errors(data)]

        return errors