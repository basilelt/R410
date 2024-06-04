from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Commentaire
from .serializers import CommentaireSerializer
from rest_framework import permissions # ajouter pour l' authentification

class CommentaireListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        commentaires = Commentaire.objects.all()
        serializer = CommentaireSerializer(commentaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'titre': request.data.get('titre'),
            'commentaire': request.data.get('commentaire'),
        }
        serializer = CommentaireSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentaireDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        commentaire = Commentaire.objects.get(pk=id) # (ou id=id qui fonctionne aussi)
        if not Commentaire:
            return Response({"res": "Object with id does not exists"},
            status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CommentaireSerializer(commentaire)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id, *args, **kwargs):
        commentaire = Commentaire.objects.get(pk=id) # (ou id=id qui fonctionne aussi)
        if not commentaire:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        commentaire.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        commentaire = Commentaire.objects.get(pk=id) # (ou id=id qui fonctionne aussi)
        if not commentaire:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'titre': request.data.get('titre'),
            'commentaire': request.data.get('commentaire'),
        }
        serializer = CommentaireSerializer(instance = commentaire, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
