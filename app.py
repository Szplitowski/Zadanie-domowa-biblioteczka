from flask import Flask, request, render_template, redirect, url_for, jsonify


from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/books/", methods=["GET", "POST"])
def books_list():
    if request.method == "POST":
        data = request.get_json()
        books.create(data)
        books.save_all()
        return jsonify({"success": "Book created"}), 201

    return jsonify(books.all())


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = books.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    form = BookForm(data=book)

    if request.method == "POST":
        if form.validate_on_submit():
            books.update(book_id - 1, form.data)
        return redirect(url_for("books_list"))
    return render_template("book.html", form=form, book_id=book_id)


@app.route("/books/<int:book_id>/delete", methods=["DELETE"])
def delete_book(book_id):
    result = books.delete(book_id)
    if result:
        return jsonify({"success": "Book deleted"})
    else:
        return jsonify({"error": "Book not found"}), 404


@app.route("/books/<int:book_id>/update", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    result = books.update(book_id, data)

    if result:
        return jsonify({"success": "Book updated"})

    else:
        return jsonify({"error": "Book not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
