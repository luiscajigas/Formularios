from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('', views.AsistenciaListView.as_view(), name='list'),
    path('create/', views.AsistenciaCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.AsistenciaDetailView.as_view(), name='detail'),
    path('<uuid:pk>/update/', views.AsistenciaUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', views.AsistenciaDeleteView.as_view(), name='delete'),
]
