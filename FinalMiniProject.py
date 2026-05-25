import datetime
# Models

class Book:
    def __init__(self, book_id: str, title: str, author: str, available: bool = True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.available = available


class Member:
    def __init__(self, member_id: str, name: str, email: str):
        self.member_id = member_id
        self.name = name
        self.email = email


class Loan:
    def __init__(
        self,
        loan_id: str,
        book_id: str,
        member_id: str,
        loan_date: str,
        return_date: str = None,
        is_active: bool = True
    ):
        self.loan_id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_active = is_active


# Library Service

class LibraryService:
    def __init__(self):
        self._books = {}      # key = book.book_id
        self._members = {}    # key = member.member_id
        self._loans = {}      # key = loan.loan_id
        self._loan_id_counter = 0

    # Add Book
    def add_book(self, book_id: str, title: str, author: str) -> None:
        if book_id in self._books:
            print("Error: Book ID already exists.")
            return

        book = Book(book_id, title, author, available=True)
        self._books[book_id] = book
        print(f"Book added: {title}")

    # Register Member
    def register_member(self, member_id: str, name: str, email: str) -> None:
        if member_id in self._members:
            print("Error: Member ID already exists.")
            return

        member = Member(member_id, name, email)
        self._members[member_id] = member
        print(f"Member registered: {name}")

    # Borrow Book
    def borrow_book(self, book_id: str, member_id: str) -> None:
        book = self._books.get(book_id)

        if book is None:
            print("Error: Book not found.")
            return

        member = self._members.get(member_id)

        if member is None:
            print("Error: Member not found.")
            return

        if not book.available:
            print("Error: Book is not available.")
            return

        # Create Loan
        self._loan_id_counter += 1
        loan_id = f"L{self._loan_id_counter:04d}"

        loan_date = datetime.date.today().strftime("%Y-%m-%d")

        loan = Loan(
            loan_id,
            book_id,
            member_id,
            loan_date
        )

        self._loans[loan_id] = loan

        # Update Book Availability
        book.available = False

        print(f"Book borrowed: {book.title}")

    # Return Book
    def return_book(self, book_id: str) -> None:
        book = self._books.get(book_id)

        if book is None:
            print("Error: Book not found.")
            return

        # Find active loan
        active_loan = None

        for loan in self._loans.values():
            if loan.book_id == book_id and loan.is_active:
                active_loan = loan
                break

        if active_loan is None:
            print("Error: No active loan for this book.")
            return

        # Update Loan and Book
        active_loan.is_active = False
        active_loan.return_date = datetime.date.today().strftime("%Y-%m-%d")

        book.available = True

        print(f"Book returned: {book.title}")

    # View Books
    def view_books(self) -> list:
        return list(self._books.values())

    # View Members
    def view_members(self) -> list:
        return list(self._members.values())

    # View Loans
    def view_loans(self) -> list:
        return list(self._loans.values())


# Main Program

def display_menu() -> None:
    print("\n--- Library Management System ---")
    print("1. Add Book")
    print("2. Register Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View Books")
    print("6. View Members")
    print("7. View Loans")
    print("8. Exit")


def main():
    service = LibraryService()

    while True:
        display_menu()

        choice = input("Enter your choice: ")

        # Add Book
        if choice == '1':
            book_id = input("Input Book ID: ")
            title = input("Input Book Title: ")
            author = input("Input Book Author: ")

            service.add_book(book_id, title, author)

        # Register Member
        elif choice == '2':
            member_id = input("Input Member ID: ")
            name = input("Input Member Name: ")
            email = input("Input Member Email: ")

            service.register_member(member_id, name, email)

        # Borrow Book
        elif choice == '3':
            book_id = input("Input Book ID: ")
            member_id = input("Input Member ID: ")

            service.borrow_book(book_id, member_id)

        # Return Book
        elif choice == '4':
            book_id = input("Input Book ID: ")

            service.return_book(book_id)

        # View Books
        elif choice == '5':
            books = service.view_books()

            if not books:
                print("Output: No books found.")
            else:
                print("\nOutput: Books:")

                for book in books:
                    status = "Available" if book.available else "Borrowed"

                    print(
                        f"{book.book_id} - "
                        f"{book.title} by {book.author} "
                        f"[{status}]"
                    )

        # View Members
        elif choice == '6':
            members = service.view_members()

            if not members:
                print("Output: No members found.")
            else:
                print("\nOutput: Members:")

                for member in members:
                    print(
                        f"{member.member_id} - "
                        f"{member.name} ({member.email})"
                    )

        # View Loans
        elif choice == '7':
            loans = service.view_loans()

            if not loans:
                print("Output: No loans found.")
            else:
                print("\nOutput: Loans:")

                for loan in loans:
                    status = "Active" if loan.is_active else "Returned"

                    print(
                        f"{loan.loan_id} - "
                        f"Book: {loan.book_id}, "
                        f"Member: {loan.member_id}, "
                        f"Date: {loan.loan_date}, "
                        f"Status: {status}"
                    )

        # Exit
        elif choice == '8':
            print("Output: Program closed.")
            break

        else:
            print("Invalid choice. Please try again.")


# Run Program
if __name__ == "__main__":
    main()