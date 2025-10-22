from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from productos.models import Producto
from .serializers import ProductoSerializer
from rest_framework import generics



#Listar productos
class ProductoListAPIView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

#Eliminar productos
class ProductoDeleteAPIView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoListView(ListView):
   model= Producto
   template_name = 'productos/producto_list.html'
   context_object_name = 'productos'


class DemoView(ListView):
    model = Producto
    template_name = 'productos/demo.html'
    context_object_name = 'productos'

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto-list')
    context_object_name = 'producto'

    def delete (self, request, *args, **kwargs):
        Producto = self.get_object()
        messages.success(self.request, f'El producto "{Producto.nombre}" ha sido eliminado.')
        return super().delete(request, *args, **kwargs)
    
#vista para manejar
@method_decorator(csrf_exempt, name='dispatch')
class ProductoAjaxView(generics.GenericAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def post(self, request, *args, **kwargs):
        """crear nuevo producto"""
        try:
            data ={ 
                'nombre': request.POST.get('nombre',),
                'descripcion': request.POST.get('descripcion',),
                'precio': request.POST.get('precio',),
                'cantidad': request.POST.get('cantidad',)
            }

            producto = Producto.objects.create(**data)
            print("Created product:", producto.id, producto.nombre)
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                'cantidad': producto.cantidad,
                #'creado': producto.cantidad.strftime('%d %H:%M:%S')   
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
    def put(self, request, pk, *args, **kwargs):
        """"actualizar producto"""
        print("PUT request data:", request.body)
        try:
            producto = get_object_or_404(Producto, pk=pk)

            # parsing JSON data from request body
            data = json.loads(request.body)
            print("Parsed data:", data)
            producto.nombre = data.get('nombre', producto.nombre)
            producto.descripcion = data.get('descripcion', producto.descripcion)
            producto.precio = data.get('precio', producto.precio)
            producto.cantidad = data.get('cantidad', producto.cantidad)
            producto.save()
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                'cantidad': producto.cantidad,
                #'creado': producto.cantidad.strftime('%d %H:%M:%S')   
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        


        

    


