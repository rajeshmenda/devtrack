from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Issue, CriticalIssue, LowPriorityIssue, Reporter
import json
from django.conf import settings


def read_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        return json.dump(data, f, indent=2)           
file_path = settings.BASE_DIR / "issues" / "issues.json"

@csrf_exempt
def issues(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'error': 'invalid JSON body'}, status=400)

        required_fields = ("title", "description", "status", "priority", "reporter_id")
        missing = [field for field in required_fields if field not in data]
        if missing:
            return JsonResponse({'error': f"missing required fields: {', '.join(missing)}"}, status=400)

        all_issues = read_data(file_path)
        new_id = max((item["id"] for item in all_issues if isinstance(item.get("id"), int)), default=0) + 1

        if data["priority"] == 'critical':
            issue = CriticalIssue(new_id, data["title"], data["description"], data["status"], data["priority"], data["reporter_id"])
        elif data["priority"] == 'low':
            issue = LowPriorityIssue(new_id, data["title"], data["description"], data["status"], data["priority"], data["reporter_id"])
        else:
            issue = Issue(new_id, data["title"], data["description"], data["status"], data["priority"], data["reporter_id"])

        try:
            issue.validate()
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        all_issues.append(issue.to_dict())
        write_data(file_path, all_issues)
        response_back = issue.to_dict()
        response_back["message"] = issue.describe()
        return JsonResponse(response_back, status=201)

    elif request.method == "GET":
        all_issues = read_data(file_path)
        issue_id = request.GET.get("id")
        status = request.GET.get("status")

        if issue_id:
            try:
                issue_id = int(issue_id)
            except (TypeError, ValueError):
                return JsonResponse({'error': 'id must be an integer'}, status=400)
            issue = [item for item in all_issues if item["id"] == issue_id]
            if issue:
                return JsonResponse(issue[0], status=200)
            return JsonResponse({'error': 'issue not found'}, status=404)

        if status:
            if status not in ["open", "in_progress", "resolved", "closed"]:
                return JsonResponse({'error': 'status should be within the allowed values'}, status=400)
            issues_by_status = [item for item in all_issues if item["status"] == status]
            return JsonResponse(issues_by_status, status=200, safe=False)
        return JsonResponse(all_issues, status=200, safe=False)

    return JsonResponse({'error': 'method not allowed'}, status=405)

reporters_file_path = settings.BASE_DIR / "issues" / "reporters.json"

@csrf_exempt
def reporters(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'error': 'invalid JSON body'}, status=400)

        required_fields = ("name", "email", "team")
        missing = [field for field in required_fields if field not in data]
        if missing:
            return JsonResponse({'error': f"missing required fields: {', '.join(missing)}"}, status=400)

        all_reporters = read_data(reporters_file_path)
        new_id = max((reporter["id"] for reporter in all_reporters if isinstance(reporter.get("id"), int)), default=0) + 1
        reporter = Reporter(new_id, data["name"], data["email"], data["team"])
        try:
            reporter.validate()
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        all_reporters.append(reporter.to_dict())
        write_data(reporters_file_path, all_reporters)
        return JsonResponse(reporter.to_dict(), status=201)

    elif request.method == "GET":
        all_reporters = read_data(reporters_file_path)
        reporter_id = request.GET.get("id")
        team = request.GET.get("team")

        if reporter_id:
            try:
                reporter_id = int(reporter_id)
            except (TypeError, ValueError):
                return JsonResponse({'error': 'id must be an integer'}, status=400)
            reporter = [item for item in all_reporters if item["id"] == reporter_id]
            if reporter:
                return JsonResponse(reporter[0], status=200)
            return JsonResponse({'error': 'reporter not found'}, status=404)

        if team:
            reporters_by_team = [item for item in all_reporters if item["team"] == team]
            if len(reporters_by_team) == 0:
                return JsonResponse({'error': 'no reporters found for this team'}, status=404)
            return JsonResponse(reporters_by_team, status=200, safe=False)

        return JsonResponse(all_reporters, status=200, safe=False)

    return JsonResponse({'error': 'method not allowed'}, status=405)