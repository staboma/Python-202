import pytest
from fastapi.testclient import TestClient
from api import app
from database import init_db, get_db_connection

client = TestClient(app)

# Testlerde kullanılacak ISBN
TEST_ISBN = "9780134494166"  

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    
    init_db()
    conn = get_db_connection()
    conn.execute("DELETE FROM books")
    conn.commit()
    conn.close()
    yield
    
    conn = get_db_connection()
    conn.execute("DELETE FROM books")
    conn.commit()
    conn.close()

def test_add_book():
    response = client.post(f"/books/{TEST_ISBN}")
    assert response.status_code == 200
    assert "Kitap eklendi" in response.json()["message"]

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    books = response.json()["books"]
    assert any(book["isbn"] == TEST_ISBN for book in books)

def test_update_book():
    new_data = {"title": "Clean Architecture - Updated", "author": "Robert C. Martin"}
    response = client.put(f"/books/{TEST_ISBN}", json=new_data)
    assert response.status_code == 200
    assert "Kitap güncellendi" in response.json()["message"]

def test_delete_book():
    response = client.delete(f"/books/{TEST_ISBN}")
    assert response.status_code == 200
    assert "Kitap silindi" in response.json()["message"]

    
    response = client.get("/books")
    books = response.json()["books"]
    assert all(book["isbn"] != TEST_ISBN for book in books)
