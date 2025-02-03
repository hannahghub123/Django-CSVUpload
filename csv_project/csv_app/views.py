import csv
import io
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UploadCSVView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.csv'):
            return Response({"error": "Only .csv files are allowed"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        valid_records = 0
        invalid_records = 0
        errors = []

        for row in reader:
            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                if not User.objects.filter(email=row['email']).exists():
                    serializer.save()
                    valid_records += 1
                else:
                    errors.append({"email": row['email'], "error": "Duplicate email"})
                    invalid_records += 1
            else:
                invalid_records += 1
                errors.append({"row": row, "errors": serializer.errors})

        # JSON response data
        response_data = {
            "success": valid_records,
            "failed": invalid_records,
            "errors": errors
        }

        # Save response data to a JSON file
        json_file_path = "api_response.json"  # Change this path as needed
        with open(json_file_path, "w") as json_file:
            json.dump(response_data, json_file, indent=4)

        return Response(response_data, status=status.HTTP_200_OK)
