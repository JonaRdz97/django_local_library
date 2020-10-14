from django.contrib import admin
from .models import Genero, Autor, InstanciaLibro, Libro

# Register your models here.

admin.site.register(Genero)
#admin.site.register(Autor)
#admin.site.register(InstanciaLibro)
#admin.site.register(Libro)

# Define the admin class
class AutorAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "fecha_nacimiento")
    #El atributo fields lista solo los campos que se van a desplegar en el formulario, en orden.
    fields = [("nombre", "apellido"), "fecha_nacimiento"]


# Register the admin class with the associated model
admin.site.register(Autor, AutorAdmin)

class InstanciaLibroInline(admin.TabularInline):
    model = InstanciaLibro

# Register the Admin classes for Book using the decorator
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "muestra_genero")
    inlines = [InstanciaLibroInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(InstanciaLibro)
class InstanciaLibroAdmin(admin.ModelAdmin):
    list_filter = ("estado", "devolucion")
    list_display = ("libro", "estado", "devolucion", "id", "prestamo")

    #vistas en detalle
    fieldsets = (
        (None, {
            'fields': ('libro', 'impreso', 'id')
        }),
        ('Disponibilidad', {
            'fields': ('estado', 'devolucion', 'prestamo')
        }),
    )


