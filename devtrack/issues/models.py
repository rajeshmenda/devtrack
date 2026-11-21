from django.db import models
from datetime import datetime

from abc import ABC, abstractmethod

class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }

class Reporter(BaseEntity):
    def __init__(self, id, name, email, team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError('Name cannot be empty')
        if not isinstance(self.email, str) or '@' not in self.email:
            raise ValueError('Invalid email')
        if not isinstance(self.team, str) or not self.team.strip():
            raise ValueError('Team cannot be empty')

class Issue(BaseEntity):
    def __init__(self, id, title, description, status, priority, reporter_id):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = str(datetime.now())

    def validate(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError('title cannot be empty')
        allowed_status = ["open", "in_progress", "resolved", "closed"]

        if self.status not in allowed_status:
            raise ValueError('status should be within the allowed values')
        allowed_priorities = ["low", "medium", "high", "critical"]
        if self.priority not in allowed_priorities:
            raise ValueError('priority is wrong')
        
    def describe(self):
        return f"{self.title} [{self.priority}]"


class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} - needs immediate attention"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} - low priority, handle them when free"
