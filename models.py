import json


class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        book = [book for book in self.books if book["id"] == id]
        if book:
            return book[0]
        return None

    def create(self, data):
        data.pop("csrf_token")
        self.books.append(data)

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        data.pop("csrf_token")
        self.books[id] = data
        self.save_all()

    def delete(self, id):
        book = self.get(id)
        if not book:
            return False
        self.books.remove(book)
        self.save_all()
        return True


books = Books()
