from copy import deepcopy
from json import JSONEncoder
import collections

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

        errors = []
        for error in schema_validator.iter_errors(data):
            errors.append({
                'pathNames': list(collections.deque(error.path)),
                'path': '.'.join(map(lambda pathName: pathName.__str__(), error.path)),
                'validator_name': error.validator,
                'validator_value': error.validator_value,
                'value': error.instance
            })
        
        return errors