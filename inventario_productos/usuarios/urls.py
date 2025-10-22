from django.urls import path, include
from .views import (
    UsuarioDeleteView, DemoView, UsuarioListView, UsuarioAjaxView
    )

urlpatterns = [
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'),
    path('usuarios/<int:pk>/delete/', UsuarioDeleteView.as_view(), name='usuario-delete'),

    #html frontend
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list-html'),
    path('usuarios/<int:pk>/delete/', UsuarioDeleteView.as_view(), name='usuario-delete-html'),
    path('demo/',DemoView.as_view(), name='demo'),
    path('', UsuarioListView.as_view(), name='home'),#pagina principal

    #ajax endpoint para el frontend
    path('ajax/usuarios/', UsuarioAjaxView.as_view(), name='usuario-ajax'),
    path('ajax/usuarios/<int:pk>/', UsuarioAjaxView.as_view(), name='usuario-ajax-detail'),
]