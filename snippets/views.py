from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import isOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework import renderers


# Create your views here.

#Function Based Views

"""
@csrf_exempt

@api_view(["GET", "POST"])
def snippet_list(request, format=None):

    #List all code snippets, or create a new snippet.

    if request.method == "GET":
        snippets=Snippet.objects.all()
        serializer=SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer=SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def snippet_detail(request, pk, format=None):

    #Retrieve, update or delete a code snippet.
    
    try:
        snippet=Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer=SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer=SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     
"""

#Class Based Views

"""
class SnippetList(APIView):
    def get(self, request, format=None):
        snippets=Snippet.objects.all()
        serializer=SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer=SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SnippetDetail(APIView):
    def get_object(self,pk):
        return get_object_or_404(Snippet, pk=pk)
    
    def get(self, request, pk, format=None):
        snippet=self.get_object(pk)
        serializer=SnippetSerializer(snippet)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        snippet=self.get_object(pk)
        serializer=SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        snippet=self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


#using mixins

"""
class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

"""

# using generic class-based views
"""
class SnippetList(generics.ListCreateAPIView):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly, isOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    #The create() method of our serializer will now be passed 
    #an additional 'owner' field, along with the validated data from the request.

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly, isOwnerOrReadOnly]
"""

#using a single SnippetViewSet instead of SnippetList, SnippetDetail and SnippetHightlight
class SnippetViewSet(viewsets.ModelViewSet):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly, isOwnerOrReadOnly]
    
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet=self.get_object()
        return Response(snippet.highlighted)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)





"""
class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
"""

#a single viewset for both userlist and userdetail
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset=User.objects.all()
    serializer_class=UserSerializer