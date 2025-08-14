from library import Library
import os

def test_full_flow():
    test_isbn = "978-0321765723"  # The C++ Programming Language

    lib = Library()

    # 1. Kitap ekleme testi
    success = lib.add_book_by_isbn(test_isbn)
    assert success is True

    # 2. Kitap bulma testi
    found_book = lib.find_book(test_isbn)
    assert found_book is not None
    assert found_book.isbn == test_isbn

    # 3. Kitap silme testi
    lib.remove_book(test_isbn)
    assert lib.find_book(test_isbn) is None
