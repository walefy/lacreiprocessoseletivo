from django.urls import path
from . import views


urlpatterns = [
    path('', views.examination_general_controller),
    path('/<int:examination_id>', views.examination_with_id_controller),
    path('/professional/<int:professional_id>', views.examination_with_professional_id_controller)
]
