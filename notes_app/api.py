from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from notes_app import storage
from notes_app.notes import Note
from notes_app.checklists import Checklist

app = FastAPI(
    title="Notes & Checklists API",
    description="A REST API for managing notes and checklists",
    version="1.0.0"
)

class NoteCreate(BaseModel):
    title: str
    body: Optional[str] = ""
    tag: Optional[str] = "general"

class NoteUpdate(BaseModel):
    body: Optional[str] = None
    tag: Optional[str] = None

class ChecklistCreate(BaseModel):
    title: str
    label: Optional[str] = "item"
    completion_adverb: Optional[str] = "done"

class CheckItemCreate(BaseModel):
    text: str

@app.get("/notes")
def get_notes():
    data = storage.load()
    return data["notes"]

@app.post("/notes", status_code=201)
def create_note(payload: NoteCreate):
    data = storage.load()
    note = Note(payload.title, payload.body, payload.tag)
    data["notes"].append(note.to_dict())
    storage.save(data)
    return note.to_dict()

@app.patch("/notes/{note_id}")
def update_note(note_id: str, payload: NoteUpdate):
    data = storage.load()
    for n in data["notes"]:
        if n["id"] == note_id:
            if payload.body is not None:
                n["body"] = payload.body
            if payload.tag is not None:
                n["tag"] = payload.tag
            storage.save(data)
            return n
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: str):
    data = storage.load()
    original = len(data["notes"])
    data["notes"] = [n for n in data["notes"] if n["id"] != note_id]
    if len(data["notes"]) == original:
        raise HTTPException(status_code=404, detail="Note not found")
    storage.save(data)

@app.get("/checklists")
def get_checklists():
    data = storage.load()
    return data["checklists"]

@app.post("/checklists", status_code=201)
def create_checklist(payload: ChecklistCreate):
    data = storage.load()
    cl = Checklist(payload.title, payload.label, payload.completion_adverb)
    data["checklists"].append(cl.to_dict())
    storage.save(data)
    return cl.to_dict()

@app.post("/checklists/{checklist_id}/items", status_code=201)
def add_item(checklist_id: str, payload: CheckItemCreate):
    data = storage.load()
    for c in data["checklists"]:
        if c["id"] == checklist_id:
            cl = Checklist.from_dict(c)
            item = cl.add_item(payload.text)
            c.update(cl.to_dict())
            storage.save(data)
            return item.to_dict()
    raise HTTPException(status_code=404, detail="Checklist not found")

@app.patch("/checklists/{checklist_id}/items/{item_id}/toggle")
def toggle_item(checklist_id: str, item_id: str):
    data = storage.load()
    for c in data["checklists"]:
        if c["id"] == checklist_id:
            cl = Checklist.from_dict(c)
            try:
                cl.toggle_item(item_id)
            except ValueError:
                raise HTTPException(status_code=404, detail="Item not found")
            c.update(cl.to_dict())
            storage.save(data)
            return c
    raise HTTPException(status_code=404, detail="Checklist not found")

@app.delete("/checklists/{checklist_id}", status_code=204)
def delete_checklist(checklist_id: str):
    data = storage.load()
    original = len(data["checklists"])
    data["checklists"] = [c for c in data["checklists"] if c["id"] != checklist_id]
    if len(data["checklists"]) == original:
        raise HTTPException(status_code=404, detail="Checklist not found")
    storage.save(data)
