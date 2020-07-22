from django.urls import path
# from django.views.generic import RedirectView
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add_item, name='add'),
    path('complete/<todo_id>', views.completeTodo, name='complete'),
    path('delete/<todo_id>', views.delete, name='delete')
]
