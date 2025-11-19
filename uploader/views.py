from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import SaveFile
from .serializers import SaveFileSerializer
import json

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def uploaderAPI(request):
    try:
        username = request.data["username"]
        gameID = request.data["gameID"]
        fileName = request.data["fileName"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        try:
            file = SaveFile.objects.get(username=username, gameID=gameID, fileName=fileName)
            serializer = SaveFileSerializer(file)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'POST':
        try:
            saveData = request.data["saveData"]
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            file = SaveFile.objects.get(username=username, gameID=gameID, fileName=fileName)
            file.saveData = saveData
            file.save()
            return Response(status=status.HTTP_200_OK)
        except:
            file = SaveFile(username=username, gameID=gameID, fileName=fileName, saveData=saveData)
            file.save()
            return Response(status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        try:
            file = SaveFile.objects.get(username=username, gameID=gameID, fileName=fileName)
            file.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)