from django.urls import path
from .views import indicador_detalhes

urlpatterns = [

    path('indicador_detalhes/<int:indicador_man_id>/', indicador_detalhes, name='indicador_detalhes'),

]