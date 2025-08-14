# Nesne Yönelimli Programlama (OOP) prensiplerini kullanarak modüler bir konsol uygulaması oluşturacağız:
## 1) Book Sınıfı : Her bir kitabın özelliklerini tanımlar
## 2) title, author ve isbn niteliklerine sahip bir __init__ metodu olmalıdır
## 3) __str__metodunu override ederek kitabı "Ulysses by james Joyce(ISBN: 978-0199535675)" şeklinde yazdıracağız

# Library Sınıfı: Tüm kütüphane operasyonlarını yönetecek.
## __init__ içinde, verilerin saklanacağı dosya adını (library.json) almalı ve kitapları tutacak boş bir liste oluşturmalıyız
## Uygulama başlar başlamaz load_books metodunu çağırarak mevcut verileri yüklemeliyiz


import httpx
from database import get_db_connection, init_db

class Book:
    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year

    def __str__(self):
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'

class Library:
    def __init__(self):
        init_db()  # Veritabanını oluşturmak için
        self.books = self.load_books()

    def load_books(self):
        conn = get_db_connection()
        books_data = conn.execute('SELECT * FROM books').fetchall()
        conn.close()
        return [Book(row['title'], row['author'], row['isbn'], row['year']) for row in books_data]
    
    def save_book(self, book:Book):
        conn = get_db_connection()
        conn.execute(
            'INSERT OR REPLACE INTO books (isbn, title, author, year) VALUES (?, ?, ?, ?)',
            (book.isbn, book.title, book.author, book.year)
        )
        conn.commit()
        conn.close()
    
    def add_book_by_isbn(self, isbn):
        """Verilen ISBN ile Open Library API'sinden kitap verilerini çeker ve kütüphaneye ekler."""
        api_url = f"https://openlibrary.org/isbn/{isbn}.json"
        try:
            response = httpx.get(api_url, follow_redirects=True)
            
            if response.status_code != 200:
                print(f"Hata: ISBN {isbn} ile kitap bulunamadı. API Durum Kodu: {response.status_code}")
                return False

            data = response.json()
            title = data.get("title", "Başlık Bilgisi Yok")
            authors = ", ".join(
                [self.get_author_name(author["key"]) for author in data.get("authors", [])]
            )
            year = data.get("publish_date", None)

            new_book = Book(title, authors, isbn, year)
            self.save_book(new_book)
            self.books.append(new_book)
            print(f"Başarıyla eklendi: {new_book}")
            return True
        except Exception as e:
            print(f"Hata: {e}")
            return False

    def get_author_name(self, author_key):
        
        try:
            url = f"https://openlibrary.org{author_key}.json"
            resp = httpx.get(url)
            if resp.status_code == 200:
                return resp.json().get("name", "Bilinmeyen Yazar")
            return "Bilinmeyen Yazar"
        except:
            return "Bilinmeyen Yazar"
        
    def find_book(self, isbn):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM books WHERE isbn=?", (isbn,)).fetchone()
        conn.close()
        if row:
            return Book(row["title"], row["author"], row["isbn"], row["year"])
        return None

    def remove_book(self, isbn):
        conn = get_db_connection()
        conn.execute("DELETE FROM books WHERE isbn=?", (isbn,))
        conn.commit()
        conn.close()
        self.books = [book for book in self.books if book.isbn != isbn]

    def update_book(self, isbn, title=None, author=None, year=None):
        conn = get_db_connection()
        book = self.find_book(isbn)
        if not book:
            return False

        new_title = title or book.title
        new_author = author or book.author
        new_year = year or book.year

        conn.execute(
            "UPDATE books SET title=?, author=?, year=? WHERE isbn=?",
            (new_title, new_author, new_year, isbn)
        )
        conn.commit()
        conn.close()
        self.books = self.load_books()
        return True

    def list_books(self):
        if not self.books:
            print("Kütüphanede hiç kitap yok.")
        for book in self.books:
            print(book)

    