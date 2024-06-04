from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer

class ClientListApiView(APIView):    
    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        data = serializer.data
        for item in data:
            item.pop('identifiant', None)
            item.pop('mot_de_passe', None)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'genre': request.data.get('genre'),
            'nom': request.data.get('nom'),
            'prenom': request.data.get('prenom'),
            'identifiant': request.data.get('identifiant'),
            'mot_de_passe': request.data.get('mot_de_passe'),
            'adresse': request.data.get('adresse'),
            'mail': request.data.get('mail'),
            'telephone': request.data.get('telephone'),
        }
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data.pop('identifiant', None)
            data.pop('mot_de_passe', None)
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDetailApiView(APIView):
    def get(self, request, id, *args, **kwargs):
        client = Client.objects.get(pk=id)
        if not client:
            return Response({"res": "Object with id does not exists"},
            status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClientSerializer(client)
        data = serializer.data
        data.pop('identifiant', None)
        data.pop('mot_de_passe', None)
        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request, id, *args, **kwargs):
        client = Client.objects.get(pk=id)
        if not client:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'identifiant': request.data.get('identifiant'),
            'mot_de_passe': request.data.get('mot_de_passe'),
        }
        if data['identifiant'] != client.identifiant or data['mot_de_passe'] != client.mot_de_passe:
            return Response(
                {"res": "Identifiant or mot_de_passe is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        client.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        client = Client.objects.get(pk=id)
        if not client:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'genre': request.data.get('genre'),
            'nom': request.data.get('nom'),
            'prenom': request.data.get('prenom'),
            'identifiant': request.data.get('identifiant'),
            'mot_de_passe': request.data.get('mot_de_passe'),
            'adresse': request.data.get('adresse'),
            'mail': request.data.get('mail'),
            'telephone': request.data.get('telephone'),
        }
        if data['identifiant'] != client.identifiant or data['mot_de_passe'] != client.mot_de_passe:
            return Response(
                {"res": "Identifiant or mot_de_passe is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClientSerializer(instance = client, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data.pop('identifiant', None)
            data.pop('mot_de_passe', None)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id, *args, **kwargs):
        client = Client.objects.get(pk=id)
        if not client:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'identifiant': request.data.get('identifiant'),
            'mot_de_passe': request.data.get('mot_de_passe'),
        }
        if data['identifiant'] != client.identifiant or data['mot_de_passe'] != client.mot_de_passe:
            return Response(
                {"res": False},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"res": True}, status=status.HTTP_200_OK)
