from library import Library, Book

def main():
    lib = Library()

    while True:
        print("\n--- Kütüphane Menüsü ---")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminiz (1-5): ")

        if choice == '1':
            isbn = input("Eklenecek kitabın ISBN'i: ")
            lib.add_book_by_isbn(isbn)

        elif choice == '2':
            isbn = input("Silinecek kitabın ISBN'i: ")
            lib.remove_book(isbn)
            print("Kitap silindi.")

        elif choice == '3':
            print("\n--- Kütüphanedeki Kitaplar ---")
            lib.list_books()

        elif choice == '4':
            isbn = input("Aranacak kitabın ISBN'i: ")
            book = lib.find_book(isbn)
            if book:
                print(f"Bulunan Kitap: {book}")
            else:
                print("Bu ISBN ile bir kitap bulunamadı.")

        elif choice == '5':
            print("Uygulamadan çıkılıyor...")
            break

        else:
            print("Geçersiz seçim. Lütfen 1-5 arası bir değer girin.")

if __name__ == "__main__":
    main()