from django.test.client import Client
from django.urls import reverse
from django.core.files.uploadedfile import UploadedFile, SimpleUploadedFile


def test_home(client: Client):
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert b"Resume Parser" in response.content


class TestUploadResume:
    upload_resume_url = reverse("upload_resume")

    def test_upload_resume_invalid_extension(self, client: Client):
        invalid_file = SimpleUploadedFile("test.txt", b"File content")
        response = client.post(self.upload_resume_url, {"file": invalid_file}, format="multipart")
        assert response.status_code == 400
        assert "error" in response.json()

    def test_upload_pdf_file(self, client: Client, generate_pdf_file):
        with open(generate_pdf_file, "rb") as uploaded_file:
            response = client.post(self.upload_resume_url, {"file": uploaded_file}, format="multipart")
            print(response.json())
        assert response.status_code == 200
