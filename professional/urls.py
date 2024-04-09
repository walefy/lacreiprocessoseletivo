from django.urls import path
from . import views


urlpatterns = [
    path('', views.professional_general_controller),
    path('/<int:professional_id>', views.professional_with_id_controller)
]
