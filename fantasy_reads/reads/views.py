from django.shortcuts import render
from datetime import datetime
from django.views import generic
from .models import Cliente, Producto, Categoria, Pedido, DetallePedido, Libro, Contacto
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from .forms import ContactoForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils.google_books import get_similar_books_by_author, get_similar_books_by_title
#decoradores
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "reads/index.html")

@login_required
def contacto(request):
    mensaje = ""
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = "Gracias por contactarnos. Tu mensaje fue enviado."
            form = ContactoForm()  # Limpiar el formulario después de enviar
    else:
        form = ContactoForm()
    
    contexto = {
        "form": form,
        "titulo": "Formulario de Contacto",
        "mensaje": mensaje
    }
    return render(request, "reads/contacto.html", contexto)
def noticias(request):
    noticias = [
        {
            "titulo": "Próxima reunión de la comunidad:",
            "descripcion": "Estamos organizando la próxima reunión de la comunidad que se realizará en el Café Literario de Parque Bustamante en Providencia. ¡Déjanos tu mail para enviarte toda la información!",
            "imagen": "reads/images/club-lectura.jpeg", 
            "tipo": "formulario",  
            "enlace": ""
        },
        {
            "titulo": "La esperada tercera parte de fourth wing llegará en enero de 2025",
            "descripcion": 'Los fans de Rebecca Yarros podrán disfrutar de la tercera "Onyx Storm", a principios del 2025.',
            "imagen": "reads/images/onyx-storm-cover.jpg",
            "tipo": "noticia",
            "enlace": "https://abcnews.go.com/GMA/Culture/onyx-storm-highly-anticipated-fourth-wing-author-rebecca/story?id=112114732"
        },
        {
            "titulo": 'Serie basada en "ACOTAR" fue cancelada para Hulu',
            "descripcion": "La serie ACOTAR ha sido oficialmente cancelada en Hulu, Maas está buscando asegurar los derechos en otro lugar.",
            "imagen": "reads/images/sarahjmaas-acotar.png",
            "tipo": "noticia",
            "enlace": "https://www.20minutos.es/cinemania/series/corte-rosas-espinas-acotar-cancelada-adaptacion-fenomeno-literario-fantasia-5683149/-hulu-rodaje-2025"
        },
        {
            "titulo": "Dilema:",
            "descripcion": "La fuerza del fenómeno es tal que el dilema planea sobre muchas familias con adolescentes y preadolescentes: ¿es mejor que sus hijas –el fenómeno es básicamente femenino– devoren libros con escenas ardientes que suelen resbalar hacia amores tóxicos y clichés tradicionales a que no lean nada? (...)",
            "imagen": "reads/images/chica-leyendo.jpg",
            "tipo": "noticia",
            "enlace": "https://www.elperiodico.com/es/sociedad/20241005/novelas-romanticas-alto-voltaje-prenden-adolescentes-mejor-lean-eso-a-nada-107959557/anahuangofficial"
        },
    ]

    contexto = {
        "titulo_pagina": "Noticias",
        "noticias": noticias
    }

    return render(request, "reads/noticias.html", contexto)


class ClienteListView(generic.ListView):
    model = Cliente
    template_name = 'reads/cliente_list.html'
    context_object_name = 'clientes'
    
class ProductoListView(generic.ListView):
    model = Producto
    template_name = 'reads/producto_list.html'
    context_object_name = 'productos'

class CategoriaListView(generic.ListView):
    model = Categoria
    template_name = 'reads/categoria_list.html'
    context_object_name = 'categorias'

class PedidoListView(generic.ListView):
    model = Pedido
    template_name = 'reads/pedido_list.html'
    context_object_name = 'pedidos'

class DetallePedidoListView(generic.ListView):
    model = DetallePedido
    template_name = 'reads/detallepedido_list.html'
    context_object_name = 'detallepedidos'

class LibroListView(generic.ListView):
    model = Libro
    template_name = 'reads/libro_list.html'
    paginate_by = 4

#Vistas de detalle

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'reads/cliente_detail.html'
    context_object_name = 'cliente'

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'reads/producto_detail.html'
    context_object_name = 'producto'

class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'reads/categoria_detail.html'
    context_object_name = 'categoria'

class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'reads/pedido_detail.html'
    context_object_name = 'pedido'

class DetallePedidoDetailView(DetailView):
    model = DetallePedido
    template_name = 'reads/detallepedido_detail.html'
    context_object_name = 'detallepedido'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'reads/libro_detail.html'
    context_object_name = 'libro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro = self.get_object()

        # Buscar libros similares por autor o título
        similares = []
        if libro.autor:
            similares = get_similar_books_by_author(libro.autor)
        elif libro.titulo:
            # alternativa si no hay autor
            from .utils.google_books import get_similar_books_by_title
            similares = get_similar_books_by_title(libro.titulo)

        context['similares'] = similares
        return context
    
def libro_detalle(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    # Buscar libros similares desde la API de Google Books
    similares = []
    if libro.nombre_autor:
        similares = get_similar_books_by_author(libro.nombre_autor, max_results=6)
    elif libro.titulo:
        similares = get_similar_books_by_title(libro.titulo, max_results=6)

    return render(request, 'reads/libro_detalle.html', {
        'libro': libro,
        'similares': similares
    })

def merchandising(request):
    productos = Producto.objects.all()
    contexto = {
        "titulo_pagina": "Merchandising",
        "productos": productos
    }
    return render(request, "reads/merchandising.html", contexto)

def crear_pedido(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    # Lógica de crear pedido
    # Redirigir a página de en construcción
    return redirect('en_construccion')

def dashboard(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_productos': Producto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_pedidos': Pedido.objects.count(),
        'total_libros': Libro.objects.count(),
        'total_contactos': Contacto.objects.count(),
        
    }
    return render(request, 'admin/dashboard.html', context)

def en_construccion(request):
    return render(request, "reads/en_construccion.html")

class LibroCreateView(CreateView):
    model = Libro
    fields = '__all__'
    initial = {'stock' : 0, 'precio': 0, }