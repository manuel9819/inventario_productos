from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework import generics
# Create your views here.


#Listar usuarios
class UsuarioListAPIView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

#Eliminar usuarios
class UsuarioDeleteAPIView(generics.DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioListView(ListView):
   model= Usuario
   template_name = 'usuarios/usuario_list.html'
   context_object_name = 'usuarios'


class DemoView(ListView):
    model = Usuario
    template_name = 'usuarios/demo.html'
    context_object_name = 'usuarios'

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario-list')
    context_object_name = 'usuario'
    print("++++++++++++++++++++++++++")
    print(f"DELETE request received - Eliminando usuario")

    def form_valid(self, form):
        """"metodo moderno para la logica personalizada"""
        Usuario = self.get_object()
        print("++++++++++++++++++++++++++")
        print(f"DELETE request received - Eliminando usuario: {Usuario.nombre} (ID: {Usuario.id})")
        messages.success(self.request, f'El usuario "{Usuario.nombre}" ha sido eliminado.')
        return super().form_valid(form)



#vista para manejar
@method_decorator(csrf_exempt, name='dispatch')
class UsuarioAjaxView(generics.GenericAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        """crear nuevo usuario"""
        print("++++++++++++++++++++++++++")
        print("POST request data:")
        print(request.body)
        try:
            data ={
                'nombre': request.POST.get('nombre',),
                'email': request.POST.get('email',),
                'telefono': request.POST.get('telefono', ''),
                'descripcion': request.POST.get('descripcion', ''),
            }

            usuario = Usuario.objects.create(**data)
            print("Created usuario:", usuario.id, usuario.nombre)
            return JsonResponse({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'email': usuario.email,
                'telefono': usuario.telefono,
                'descripcion': usuario.descripcion,
                'fecha_registro': usuario.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, pk, *args, **kwargs):
        """"actualizar usuario"""
        print("PUT request data:", request.body)
        try:
            usuario = get_object_or_404(Usuario, pk=pk)

            # parsing JSON data from request body
            data = json.loads(request.body)
            print("Parsed data:", data)
            usuario.nombre = data.get('nombre', usuario.nombre)
            usuario.email = data.get('email', usuario.email)
            usuario.telefono = data.get('telefono', usuario.telefono)
            usuario.descripcion = data.get('descripcion', usuario.descripcion)
            usuario.save()
            return JsonResponse({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'email': usuario.email,
                'telefono': usuario.telefono,
                'descripcion': usuario.descripcion,
                'fecha_registro': usuario.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
