from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', views.TodoViewSet)

urlpatterns = [
    path('', views.all_todos, name='index'),
    path('<int:pk>', views.todo_detail_view, name='index'),
    path('cbv/', views.ListTodosApiView.as_view(), name='index'),
    path('cbv/<int:pk>', views.TodosDetailApiView.as_view(), name='index'),
    path('mixins/', views.TodosListMixinApiView.as_view(), name='index'),
    path('mixins/<int:pk>', views.TodosDetailMixinApiView.as_view(), name='index'),
    path('generics/', views.TodosGenericApiView.as_view(), name='index'),
    path('generics/<int:pk>', views.TodosGenericDetailApiView.as_view(), name='index'),
    path('viewsets/', include(router.urls)),
    path('users/', views.UsersGenericApiView.as_view(), name='index'),
]