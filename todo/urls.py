from django.urls import path
from todo import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('/createtodo', views.createTodo, name='create'),
    path('todo/<str:pk>',views.todoView, name='todo-view'),
    path('todo-update/<str:pk>',views.todoUpdate, name='todo-update'),
    path('todo_delete/<str:pk>',views.deleteTodo, name='todo_delete'),
    # path('task/<int:pk>/toggle/', views.toggle_completion, name='toggle-completion'),
]