import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase

from . import views


class IssueEndpointTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.issue_file = Path(self.temp_dir.name) / "issues.json"
        self.reporter_file = Path(self.temp_dir.name) / "reporters.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_issue_success(self):
        with patch.object(views, "file_path", self.issue_file):
            response = self.client.post(
                "/api/issues/",
                data=json.dumps({
                    "title": "Login failure",
                    "description": "Cannot log in",
                    "status": "open",
                    "priority": "critical",
                    "reporter_id": 1,
                }),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Login failure")
        self.assertIn("URGENT", response.json()["message"])

    def test_create_issue_invalid_status(self):
        with patch.object(views, "file_path", self.issue_file):
            response = self.client.post(
                "/api/issues/",
                data=json.dumps({
                    "title": "Login failure",
                    "description": "Cannot log in",
                    "status": "unknown",
                    "priority": "high",
                    "reporter_id": 1,
                }),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 400)

    def test_filter_issues_by_status(self):
        self.issue_file.write_text(
            json.dumps([{
                "id": 1,
                "title": "Example",
                "description": "Example issue",
                "status": "open",
                "priority": "medium",
                "reporter_id": 1,
                "created_at": "2026-11-21",
            }]),
            encoding="utf-8",
        )
        with patch.object(views, "file_path", self.issue_file):
            response = self.client.get("/api/issues/?status=open")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


class ReporterEndpointTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.reporter_file = Path(self.temp_dir.name) / "reporters.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_reporter_success(self):
        with patch.object(views, "reporters_file_path", self.reporter_file):
            response = self.client.post(
                "/api/reporters/",
                data=json.dumps({
                    "name": "Asha",
                    "email": "asha@example.com",
                    "team": "backend",
                }),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], "asha@example.com")

    def test_create_reporter_invalid_email(self):
        with patch.object(views, "reporters_file_path", self.reporter_file):
            response = self.client.post(
                "/api/reporters/",
                data=json.dumps({
                    "name": "Asha",
                    "email": "not-an-email",
                    "team": "backend",
                }),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 400)
