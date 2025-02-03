from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from csv_app.models import User

class CSVUploadTest(TestCase):
    def setUp(self):
        """Set up the test client before each test"""
        self.client = APIClient()

    def test_upload_valid_csv(self):
        """Test uploading a valid CSV file"""
        csv_data = b"name,email,age\nJohn Doe,john@example.com,30\nJane Doe,jane@example.com,25"
        csv_file = SimpleUploadedFile("test.csv", csv_data, content_type="text/csv")

        response = self.client.post('/api/upload/', {'file': csv_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)  # Should save 2 users

    def test_upload_invalid_csv(self):
        """Test uploading an invalid CSV file (invalid age and email)"""
        csv_data = b"name,email,age\nJohn Doe,john@example.com,130\nInvalid User,invalid_email,25"
        csv_file = SimpleUploadedFile("test.csv", csv_data, content_type="text/csv")

        response = self.client.post('/api/upload/', {'file': csv_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)  # No valid users should be saved

    def test_upload_duplicate_email(self):
        """Test that duplicate emails are ignored"""
        csv_data = b"name,email,age\nJohn Doe,john@example.com,30\nDuplicate,john@example.com,40"
        csv_file = SimpleUploadedFile("test.csv", csv_data, content_type="text/csv")

        response = self.client.post('/api/upload/', {'file': csv_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)  # Only the first user should be saved

    def test_upload_non_csv_file(self):
        """Test that only .csv files are allowed"""
        txt_data = b"This is a test text file"
        txt_file = SimpleUploadedFile("test.txt", txt_data, content_type="text/plain")

        response = self.client.post('/api/upload/', {'file': txt_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Only .csv files are allowed")
