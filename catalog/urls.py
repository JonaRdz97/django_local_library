from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^books/$', views.VistaListaLibro.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.VistaDetalleLibro.as_view(), name='detalle-libro'),
    url(r'^authors/$', views.VistaListaAutor.as_view(), name='author'),
    url(r'^author/(?P<pk>\d+)$', views.VistaDetalleAutor.as_view(), name='detalle-autor'),
]

urlpatterns += [
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^borrowed/$', views.PrestamosBibliotecario.as_view(), name='borrowed')
]

urlpatterns += [
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns +=[
    url(r'book/create/$', views.CrearLibro.as_view(), name='book_create'),
    url(r'book/(?P<pk>\d+)/update/$', views.ActualizarLibro.as_view(), name='book_update'),
    url(r'book/(?P<pk>\d+)/delete/$', views.EliminarLibro.as_view(), name='book_delete'),
]