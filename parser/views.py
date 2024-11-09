from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError

from .validators import validate_file_extension, validate_file_size
from .utils import read_uploaded_file


def home(request: HttpRequest):
    return render(request, 'index.html')


def upload_resume(request: HttpRequest):
    if request.method == "POST" and request.FILES.get("file"):
        file: UploadedFile = request.FILES["file"]
        try:
            ext: str = validate_file_extension(file)
            validate_file_size(file)
            file_content = read_uploaded_file(file, ext)
            print("file_content>>", file_content)
        except ValidationError as err:
            return JsonResponse({"error": err.message})
    return JsonResponse({"error": "Invalid Request"}, status=400)
