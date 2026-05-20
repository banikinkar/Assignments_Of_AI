"""
Definition
City Library Management System with:
- Interative Menu for ease of user inputs
- JSON save/load persistence
Version:1.0 Author:Bani Assignment:Week4_Graded
"""

import json
from datetime import datetime

# --- Global Records  ---
books = {}          # book_id -> {id, title, author, genre, available}
members = {}        # member_id -> {id, name, age, contact, borrowed_books}
borrow_log = []     # list of {timestamp, member_id, book_id, action}
genre_popularity = {}  # genre -> times issued


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _generate_id(prefix, store):
    i = 1
    while True:
        candidate = f"{prefix}{i}"
        if candidate not in store:
            return candidate
        i += 1



def save_data(filename="library_data.json"):
    """ This function Save books, members, borrow_log, and genre_popularity to a JSON file."""
    payload = {
        "books": books,
        "members": members,
        "borrow_log": borrow_log,
        "genre_popularity": genre_popularity
    }
    with open(filename, "w") as f:
        json.dump(payload, f, indent=2)
    return filename

def load_data(filename="library_data.json"):
    """ This function Load data from JSON file into memory. Returns True if loaded, False otherwise."""
    global books, members, borrow_log, genre_popularity
    try:
        with open(filename, "r") as f:
            payload = json.load(f)
        books = {k: v for k, v in payload.get("books", {}).items()}
        members = {k: v for k, v in payload.get("members", {}).items()}
        borrow_log[:] = payload.get("borrow_log", [])
        genre_popularity.clear()
        genre_popularity.update(payload.get("genre_popularity", {}))
        return True
    except FileNotFoundError:
        return False

#  Book functions to add and check availability
def add_book(title, author, genre, book_id=None):
    if book_id is None:
        book_id = _generate_id("B", books)
    if book_id in books:
        raise ValueError("Book ID already exists.")
    books[book_id] = {
        "id": book_id,
        "title": title.strip(),
        "author": author.strip(),
        "genre": genre.strip().lower(),
        "available": True
    }
    genre_popularity.setdefault(genre.strip().lower(), 0)
    return book_id

def update_availability(book_id, available):
    if book_id not in books:
        raise KeyError("Book not found.")
    books[book_id]["available"] = bool(available)
    return True

#  Library Member record Functions
def register_member(name, age, contact, member_id=None):
    if member_id is None:
        member_id = _generate_id("M", members)
    if member_id in members:
        raise ValueError("Member ID already exists.")
    members[member_id] = {
        "id": member_id,
        "name": name.strip(),
        "age": int(age),
        "contact": contact.strip(),
        "borrowed_books": []
    }
    return member_id

#  Borrowing and Returning system
def issue_book(member_id, book_id):
    if member_id not in members:
        return f"Member {member_id} not found."
    if book_id not in books:
        return f"Book {book_id} not found."
    if not books[book_id]["available"]:
        return f"Book '{books[book_id]['title']}' is already issued."
    books[book_id]["available"] = False
    members[member_id]["borrowed_books"].append(book_id)
    borrow_log.append({
        "timestamp": _now(),
        "member_id": member_id,
        "book_id": book_id,
        "action": "issued"
    })
    genre = books[book_id]["genre"]
    genre_popularity[genre] = genre_popularity.get(genre, 0) + 1
    return f"Book '{books[book_id]['title']}' issued to {members[member_id]['name']}."

def return_book(member_id, book_id):
    if member_id not in members:
        return f"Member {member_id} not found."
    if book_id not in books:
        return f"Book {book_id} not found."
    if book_id not in members[member_id]["borrowed_books"]:
        return f"Member {member_id} did not borrow book {book_id}."
    books[book_id]["available"] = True
    members[member_id]["borrowed_books"].remove(book_id)
    borrow_log.append({
        "timestamp": _now(),
        "member_id": member_id,
        "book_id": book_id,
        "action": "returned"
    })
    return f"Book '{books[book_id]['title']}' returned by {members[member_id]['name']}."

#  Reports and related queries
def search_books_by_title_or_author(query):
    q = query.strip().lower()
    results = []
    for b in books.values():
        if q in b["title"].lower() or q in b["author"].lower():
            results.append(b.copy())
    return results

def available_books_by_genre(genre):
    g = genre.strip().lower()
    return [b.copy() for b in books.values() if b["genre"] == g and b["available"]]

def members_with_borrowed_books():
    return [m.copy() for m in members.values() if m["borrowed_books"]]

