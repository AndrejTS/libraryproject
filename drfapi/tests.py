from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Author, Book


class AuthorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = self.get_token_for_user(self.user)
        self.author = Author.objects.create(
            first_name="John", last_name="Doe", birth_date="1970-01-01"
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_create_author(self):
        self.authenticate()
        url = reverse("author-list")
        data = {"first_name": "Jane", "last_name": "Doe", "birth_date": "1980-02-02"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(Author.objects.get(id=2).first_name, "Jane")

    def test_read_authors(self):
        url = reverse("author-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_author(self):
        self.authenticate()
        url = reverse("author-detail", kwargs={"pk": self.author.pk})
        data = {"first_name": "John", "last_name": "Smith", "birth_date": "1970-01-01"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.last_name, "Smith")

    def test_delete_author(self):
        self.authenticate()
        url = reverse("author-detail", kwargs={"pk": self.author.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class BookTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = self.get_token_for_user(self.user)
        self.author1 = Author.objects.create(
            first_name="John", last_name="Doe", birth_date="1970-01-01"
        )
        self.author2 = Author.objects.create(
            first_name="Jane", last_name="Doe", birth_date="1980-02-02"
        )
        self.book = Book.objects.create(
            title="Sample Book", isbn="1234567890123", publication_date="2020-01-01"
        )
        self.book.authors.set([self.author1, self.author2])

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_create_book(self):
        self.authenticate()
        url = reverse("book-list")
        data = {
            "title": "New Book",
            "isbn": "9876543210987",
            "publication_date": "2021-02-02",
            "author_ids": [self.author1.id],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(isbn="9876543210987").title, "New Book")

    def test_read_books(self):
        url = reverse("book-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_book(self):
        self.authenticate()
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        data = {
            "title": "Updated Book",
            "isbn": "1234567890123",
            "publication_date": "2020-01-01",
            "author_ids": [self.author2.id],
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")
        self.assertEqual(self.book.authors.count(), 1)
        self.assertEqual(self.book.authors.first().id, self.author2.id)

    def test_delete_book(self):
        self.authenticate()
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
