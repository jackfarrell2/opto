from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='nfl_index'),
    path('update-slates', views.update_slates, name='update_slates'),
    path('add-slate', views.add_slate, name='add_slate'),
    path('delete-slate/<int:slate>', views.delete_slate, name='delete_slate'),
    path('update-default-projections/<int:slate>', views.update_default_projections, name='update_default_projections'),
]