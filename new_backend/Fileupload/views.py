from django.shortcuts import render
#from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from zipfile import ZipFile
from .serializers import FileSerializer
import os

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    
    def post(self, request, *args, **kwargs):
      
      uploaded_file = request.data['file']
      file_serializer = FileSerializer(data=request.data)
    
      if file_serializer.is_valid():
        
          name_file = uploaded_file.name
          name_file = os.path.splitext(name_file)[0]
          with ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall('media/'+ name_file)
            #python
          return Response(name_file, status=status.HTTP_201_CREATED)
          
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



