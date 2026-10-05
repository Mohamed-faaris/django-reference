from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_form, name='student_form'),
    path('show/', views.show_students, name='show_students'),
    path('export/vcards/', views.export_vcards, name='export_vcards'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('import/csv/', views.import_csv, name='import_csv'),
]
