import os
from notes_app import storage
from notes_app.notes import Note
from notes_app.checklists import Checklist

def clear():
    os.system("clear")

def print_menu():
    print("\n=============================")
    print("     NOTES & CHECKLISTS")
    print("=============================")
    print("\nNOTES")
    print("  1. View all notes")
    print("  2. Add a note")
    print("  3. Edit a note")
    print("  4. Delete a note")
    print("\nCHECKLISTS")
    print("  5. View all checklists")
    print("  6. Add a checklist")
    print("  7. Manage a checklist")
    print("  8. Delete a checklist")
    print("\n  0. Quit")

def pick(items, label="item", display_fn=None):
    if not items:
        print(f"\n  No {label}s found.")
        return None
    print()
    for i, item in enumerate(items, start=1):
        display = display_fn(item) if display_fn else str(item)
        print(f"  {i}. {display}")
    print()
    choice = input(f"  Select {label} number (or 0 to cancel): ").strip()
    if choice == "0" or not choice:
        return None
    try:
        index = int(choice) - 1
        if 0 <= index < len(items):
            return items[index]
        else:
            print("  Invalid selection.")
            return None
    except ValueError:
        print("  Please enter a number.")
        return None

# ─── NOTE FUNCTIONS ───────────────────────────────────────────

def view_notes(data):
    clear()
    print("\n── Your Notes ──────────────────\n")
    if not data["notes"]:
        print("  No notes yet.")
        return
    for n in data["notes"]:
        note = Note.from_dict(n)
        print(f"  {note.display()}")
        if note.body:
            print(f"     {note.body[:60]}{'...' if len(note.body) > 60 else ''}")
        print()

def add_note(data):
    clear()
    print("\n── Add a Note ──────────────────\n")
    title = input("  Title: ").strip()
    if not title:
        print("  Title cannot be empty.")
        return
    body = input("  Body (optional): ").strip()
    print("  Tags: general, work, personal, ideas")
    tag = input("  Tag [general]: ").strip() or "general"
    note = Note(title, body, tag)
    data["notes"].append(note.to_dict())
    storage.save(data)
    print(f"\n  ✓ Note '{title}' saved.")

def edit_note(data):
    clear()
    print("\n── Edit a Note ─────────────────")
    notes = [Note.from_dict(n) for n in data["notes"]]
    note = pick(notes, "note", display_fn=lambda n: n.display())
    if note is None:
        return
    print(f"\n  Editing: {note.title}")
    new_body = input(f"  New body [{note.body}]: ").strip()
    new_tag = input(f"  New tag [{note.tag}]: ").strip()
    for n in data["notes"]:
        if n["id"] == note.id:
            if new_body:
                n["body"] = new_body
            if new_tag:
                n["tag"] = new_tag
            storage.save(data)
            print("\n  ✓ Note updated.")
            return

def delete_note(data):
    clear()
    print("\n── Delete a Note ───────────────")
    notes = [Note.from_dict(n) for n in data["notes"]]
    note = pick(notes, "note", display_fn=lambda n: n.display())
    if note is None:
        return
    confirm = input(f"\n  Delete '{note.title}'? (y/n): ").strip().lower()
    if confirm == "y":
        data["notes"] = [n for n in data["notes"] if n["id"] != note.id]
        storage.save(data)
        print("\n  ✓ Note deleted.")
    else:
        print("\n  Cancelled.")

# ─── CHECKLIST FUNCTIONS ──────────────────────────────────────

def view_checklists(data):
    clear()
    print("\n── Your Checklists ─────────────\n")
    if not data["checklists"]:
        print("  No checklists yet.")
        return
    for c in data["checklists"]:
        cl = Checklist.from_dict(c)
        print(f"  {cl.display()}")
        for item in cl.items:
            print(f"     {item}")
        print()

def add_checklist(data):
    clear()
    print("\n── Add a Checklist ─────────────\n")
    title = input("  Title: ").strip()
    if not title:
        print("  Title cannot be empty.")
        return
    label = input("  What are the items called? [item]: ").strip() or "item"
    completion_adverb = input(f"  What does it mean when a {label} is checked off? [done]: ").strip() or "done"
    cl = Checklist(title, label, completion_adverb)
    print(f"\n  Add {label}s (press Enter with no text to finish):")
    while True:
        item = input("  + ").strip()
        if not item:
            break
        cl.add_item(item)
    data["checklists"].append(cl.to_dict())
    storage.save(data)
    print(f"\n  ✓ '{title}' saved with {len(cl.items)} {label}s.")

def manage_checklist(data):
    clear()
    print("\n── Manage a Checklist ──────────")
    checklists = [Checklist.from_dict(c) for c in data["checklists"]]
    cl = pick(checklists, "checklist", display_fn=lambda c: c.display())
    if cl is None:
        return
    for c in data["checklists"]:
        if c["id"] == cl.id:
            while True:
                clear()
                print(f"\n── {cl.title} — {cl.progress()} ──\n")
                items = cl.items
                for i, item in enumerate(items, start=1):
                    print(f"  {i}. {item}")
                print("\n  t. Toggle item")
                print("  a. Add item")
                print("  d. Delete item")
                print("  b. Back")
                action = input("\n  > ").strip().lower()
                if action == "t":
                    item = pick(cl.items, "item")
                    if item:
                        cl.toggle_item(item.id)
                elif action == "a":
                    text = input("  New item: ").strip()
                    if text:
                        cl.add_item(text)
                elif action == "d":
                    item = pick(cl.items, "item")
                    if item:
                        cl.remove_item(item.id)
                elif action == "b":
                    break
                c.update(cl.to_dict())
                storage.save(data)
            return

def delete_checklist(data):
    clear()
    print("\n── Delete a Checklist ──────────")
    checklists = [Checklist.from_dict(c) for c in data["checklists"]]
    cl = pick(checklists, "checklist", display_fn=lambda c: c.display())
    if cl is None:
        return
    confirm = input(f"\n  Delete '{cl.title}'? (y/n): ").strip().lower()
    if confirm == "y":
        data["checklists"] = [c for c in data["checklists"] if c["id"] != cl.id]
        storage.save(data)
        print("\n  ✓ Checklist deleted.")
    else:
        print("\n  Cancelled.")

# ─── MAIN LOOP ────────────────────────────────────────────────

def main():
    data = storage.load()
    actions = {
        "1": view_notes,
        "2": add_note,
        "3": edit_note,
        "4": delete_note,
        "5": view_checklists,
        "6": add_checklist,
        "7": manage_checklist,
        "8": delete_checklist,
    }
    while True:
        clear()
        print_menu()
        choice = input("\n> ").strip()
        if choice == "0":
            print("\nGoodbye!\n")
            break
        elif choice in actions:
            actions[choice](data)
            input("\nPress Enter to continue...")
        else:
            print("\n  Invalid choice.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()