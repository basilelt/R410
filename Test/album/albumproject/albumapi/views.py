from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Album
from .serializers import AlbumSerializer
# from rest_framework import permissions

class AlbumListApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            title = request.GET.get('title', None)
        except:
            title = None
        if title:
            album = Album.objects.filter(titre__icontains=title) # non case sensitive
            serializer = AlbumSerializer(album, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlbumDetailApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        try:
            album = Album.objects.get(pk=id)
            serializer = AlbumSerializer(album)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Album.DoesNotExist:
            return Response({"res": "Object with id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            album = Album.objects.get(pk=id)
            album.delete()
            return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
        except Album.DoesNotExist:
            return Response({"res": "Object with id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        try:
            album = Album.objects.get(pk=id)
            serializer = AlbumSerializer(instance=album, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Album.DoesNotExist:
            return Response({"res": "Object with id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        