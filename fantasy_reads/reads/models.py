from django.db import models
from django.utils import timezone
from django.urls import reverse


class Libro(models.Model):
    titulo = models.CharField(
        max_length=100, 
        help_text="Ingresa título del libro"
    )
    nombre_autor = models.CharField(
        max_length=100, 
        help_text="Ingresa nombre del autor del libro"
    )
    saga = models.BooleanField(
        default=False, 
        help_text="¿Es el libro parte de una saga?"
    )
    saga_nombre = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Nombre de la saga (si aplica)"
    )
    cantidad_saga = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Número total de libros en la saga"
    )
    saga_terminada = models.BooleanField(
        default=False,
        help_text="¿La saga está terminada?"
    )
    sinopsis = models.TextField(
        null=True, 
        blank=True, 
        help_text="Ingresa una sinopsis del libro"
    )
    fecha_publicacion = models.DateField(
        blank=True, 
        null=True,
        help_text="Fecha de publicación del libro"
    )
    categoria = models.ForeignKey(
        'Categoria', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Selecciona la categoría"
    )
    portada = models.ImageField(
        upload_to='portadas/', 
        null=True, 
        blank=True,
        help_text="Sube una portada para el libro"
    )
    calificacion_trama = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], 
        default=3,
        help_text="Calificación de la trama (1 a 5)"
    )
    nivel_spicy = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], 
        default=1,
        help_text="Nivel de spicy (1 a 5)"
    )
    linkGoodreads = models.URLField(
        max_length=300, 
        null=True, 
        blank=True, 
        help_text="Link del libro en Goodreads"
    )

    class Meta:
        db_table = "Libro"
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self):
        return f"{self.titulo} - {self.nombre_autor}"
    
    def get_absolute_url(self):
        return reverse("libro-detail", args =[str(self.id)])

    
    

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_absolute_url(self):
        return reverse("cliente-detail", args =[str(self.id)])
    

 
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre   
    
    def get_absolute_url(self):
        return reverse("categoria-detail", args =[str(self.id)])
    
    
class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('libro', 'Libro'),
        ('merch', 'Merchandising'),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # porcentaje
    stock = models.PositiveIntegerField(default=0)
    tipo = models.CharField(max_length=10, choices=TIPO_PRODUCTO, default='libro')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    @property
    def precio_final(self):
        return self.precio * (1 - self.descuento / 100)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("producto-detail", args =[str(self.id)])
    

class Pedido(models.Model):
    ESTADO_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_PEDIDO, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"

    def actualizar_total(self):
        total = sum([detalle.subtotal for detalle in self.detallepedido_set.all()])
        self.total = total
        self.save()
        
    def get_absolute_url(self):
        return reverse("pedido-detail", args =[str(self.id)])
    

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio_final

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Reducir stock automáticamente
        self.producto.stock = max(0, self.producto.stock - self.cantidad)
        self.producto.save()
        self.pedido.actualizar_total()
        
    def get_absolute_url(self):
        return reverse("detallepedido-detail", args =[str(self.id)])
    
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    comentario = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Contacto"
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return f"{self.nombre} - {self.correo}"
