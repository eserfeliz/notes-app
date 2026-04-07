from datetime import datetime
from zoneinfo import ZoneInfo
import uuid

TIMEZONE = ZoneInfo("America/New_York")

class CheckItem:
    def __init__(self, text):
        if not text.strip():
            raise ValueError("Item text cannot be empty")
        self.id = str(uuid.uuid4())[:8]
        self.text = text.strip()
        self.done = False

    def toggle(self):
        self.done = not self.done

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "done": self.done
        }

    @staticmethod
    def from_dict(data):
        item = CheckItem.__new__(CheckItem)
        item.id = data["id"]
        item.text = data["text"]
        item.done = data["done"]
        return item

    def __repr__(self):
        status = "x" if self.done else " "
        return f"[{status}] {self.text}"


class Checklist:
    def __init__(self, title, label="item", completion_adverb="done"):
        if not title.strip():
            raise ValueError("Title cannot be empty")
        self.id = str(uuid.uuid4())[:8]
        self.title = title.strip()
        self.label = label
        self.completion_adverb = completion_adverb
        self.created = datetime.now(TIMEZONE).strftime("%Y-%m-%d %I:%M %p")
        self.items = []

    def add_item(self, text):
        item = CheckItem(text)
        self.items.append(item)
        return item

    def remove_item(self, item_id):
        self.items = [i for i in self.items if i.id != item_id]

    def toggle_item(self, item_id):
        for item in self.items:
            if item.id == item_id:
                item.toggle()
                return
        raise ValueError(f"Item {item_id} not found")

    def progress(self):
        if not self.items:
            return f"No {self.label}s"
        done = sum(1 for i in self.items if i.done)
        return f"{done}/{len(self.items)} {self.completion_adverb}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "label": self.label,
            "completion_adverb": self.completion_adverb,
            "created": self.created,
            "items": [i.to_dict() for i in self.items]
        }

    @staticmethod
    def from_dict(data):
        cl = Checklist.__new__(Checklist)
        cl.id = data["id"]
        cl.title = data["title"]
        cl.label = data.get("label", "item")
        cl.completion_adverb = data.get("completion_adverb", "done")
        cl.created = data["created"]
        cl.items = [CheckItem.from_dict(i) for i in data["items"]]
        return cl

    def display(self):
        return f"{self.title} — {self.progress()} — {self.created}"

    def __repr__(self):
        return f"[{self.id}] {self.title} — {self.progress()} — {self.created}"