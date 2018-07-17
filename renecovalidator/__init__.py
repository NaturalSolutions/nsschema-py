from copy import deepcopy
from json import JSONEncoder
import collections
import re

from jsonschema import validators, Draft6Validator, FormatChecker

from .renecovalidators import *

class RenecoValidator:

    app_validators = dict(
        thesaurus=renecovalidators.thesaurus
    )

    # Create a new format checker instance.
    format_checker = FormatChecker()

    # Register a new format checker method for format 'even'. It must take exactly one
    # argument - the value for checking.
    @format_checker.checks('even')
    def even_number(value):
        return value % 2 == 0

    SchemaValidator = validators.extend(
        Draft6Validator,
        validators=app_validators
    )

    def validate(schema, data):
        schema_validator = RenecoValidator.SchemaValidator(
            schema, format_checker=RenecoValidator.format_checker
        )

        #return [ error for error in schema_validator.iter_errors(data) ]

        def getProperty(error):
            return error.message.split("'")[1] \
                if error.validator in ['required', 'dependencies'] \
                else error.schema_path[len(error.schema_path) - 2]
        
        def getValue(error):
            return error.instance \
                if error.validator not in ['required', 'dependencies'] \
                else None

        def getDependency(error):
            def getDependencyName():
                schemaPath = error.schema_path
                schemaPathCopy = deepcopy(schemaPath)
                schemaPathCopy.reverse()

                return schemaPath[len(schemaPath) - schemaPathCopy.index('dependencies')]

            return re.search("\'(.*)\' .* \'(.*)\'", error.message).group(2) \
                if error.validator == 'dependencies' \
                else getDependencyName() \
                    if 'dependencies' in error.schema_path \
                    else None

        # 'schema': list(collections.deque(error.schema)),
        # 'schema_names': '.'.join(map(lambda schema_name: schema_name.__str__(), error.schema)),
        # 'pathNames': list(collections.deque(error.path)),
        # 'path': '.'.join(map(lambda pathName: pathName.__str__(), error.path)),

        errors = [
            {
                'schemaPath': list(collections.deque(error.schema_path)),
                'keyword': error.validator,
                'keywordValue': error.validator_value,
                'property': getProperty(error),
                'value': getValue(error),
                'dependency': getDependency(error),
                'message': error.message
            } for error in schema_validator.iter_errors(data)]

        return errors
