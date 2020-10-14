from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

#uuid requerida para las instancias de libros con ids unicos

# Create your models here.

class Genero(models.Model):
    #modelo que representa un género literario
    nombre_genero = models.CharField(max_length=200,
                                     help_text="Ingrese el nombre del género (p.ej Ciencia Ficción, Terror, etc")

    def __str__(self):
        #cadena que representa la instancia del modelo (p.ej en el sitio de administración)
        return self.nombre_genero

class Libro(models.Model):

    def muestra_genero(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genero.nombre_genero for genero in self.genero.all()[:3]])

    muestra_genero.short_description = 'Género'

    #modelo que representa un libro, no un ejemplar especifico

    titulo = models.CharField(max_length=100)

    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    resumen = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")

    ISBN = models.CharField('ISBN', max_length=13,
                            help_text="13 Caracteres <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")

    genero = models.ManyToManyField(Genero, help_text="Seleccione un género para este libro")
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.

    LENGUAJES = (
        ("E", "Español"),
        ("I", "Inglés"),
    )

    lenguaje = models.CharField(max_length=1, choices=LENGUAJES, default="E", blank=True,
                                help_text="Lenguaje en que esta escrito el libro")

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        #string que representa al modelo Libro
        return self.titulo

    def get_absolute_url(self):
        #devuelve el URL a una instancia particular de Libro
        return reverse('detalle-libro', args=[str(self.id)])

class InstanciaLibro(models.Model):
    #Modelo que representa una unica copia de un libro (p.e que puede ser prestado por biblioteca)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="ID unico para este libro en particular en toda la biblioteca")
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True)
    impreso = models.CharField(max_length=200)
    devolucion = models.DateField(null=True, blank=True)

    ESTADO_PRESTAMO = (
        ("M", "Mantenimiento"),
        ("P", "En préstamo"),
        ("D", "Disponible"),
        ("R", "Reservado"),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_PRESTAMO, blank=True, default="M",
                              help_text="Disponibilidad del libro")

    prestamo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["devolucion"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        #String para representa el objeto del modelo
        return " {0} ({1}) ".format(self.id, self.libro.titulo)

    @property
    def is_overdue(self):
        if self.devolucion and date.today() > self.devolucion:
            return True
        return False

class Autor(models.Model):
    #modelo que representa un autor
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    #fecha_muerte = models.DateField("Murió", null=True, blank=True)

    class Meta:
        ordering = ["nombre", "apellido"]
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def get_absolute_url(self):
        #retorna la URL para acceder a una instancia en particular de un autor
        return reverse("detalle-autor", args=[str(self.id)])

    def __str__(self):
        #string para representatar el objeto del modelo
        return " {0} {1} ".format(self.apellido, self.nombre)

