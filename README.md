# DevTrack Django API

DevTrack is a small JSON-backed issue tracking API built with Django.

## Run locally

```powershell
cd D:\Airtribe_Django\devtrack\devtrack
python -m venv venv
venv\Scripts\activate
python -m pip install -r ..\requirements.txt
python manage.py migrate
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`.

## Endpoints

| Method | URL | Description |
|---|---|---|
| `POST` | `/api/issues/` | Creates an issue. Required JSON fields: `title`, `description`, `status`, `priority`, and `reporter_id`. |
| `GET` | `/api/issues/` | Lists all issues. |
| `GET` | `/api/issues/?id=<id>` | Returns one issue by ID. |
| `GET` | `/api/issues/?status=<status>` | Filters issues by `open`, `in_progress`, `resolved`, or `closed`. |
| `POST` | `/api/reporters/` | Creates a reporter. Required JSON fields: `name`, `email`, and `team`. |
| `GET` | `/api/reporters/` | Lists all reporters. |
| `GET` | `/api/reporters/?id=<id>` | Returns one reporter by ID. |
| `GET` | `/api/reporters/?team=<team>` | Filters reporters by team. |

Example issue request:

```json
{
  "title": "Login failure",
  "description": "User cannot sign in",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1
}
```

## Design decision

I keep the domain classes (`Issue`, `CriticalIssue`, `LowPriorityIssue`, and `Reporter`) in `issues/models.py` and keep HTTP handling in `issues/views.py`. This separates validation/domain behavior from request/response logic, makes polymorphic issue descriptions possible, and keeps the API views easier to test.

## Postman tests

Test the endpoints in Postman against `http://127.0.0.1:8000`. Save screenshots in `docs/` and add them here.
Add one success screenshot and one failure screenshot under `docs/postman-success.png` and `docs/postman-failure.png`.
