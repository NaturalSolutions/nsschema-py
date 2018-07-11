from renecovalidator import RenecoValidator

schema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "value": {
            "type": "number",
            "format": "even"
        },
        "test": {
            "type": "string",
            "thesaurus": {
                "url": "natural2018/thesaurusCore/api/Thesaurus/existBy",
                "data": {
                    "sTypeField": "FullPath",
                    "sLng": 'Fr'
                }
            }
        }
    }
}

errors = RenecoValidator.validate(schema, {
    'value': 2,
    'test': 'tata'
})

print(errors)