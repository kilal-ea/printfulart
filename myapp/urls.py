from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', views.login_view, name='login'),
    path('admin/dashboard/', views.dashboard_view, name='dashboard'),  # Protected dashboard page
    path('admin/add-book-type/', views.add_book_type, name='add_book_type'),
    path('admin/add-book/', views.add_book, name='add_book'),
    path('admin/book-types/', views.book_type_list, name='book_type_list'),
    path('admin/book-types/update/<int:pk>/', views.update_book_type, name='update_book_type'),
    path('admin/book-types/delete/<int:pk>/', views.delete_book_type, name='delete_book_type'),
    path('admin/books/', views.book_list, name='book_list'),
    path('admin/books/update/<int:pk>/', views.update_book, name='update_book'),
    path('admin/books/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('admin/commandes/list', views.commandes_list, name='commandes_list'),
    path('admin/commandes/list/<int:commande_id>/', views.commande_detail, name='commande_detail'),
    path('admin/commande/valider/<int:id>/', views.valider_commande, name='valider_commande'),


    path('', views.home, name='home'),
    path('book_search/', views.book_search, name='search_books'),
    path('commande/', views.commande, name='commande'),  # URL for printing the book
    path('commande/save', views.savecommande, name='savecommande'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)