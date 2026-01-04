from django.contrib import admin
from .models import Cliente, Producto, Categoria, Pedido, DetallePedido, Libro
from .models import Contacto

# ModelAdmin para cada modelo

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'email', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('fecha_registro',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'categoria', 'precio', 'descuento', 'stock')
    search_fields = ('nombre', 'tipo', 'categoria__nombre')
    list_filter = ('tipo', 'categoria')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'total')
    search_fields = ('cliente__nombre', 'cliente__apellido')
    list_filter = ('estado', 'fecha_pedido')
    inlines = [DetallePedidoInline]

class LibroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'nombre_autor', 'saga', 'fecha_publicacion','categoria')
    search_fields = ('titulo', 'nombre_autor', 'saga','categoria')
    list_filter = ('saga','nombre_autor', 'fecha_publicacion')


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'fecha_envio')
    list_filter = ('fecha_envio',)
    search_fields = ('nombre', 'correo', 'comentario')
    
       
# =========================
# Registrar modelos en admin predeterminado
# =========================
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido) 
admin.site.register(Libro, LibroAdmin)
