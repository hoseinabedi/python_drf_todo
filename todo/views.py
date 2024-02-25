from django.shortcuts import render
from .models import Todo
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import TodoSerializer
from rest_framework.views import APIView
from rest_framework import mixins, generics

# Create your views here.

# region function base view

@api_view(['GET', 'POST'])
def all_todos(request: Request) -> Response:
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(None, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_view(request: Request, pk: int) -> Response:
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(None, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        todo.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
#endregion
    
# region class base view
class ListTodosApiView(APIView):
    def get(self, request: Request) -> Response:
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request: Request) -> Response:
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodosDetailApiView(APIView):
    def get_object(self, pk: int) -> Todo:
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
    def get(self, request: Request, pk: int) -> Response:
        todo = self.get_object(pk=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request: Request, pk: int) -> Response:
        todo = self.get_object(pk=pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, pk: int) -> Response:
        todo = self.get_object(pk=pk)
        todo.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
# endregion
    
# region mixins
class TodosListMixinApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)
    
    def post(self, request: Request) -> Response:
        return self.create(request)

class TodosDetailMixinApiView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk=pk)
    
    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk=pk)
    
    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk=pk)
# endregion
    
# region generic views
class TodosGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodosGenericDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer 
#endregion