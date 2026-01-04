from django.urls import path
from . import views
from .views import (
    ClienteListView, ProductoListView, CategoriaListView,
    PedidoListView, DetallePedidoListView, LibroListView, 
    ClienteDetailView, ProductoDetailView, CategoriaDetailView,
    PedidoDetailView, DetallePedidoDetailView, LibroDetailView
)
from django.contrib import admin  # admin predeterminado


urlpatterns = [
   
    path("", views.index, name="index"),
    path("contacto/", views.contacto, name="contacto"),
    path("noticias/", views.noticias, name="noticias"),
    path("merchandising/", views.merchandising, name="merchandising"),
    
    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
    path("productos/", ProductoListView.as_view(), name="producto_list"),
    path("categorias/", CategoriaListView.as_view(), name="categoria_list"),
    path("pedidos/", PedidoListView.as_view(), name="pedido_list"),
    path("detallepedidos/", DetallePedidoListView.as_view(), name="detallepedido_list"),
    path("libros/", LibroListView.as_view(), name="libro_list"),
    
    path('libro/<int:libro_id>/', views.libro_detalle, name='libro_detalle'),
    path('libro/<int:libro_id>/comprar/', views.crear_pedido, name='crear_pedido'),
    path('en_construccion/', views.en_construccion, name='en_construccion'),
    
    # URLs de detalle
    path('cliente/<int:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
    path('producto/<int:pk>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('categoria/<int:pk>/', CategoriaDetailView.as_view(), name='categoria-detail'),
    path('pedido/<int:pk>/', PedidoDetailView.as_view(), name='pedido-detail'),
    path('detallepedido/<int:pk>/', DetallePedidoDetailView.as_view(), name='detallepedido-detail'),
    path('libro/<int:pk>/', LibroDetailView.as_view(), name='libro-detail'),

    path("libro/add/", views.LibroCreateView.as_view(), name="libro_add"),
    
    
    # admin básico de Django
    path('admin/', admin.site.urls),
    path('admin/dashboard/', views.dashboard, name='dashboard'), path('dashboard/', views.dashboard, name='dashboard'),
]