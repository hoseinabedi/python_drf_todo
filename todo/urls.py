from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_todos, name='index'),
    path('<int:pk>', views.todo_detail_view, name='index'),
]