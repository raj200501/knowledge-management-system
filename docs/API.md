# API Reference

Base URL: `http://127.0.0.1:5000`

## GET /health

Returns service metadata.

Response:

```json
{
  "status": "success",
  "data": {
    "status": "ok",
    "environment": "development",
    "page_size": 20
  }
}
```

## GET /entries

Retrieve knowledge entries with pagination and optional search.

Query parameters:

- `query`: search across title and content
- `tag`: filter by tag
- `limit`: max results (default 20, max 100)
- `offset`: start offset

Response:

```json
{
  "status": "success",
  "data": {
    "items": [],
    "total": 0,
    "limit": 20,
    "offset": 0
  }
}
```

## POST /entry

Create a new entry.

```json
{
  "title": "First Entry",
  "content": "Hello knowledge base",
  "tags": ["intro", "example"],
  "source": "manual",
  "status": "active"
}
```

Response includes the stored entry with timestamps.

## GET /entry/<id>

Retrieve a single entry by ID.

## PUT /entry/<id>

Update a single entry. Fields are optional and overwrite existing values.

## DELETE /entry/<id>

Delete a single entry.
