from datetime import date, timedelta


class Book:
    def __init__(self, title):
        self.title = title
        self.on_shelf = True


class Rules:
    loan_days = 14
    max_books = 3
    fine_per_day = 0.50

    def due_date(self, today):
        return today + timedelta(days=self.loan_days)

    def fine(self, due_date, today):
        late = (today - due_date).days
        if late < 0:
            late = 0
        return round(late * self.fine_per_day, 2)


class BorrowService:
    def __init__(self, books, rules):
        self.books = books
        self.rules = rules
        self.loans = []

    def borrow(self, member_id, book_id, today):
        book = self.books[book_id]
        if not book.on_shelf:
            return book.title + " is already borrowed"
        if len(self.my_books(member_id)) >= self.rules.max_books:
            return "The student already has " + str(self.rules.max_books) + " books"
        due = self.rules.due_date(today)
        self.loans.append([book_id, member_id, due])
        book.on_shelf = False
        return book.title + " -> return before " + str(due)

    def return_book(self, book_id, today):
        for loan in self.loans:
            if loan[0] == book_id:
                self.loans.remove(loan)
                self.books[book_id].on_shelf = True
                return "Fine = " + str(self.rules.fine(loan[2], today)) + " SAR"
        return "This book is not borrowed"

    def my_books(self, member_id):
        titles = []
        for loan in self.loans:
            if loan[1] == member_id:
                titles.append(self.books[loan[0]].title)
        return titles


books = {
    "B1": Book("Clean Code"),
    "B2": Book("Python Programming"),
    "B3": Book("Data Structures"),
    "B4": Book("Design Patterns"),
}

desk = BorrowService(books, Rules())
today = date(2026, 9, 16)

print(desk.borrow("S2203", "B1", today))
print(desk.borrow("S2203", "B2", today))
print(desk.borrow("S2203", "B3", today))
print(desk.borrow("S2203", "B4", today))
print(desk.borrow("S3010", "B1", today))
print("Books of S2203:", desk.my_books("S2203"))
print(desk.return_book("B1", today + timedelta(days=10)))
print(desk.return_book("B2", today + timedelta(days=18)))
