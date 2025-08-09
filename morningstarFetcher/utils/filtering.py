from collections.abc import Sequence

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
        val = value
        if op in {"in", "not in"} and isinstance(val, Sequence) and not isinstance(val, str):
            items = []
            for item in val:
                item_val = str(item)
                if field_type in {"string", "date"} and not (item_val.startswith('"') or item_val.startswith("'")):
                    item_val = f"'{item_val}'"
                items.append(item_val)
            val = f"({','.join(items)})"
        else:
            val = str(val)
        if field_type == "string" and any(ch in val for ch in "*?"):
            val = val.replace("*", "%").replace("?", "_")
            if op in {"="}:
                op = "like"
            elif op in {"!=", "<>"}:
                op = "not like"
        if op not in allowed:
            continue
        if field_type in {"string", "date"} and not (val.startswith('"') or val.startswith("'") or (val.startswith("(") and val.endswith(")"))):
            val = f'"{val}"'
        filter_strings.append(f"{field} {op} {val}")
    return f"({' AND '.join(filter_strings)})" if filter_strings else ""
