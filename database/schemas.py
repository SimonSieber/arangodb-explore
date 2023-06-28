NODE_COMPANY = {
    "rule": {
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "country": {"type": "string"},
            "permid": {"type": "string"},
            "lei": {"type": "string"},
        },
        "required": ["id", "name", "country"],
        "additionalProperties": False,
    },
    "level": "strict",
    "message": "Company validation failed.",
}

NODE_REPORT = {
    "rule": {
        "properties": {
            "id": {"type": "string"},
            "filename": {"type": "string"},
            "title": {"type": "string"},
            "type": {
                "type": "array",
                "items": {"type": "string"},
            },
            "publication_year": {"type": "string"},
            "report_year": {"type": "string"},
            "url": {"type": "string"},
            "num_pages": {"type": "string"},
        },
        "required": ["id"],
        "additionalProperties": False,
    },
    "level": "strict",
    "message": "Report validation failed.",
}

NODE_NET_ZERO_TARGET = {
    "rule": {
        "properties": {
            "id": {"type": "string"},
            # "target_year": {"type": "string"},
            # "reference_year": {"type": "string"},
            # "absolute_target_value": {"value": "string"},
            # "relative_target_value": {"value": "string"},
            # "company_division": {"type": "string"},
        },
        "required": ["id"],
        # "additionalProperties": False,
    },
    "level": "strict",
    "message": "Net Zero Target validation failed.",
}

NODE_PORTFOLIO = {
    "rule": {
        "properties": {
            "id": {"type": "string"},
        },
        "required": ["id"],
        "additionalProperties": False,
    },
    "level": "strict",
    "message": "Portfolio validation failed.",
}


REL_DEFINES = {
    "rule": {
        "properties": {
            "page": {"type": "number"},
            "text": {"type": "string"},
            "statement": {"type": "string"},
        },
        "required": ["references"],
        "additionalProperties": False,
    },
    "level": "strict",
    "message": "Validation of relation 'defines' failed.",
}

REL_RELATES_TO = {
    "rule": {
        "properties": {
            "statement_type": {"type": "string"},
        },
        "required": ["statement_type"],
        "additionalProperties": False,
    },
    "level": "strict",
    "message": "Validation of relation 'relates_to' failed.",
}
