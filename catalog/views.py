from django.shortcuts import render
from .models import Autor, Libro, InstanciaLibro, Genero
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Autor

# Create your views here.

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_books = Libro.objects.all().count()
    num_instances = InstanciaLibro.objects.all().count()
    # Libros disponibles (status = 'd')
    num_instances_available = InstanciaLibro.objects.filter(estado__exact='D').count()
    num_authors = Autor.objects.count()  # El 'all()' esta implícito por defecto.
    num_genre = Genero.objects.all().count()
    num_specific_word = Libro.objects.filter(titulo__exact='1984').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_genre': num_genre, 'num_specific_word': num_specific_word,
                 'num_visits': num_visits}  # num_visits appended
    )

class VistaListaLibro(generic.ListView):
    model = Libro
    context_object_name = 'lista_libros'
    paginate_by = 2

class VistaDetalleLibro(generic.DetailView):
    model = Libro

class VistaListaAutor(generic.ListView):
    model = Autor
    context_object_name = "lista_autor"

class VistaDetalleAutor(generic.DetailView):
    model = Autor


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = InstanciaLibro
    context_object_name = "instancia_libro"
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return InstanciaLibro.objects.filter(prestamo=self.request.user).filter(estado__exact='P').order_by('devolucion')

class PrestamosBibliotecario(LoginRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = InstanciaLibro
    context_object_name = "libro_inst"
    template_name = "catalog/borrowed_books.html"
    paginate_by = 10

    def get_queryset(self):
        return InstanciaLibro.objects.filter(estado__exact='P').order_by('devolucion')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(InstanciaLibro, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['fecha_renovacion']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'fecha_renovacion': proposed_renewal_date})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(CreateView, LoginRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Autor
    fields = '__all__'
    initial = {'fecha_nacimiento': '05/01/2018'}


class AuthorUpdate(UpdateView, LoginRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Autor
    fields = ['nombre', 'apellido', 'fecha_nacimiento']


class AuthorDelete(DeleteView, LoginRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Autor
    success_url = reverse_lazy('author')

class CrearLibro(CreateView, LoginRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Libro
    fields = '__all__'

class ActualizarLibro(UpdateView, LoginRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Libro
    fields = '__all__'

class EliminarLibro(DeleteView, LoginRequiredMixin):
    permission_required = 'catalog.can_mark_returned'
    model = Libro
    success_url = reverse_lazy('books')
