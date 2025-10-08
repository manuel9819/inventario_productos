from django.urls import path, include
from.views import ( 
    ProductoDeleteView, DemoView, ProductoListView, ProductoAjaxView
    )

urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/<int:pk>/delete/', ProductoDeleteView.as_view(), name='producto-delete'),

    #html frontend
    path('productos/', ProductoListView.as_view(), name='producto-list-html'),
    path('productos/<int:pk>/delete/', ProductoDeleteView.as_view(), name='producto-delete-html'),
    path('demo/',DemoView.as_view(), name='demo'),
    path('', ProductoListView.as_view(), name='home'),#pagina principal

    #ajax endpoint para el frontend
    path('ajax/productos/', ProductoAjaxView.as_view(), name='producto-ajax'),
    path('ajax/productos/<int:pk>', ProductoDeleteView.as_view(), name='producto-ajax-detail'),
]