from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Gare
from .serializers import GareSerializer
from rest_framework import permissions

class GareListApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            departement = request.GET['departement']
        except:
            departement = None
            
        if departement:
            gares = Gare.objects.filter(code_postal__startswith=departement)
            serializer = GareSerializer(gares, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        gares = Gare.objects.all()
        serializer = GareSerializer(gares, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            gares = []
            for item in data:
                serializer = GareSerializer(data=item)
                if serializer.is_valid():
                    gare = serializer.save()
                    gares.append(gare)
            serializer = GareSerializer(gares, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        serializer = GareSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GareDetailApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        gare = Gare.objects.get(pk=id)
        if not gare:
            return Response({"res": "Object with id does not exists"},
            status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GareSerializer(gare)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id, *args, **kwargs):
        gare = Gare.objects.get(pk=id)
        if not gare:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        gare.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        gare = Gare.objects.get(pk=id)
        if not gare:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'nom': request.data.get('nom'),
            'ville': request.data.get('ville'),
            'code_postal': request.data.get('code_postal'),
            'nb_quais': request.data.get('nb_quais'),
            'date_construction': request.data.get('date_construction'),
        }
        serializer = GareSerializer(instance = gare, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)