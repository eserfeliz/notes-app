from datetime import datetime
from zoneinfo import ZoneInfo
import uuid

TIMEZONE = ZoneInfo("America/New_York")

class Note:
    def __init__(self, title, body="", tag="general"):
        if not title.strip():
            raise ValueError("Title cannot be empty")
        self.id = str(uuid.uuid4())[:8]
        self.title = title.strip()
        self.body = body
        self.tag = tag
        self.created = datetime.now(TIMEZONE).strftime("%Y-%m-%d %I:%M %p")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "tag": self.tag,
            "created": self.created
        }

    @staticmethod
    def from_dict(data):
        note = Note.__new__(Note)
        note.id = data["id"]
        note.title = data["title"]
        note.body = data["body"]
        note.tag = data["tag"]
        note.created = data["created"]
        return note

    def __repr__(self):
        return f"[{self.id}] ({self.tag}) {self.title} — {self.created}"