from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SaveFile
from .serializers import SaveFileSerializer

@api_view(['GET', 'POST', 'DELETE'])
def uploaderAPI(request, username=None, gameID=None, fileName=None):

    if request.method == 'GET':
        if username and fileName and gameID:
            try:
                file = SaveFile.objects.get(username=username, fileName=fileName, gameID=gameID)
                serializer = SaveFileSerializer(file)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SaveFile.DoesNotExist:
                return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        elif username and gameID:
            files = SaveFile.objects.filter(username=username, gameID=gameID)
            serializer = SaveFileSerializer(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif username:
            files = SaveFile.objects.filter(username=username)
            serializer = SaveFileSerializer(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            files = SaveFile.objects.all()
            serializer = SaveFileSerializer(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            username = request.data["username"]
            gameID = request.data["gameID"]
            fileName = request.data["fileName"]
            saveData = request.data["saveData"]
        except KeyError:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        file, created = SaveFile.objects.update_or_create(
            username=username, gameID=gameID, fileName=fileName,
            defaults={'saveData': saveData}
        )
        return Response(
            {"status": "created" if created else "updated"},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    if request.method == 'DELETE':
        try:
            file = SaveFile.objects.get(username=username, fileName=fileName, gameID=gameID)
            file.delete()
            return Response({"status": "deleted"}, status=status.HTTP_200_OK)
        except SaveFile.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
