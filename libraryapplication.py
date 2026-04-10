class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.borrowed_by = None
        self.reserved_by = None

    def __str__(self):
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {status}"


class User:
    def __init__(self, username, password, resident=True):
        self.username = username
        self.password = password
        self.borrowed_books = []
        self.reservations = []
        self.resident = resident  # Must be True (Australian resident condition)

    def can_borrow(self):
        return len(self.borrowed_books) < 2


class Library:
    def __init__(self):
        self.books = []
        self.users = {}

    # ---------------- USER FUNCTIONS ----------------
    def register_user(self, username, password, resident=True):
        if not resident:
            print("❌ Only Australian residents can register.")
            return

        if username in self.users:
            print("❌ Username already exists.")
        else:
            self.users[username] = User(username, password, resident)
            print("✅ Registration successful.")

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            print("✅ Login successful.")
            return user
        print("❌ Invalid credentials.")
        return None

    # ---------------- BOOK FUNCTIONS ----------------
    def add_book(self, title, author, isbn):
        self.books.append(Book(title, author, isbn))
        print("✅ Book added.")

    def search_books(self, keyword):
        results = [
            book for book in self.books
            if keyword.lower() in book.title.lower()
            or keyword.lower() in book.author.lower()
            or keyword == book.isbn
        ]

        if results:
            for book in results:
                print(book)
        else:
            print("❌ No books found.")

    # ---------------- BORROW ----------------
    def borrow_book(self, user, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if not book.available:
                    print("❌ Book not available.")
                    return

                if not user.can_borrow():
                    print("❌ Borrowing limit reached (2 books).")
                    return

                book.available = False
                book.borrowed_by = user.username
                user.borrowed_books.append(book)
                print("✅ Book borrowed successfully.")
                return

        print("❌ Book not found.")

    # ---------------- RETURN ----------------
    def return_book(self, user, isbn):
        for book in user.borrowed_books:
            if book.isbn == isbn:
                book.available = True
                book.borrowed_by = None
                user.borrowed_books.remove(book)

                # Notify reservation
                if book.reserved_by:
                    print(f"📢 Book reserved by {book.reserved_by} is now available!")

                print("✅ Book returned.")
                return

        print("❌ You don’t have this book.")

    # ---------------- RESERVE ----------------
    def reserve_book(self, user, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.available:
                    print("❌ Book is available, no need to reserve.")
                    return

                book.reserved_by = user.username
                user.reservations.append(book)
                print("✅ Book reserved.")
                return

        print("❌ Book not found.")


# ---------------- MAIN PROGRAM ----------------
library = Library()

# Add sample books
library.add_book("Harry Potter", "J.K. Rowling", "111")
library.add_book("The Hobbit", "J.R.R. Tolkien", "222")

while True:
    print("\n1. Register\n2. Login\n3. Exit")
    choice = input("Choose: ")

    if choice == "1":
        u = input("Username: ")
        p = input("Password: ")
        res = input("Are you an Australian resident? (yes/no): ").lower() == "yes"
        library.register_user(u, p, res)

    elif choice == "2":
        u = input("Username: ")
        p = input("Password: ")
        user = library.login(u, p)

        if user:
            while True:
                print("\n1. Search Book\n2. Borrow\n3. Return\n4. Reserve\n5. Logout")
                opt = input("Choose: ")

                if opt == "1":
                    key = input("Enter keyword: ")
                    library.search_books(key)

                elif opt == "2":
                    isbn = input("Enter ISBN: ")
                    library.borrow_book(user, isbn)

                elif opt == "3":
                    isbn = input("Enter ISBN: ")
                    library.return_book(user, isbn)

                elif opt == "4":
                    isbn = input("Enter ISBN: ")
                    library.reserve_book(user, isbn)

                elif opt == "5":
                    break

    elif choice == "3":
        break