import re


def format_response(data, status="success"):
    return {
        "status": status,
        "data": data,
    }


def format_error(message, status_code=400):
    return {
        "status": "error",
        "message": message,
    }, status_code


def normalize_tags(tags):
    if tags is None:
        return []
    if isinstance(tags, str):
        return [tag.strip() for tag in tags.split(",") if tag.strip()]
    if isinstance(tags, list):
        return [str(tag).strip() for tag in tags if str(tag).strip()]
    return []


def validate_entry_payload(payload, partial=False):
    if payload is None:
        return False, "Missing JSON payload"

    required_fields = ["title", "content"]
    if not partial:
        for field in required_fields:
            if field not in payload:
                return False, f"Missing required field: {field}"

    title = payload.get("title")
    content = payload.get("content")

    if title is not None and not isinstance(title, str):
        return False, "Title must be a string"
    if title is not None and len(title.strip()) < 3:
        return False, "Title must be at least 3 characters"
    if content is not None and not isinstance(content, str):
        return False, "Content must be a string"
    if content is not None and len(content.strip()) < 5:
        return False, "Content must be at least 5 characters"

    tags = payload.get("tags")
    if tags is not None and not isinstance(tags, (list, str)):
        return False, "Tags must be a list or comma-separated string"

    source = payload.get("source")
    if source is not None and not isinstance(source, str):
        return False, "Source must be a string"

    status = payload.get("status")
    if status is not None and not isinstance(status, str):
        return False, "Status must be a string"

    return True, "ok"


def sanitize_query(query):
    if not query:
        return None
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", query)
    return cleaned.strip() or None


def _get_first_value(args, key):
    value = args.get(key)
    if isinstance(value, list):
        return value[0] if value else None
    return value


def parse_pagination(args, default_limit):
    def _parse(value, fallback):
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback

    limit = _parse(_get_first_value(args, "limit"), default_limit)
    offset = _parse(_get_first_value(args, "offset"), 0)

    limit = max(1, min(limit, 100))
    offset = max(0, offset)

    return limit, offset
