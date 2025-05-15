from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_form, name='student_form'),
    path('show/', views.show_students, name='show_students'),
]
