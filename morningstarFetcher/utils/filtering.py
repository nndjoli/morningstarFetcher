OPERATORS_BY_TYPE = {
    "string": [
        "=",
        "!=",
        "<>",
        "in",
        "not in",
        "like",
        "not like",
        "between",
        "not between",
        "is null",
        "is not null",
    ],
    "number": [
        "=",
        "!=",
        "<>",
        "<",
        "<=",
        ">",
        ">=",
        "in",
        "not in",
        "between",
        "not between",
        "is null",
        "is not null",
    ],
    "date": [
        "=",
        "!=",
        "<>",
        "<",
        "<=",
        ">",
        ">=",
        "in",
        "not in",
        "between",
        "not between",
        "is null",
        "is not null",
    ],
    "boolean": ["=", "!=", "<>", "is", "is not", "is null", "is not null"],
    "currency": [
        "=",
        "!=",
        "<>",
        "<",
        "<=",
        ">",
        ">=",
        "in",
        "not in",
        "between",
        "not between",
        "is null",
        "is not null",
    ],
    "rank": [
        "=",
        "!=",
        "<>",
        "<",
        "<=",
        ">",
        ">=",
        "in",
        "not in",
        "between",
        "not between",
        "is null",
        "is not null",
    ],
    "percent": [
        "=",
        "!=",
        "<>",
        "<",
        "<=",
        ">",
        ">=",
        "in",
        "not in",
        "between",
        "not between",
        "is null",
        "is not null",
    ],
}


def build_filter_string(filters, available_fields):
    """Return a query snippet from a list of filters with wildcard support."""
    filter_strings = []
    for field, operator, value in filters:
        if field not in available_fields:
            continue
        field_type = available_fields[field]
        allowed = OPERATORS_BY_TYPE.get(field_type, OPERATORS_BY_TYPE["string"])
        op = operator
        val = str(value)
        if field_type == "string" and any(ch in val for ch in "*?"):
            val = val.replace("*", "%").replace("?", "_")
            if op in {"="}:
                op = "like"
            elif op in {"!=", "<>"}:
                op = "not like"
        if op not in allowed:
            continue
        if field_type in {"string", "date"} and not (val.startswith("\"") or val.startswith("'")):
            val = f'"{val}"'
        filter_strings.append(f"{field} {op} {val}")
    return f"({' AND '.join(filter_strings)})" if filter_strings else ""
