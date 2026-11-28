const API_URL = "http://127.0.0.1:8100";

const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
const bookList = document.getElementById("book-list");
const addBookForm = document.getElementById("add-book-form");
const editBookForm = document.getElementById("edit-book-form");
const deleteBookForm = document.getElementById("delete-book-form");

async function loadBooks() {
    try {
        const response = await fetch(`${API_URL}/api/books`);

        if (!response.ok) {
            throw new Error("Failed to load books");
        }

        const books = await response.json();

        displayBooks(books);

    } catch (error) {
        console.error("Error loading books:", error);
        bookList.textContent = "Unable to load books. Please try again later.";
    }
}

function displayBooks(bookArray) {
    bookList.innerHTML = "";
    if (bookArray.length === 0) {
    bookList.textContent = "No books found. Try another search.";
    return;
}

    bookArray.forEach(function(book) {
        const bookCard = document.createElement("div");
        bookCard.classList.add("book-card");

        const bookId = document.createElement("p");
        bookId.textContent = "Book ID: " + book.id;
        const bookTitle = document.createElement("h3");
        bookTitle.textContent = book.title;

        const bookAuthor = document.createElement("p");
        bookAuthor.textContent = "Author: " + book.author;
        const bookCategory = document.createElement("p");
        bookCategory.textContent = "Category: " + book.category;

        bookCard.appendChild(bookId);
        bookCard.appendChild(bookTitle);
        bookCard.appendChild(bookAuthor);
        bookCard.appendChild(bookCategory);
        bookList.appendChild(bookCard);
    });
}

loadBooks();
searchButton.addEventListener("click", async function() {
    const searchTerm = searchInput.value.trim();

    if (searchTerm === "") {
        loadBooks();
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/api/books/search?keyword=${encodeURIComponent(searchTerm)}`
        );

        if (!response.ok) {
            throw new Error("Failed to search books");
        }

        const filteredBooks = await response.json();
        displayBooks(filteredBooks);

    } catch (error) {
        console.error("Error searching books:", error);
        bookList.textContent = "Unable to search books. Please try again.";
    }
});
searchInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        searchButton.click();
    }
});

addBookForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const newBook = {
        title: document.getElementById("book-title").value.trim(),
        author: document.getElementById("book-author").value.trim(),
        category: document.getElementById("book-category").value.trim()
    };

    try {
        const response = await fetch(`${API_URL}/api/books`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newBook)
        });

        if (!response.ok) {
            throw new Error("Failed to add book");
        }

        addBookForm.reset();
        loadBooks();

        alert("Book added successfully!");

    } catch (error) {
        console.error("Error adding book:", error);
        alert("Unable to add book. Please try again.");
    }
});

editBookForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const bookId = document.getElementById("edit-book-id").value;

    const updatedBook = {
        title: document.getElementById("edit-book-title").value.trim(),
        author: document.getElementById("edit-book-author").value.trim(),
        category: document.getElementById("edit-book-category").value.trim()
    };

    try {
        const response = await fetch(`${API_URL}/api/books/${bookId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedBook)
        });

        if (!response.ok) {
            throw new Error("Failed to update book");
        }

        editBookForm.reset();
        loadBooks();

        alert("Book updated successfully!");

    } catch (error) {
        console.error("Error updating book:", error);
        alert("Unable to update book. Please check the Book ID.");
    }
});

deleteBookForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const bookId = document.getElementById("delete-book-id").value;

    const confirmed = confirm(`Are you sure you want to delete book ID ${bookId}?`);

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/books/${bookId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Failed to delete book");
        }

        deleteBookForm.reset();
        loadBooks();

        alert("Book deleted successfully!");

    } catch (error) {
        console.error("Error deleting book:", error);
        alert("Unable to delete book. Please check the Book ID.");
    }
});