def most_popular_genre():
    if not genre_popularity:
        return (None, 0)
    max_genre = None
    max_count = -1
    for g, cnt in genre_popularity.items():
        if cnt > max_count:
            max_genre = g
            max_count = cnt
    if max_count <= 0:
        return (None, 0)
    return (max_genre, max_count)

def library_summary():
    total_books = len(books)
    available = sum(1 for b in books.values() if b["available"])
    total_members = len(members)
    borrowed = total_books - available
    popular_genre, pop_count = most_popular_genre()
    return {
        "total_books": total_books,
        "available_books": available,
        "borrowed_books": borrowed,
        "total_members": total_members,
        "members_with_borrowed_books": len(members_with_borrowed_books()),
        "most_popular_genre": popular_genre,
        "most_popular_genre_count": pop_count
    }

# Print Output
def print_books(book_list):
    if not book_list:
        print("  (No books found.)")
        return
    for b in book_list:
        status = "Available" if b["available"] else "Issued"
        print(f"  {b['id']} | {b['title']} by {b['author']} | Genre: {b['genre']} | {status}")

def print_members(member_list):
    if not member_list:
        print("  (No members found.)")
        return
    for m in member_list:
        print(f"  {m['id']} | {m['name']} | Age: {m['age']} | Contact: {m['contact']} | Borrowed: {m['borrowed_books']}")

def print_borrow_log():
    if not borrow_log:
        print("  (Borrow log is empty.)")
        return
    for entry in borrow_log:
        print(f"  {entry['timestamp']} | Member: {entry['member_id']} | Book: {entry['book_id']} | {entry['action']}")

#  Interactive Menu
def cli_menu():
    menu = """
Please choose from Below library Menu
1. Add book
2. Register member
3. Issue book
4. Return book
5. Search books (title/author)
6. Show available books by genre
7. List members with borrowed books
8. Show library summary
9. Show borrow log
10. Save data to JSON
11. Load data from JSON
0. Exit
Choose an option: """
    while True:
        choice = input(menu).strip()
        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            genre = input("Genre: ").strip()
            bid = add_book(title, author, genre)
            print(f"Added book with ID {bid}.")
        elif choice == "2":
            name = input("Name: ").strip()
            age = input("Age: ").strip()
            contact = input("Contact: ").strip()
            mid = register_member(name, age, contact)
            print(f"Registered member with ID {mid}.")
        elif choice == "3":
            mid = input("Member ID: ").strip()
            bid = input("Book ID: ").strip()
            print(issue_book(mid, bid))
        elif choice == "4":
            mid = input("Member ID: ").strip()
            bid = input("Book ID: ").strip()
            print(return_book(mid, bid))
        elif choice == "5":
            q = input("Search query (title or author): ").strip()
            results = search_books_by_title_or_author(q)
            print_books(results)
        elif choice == "6":
            g = input("Genre: ").strip()
            results = available_books_by_genre(g)
            print_books(results)
        elif choice == "7":
            mlist = members_with_borrowed_books()
            print_members(mlist)
        elif choice == "8":
            summary = library_summary()
            print("Library Summary:")
            for k, v in summary.items():
                print(f"  {k}: {v}")
        elif choice == "9":
            print("Borrow Log:")
            print_borrow_log()
        elif choice == "10":
            fname = input("Filename (default library_data.json): ").strip() or "library_data.json"
            save_data(fname)
            print(f"Saved data to {fname}.")
        elif choice == "11":
            fname = input("Filename (default library_data.json): ").strip() or "library_data.json"
            ok = load_data(fname)
            if ok:
                print(f"Loaded data from {fname}.")
            else:
                print(f"No file named {fname} found.")
        elif choice == "0":
            print("Thank You for Using Library Management System!!\nYou have a  GoodDay.")
            break
        else:
            print("Invalid Input. Please Try again.")


if __name__ == "__main__":
    print("===================================")
    print("Welcome to Library Management System")
    print("===================================")
    print()
    print("Options:")
    print("  1) Choose your desired action from menu")
    print("  2) Load data from JSON then run CLI")
    choice = input("Choose 1 or 2 (default 1): ").strip() or "1"
    if choice == "2":

        fname = input("Filename to load (default library_data.json): ").strip() or "library_data.json"
        if load_data(fname):
            print(f"Loaded {fname}. Entering CLI.")
            cli_menu()
        else:
            print(f"File {fname} not found. Starting empty CLI.")
            cli_menu()
    else:
        cli_menu()
