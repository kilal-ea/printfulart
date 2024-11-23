from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import BookType, Book, Image  ,Commande


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            # Redirect to dashboard after successful login
            return redirect('dashboard')
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # Stay on login page

    return render(request, 'dash/login.html')  # Render login page for GET requests


@login_required
def add_book_type(request):
    print('eee')
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            # Create a new BookType record
            BookType.objects.create(name=name)
            messages.success(request, 'Book Type added successfully')  # Success message
            return redirect('dashboard')  # Redirect back to dashboard or another page
    return render(request, 'dash/addtype.html')  # Render the form if GET request

# Dashboard view (only accessible to authenticated users)

@login_required
def dashboard_view(request):
    return render(request, 'dash/dashboard.html')  # You can customize the dashboard page







def book_type_list(request):
    book_types = BookType.objects.all()
    return render(request, 'dash/book_type_list.html', {'book_types': book_types})

# Update a book type
def update_book_type(request, pk):
    book_type = get_object_or_404(BookType, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            book_type.name = name
            book_type.save()
            messages.success(request, 'Book Type updated successfully')
            return redirect('book_type_list')
    return render(request, 'dash/update_book_type.html', {'book_type': book_type})

# Delete a book type
def delete_book_type(request, pk):
    book_type = get_object_or_404(BookType, pk=pk)
    if request.method == 'POST':
        book_type.delete()
        messages.success(request, 'Book Type deleted successfully')
    return redirect('book_type_list')


# List all books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'dash/book_list.html', {'books': books})


# Update a book
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_types = BookType.objects.all()
    images = book.images.all()  # Fetching images related to the book

    if request.method == 'POST':
        # Handle form data and image upload
        name = request.POST.get('name')
        description = request.POST.get('description')
        link = request.POST.get('link')
        book_type_id = request.POST.get('book_type')

        if name and description and link and book_type_id:
            book.name = name
            book.description = description
            book.link = link
            book.book_type = get_object_or_404(BookType, pk=book_type_id)

            # Handling image uploads
            if 'images' in request.FILES:
                for img in request.FILES.getlist('images'):
                    Image.objects.create(book=book, image=img)

            book.save()
            messages.success(request, 'Book updated successfully')
            return redirect('book_list')

    return render(request, 'dash/update_book.html', {'book': book, 'book_types': book_types, 'images': images})


# Delete a book
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully')
    return redirect('book_list')


@login_required
def add_book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        link = request.POST.get('link')
        book_type_id = request.POST.get('book_type')

        # Create the Book instance
        book = Book.objects.create(
            name=name,
            description=description,
            link=link,
            book_type_id=book_type_id
        )

        cover_set = False  # Track if a cover image was set
        # Save uploaded images
        for i, image_file in enumerate(request.FILES.getlist('images')):
            cover = request.POST.get(f'cover_{i}') == 'on'  # Check if this image is marked as the cover
            image = Image.objects.create(book=book, image=image_file, cover=cover)

            if cover:
                cover_set = True

        # If no cover image was selected, set the first image as the cover
        if not cover_set and book.images.exists():
            first_image = book.images.first()
            first_image.cover = True
            first_image.save()

        return redirect('book_list')  # Redirect to a page of your choice

    # For GET requests, render the form with existing book types
    book_types = BookType.objects.all()
    return render(request, 'dash/add_book.html', {'book_types': book_types})

@login_required
def delete_image(request, image_id):
    print(image_id)
    image = get_object_or_404(Image, pk=image_id)  # Ensure the image exists
    book = image.book  # Get the book related to the image

    # You can add more checks here if needed (for example, to ensure the user owns the book)

    image.delete()  # Delete the image

    return redirect('update_book', pk=book.pk)  # Redirect to the book's update page

@login_required
def commandes_list(request):
    commandes = Commande.objects.all()
    return render(request, 'dash/commandes_list.html', {'commandes': commandes})


@login_required
def commande_detail(request, commande_id):
    # Fetch the commande object
    commande = get_object_or_404(Commande, id=commande_id)

    # Fetch the related book
    book = commande.book

    return render(request, 'dash/commande_detail.html', {'commande': commande, 'book': book})

@login_required
def valider_commande(request, id):
    commande = get_object_or_404(Commande, id=id)
    commande.valider = True  # Set the valider field to True
    commande.save()  # Save the changes to the database

    # Ensure you use the correct name 'commande_detail' in the redirect
    return redirect('commandes_list')


###################
###################
###################
###################
###################
###################
###################


def home(request):
    # Fetch all book types for the dropdown
    book_types = BookType.objects.all()

    # Fetch all books with their images
    books = Book.objects.all()

    return render(request, 'web/home.html', {'book_types': book_types, 'books': books})




def book_search(request):
    book_id = request.GET.get('book_id')
    type_id = request.GET.get('type_id')

    context = {}

    # If a specific book ID is provided, fetch that book
    if book_id:
        # Fetch the specific book
        book = get_object_or_404(Book, id=book_id)
        context['book'] = book

        # Optionally, you can fetch books of the same type to show on the book page
        books_of_same_type = Book.objects.filter(book_type=book.book_type).exclude(id=book_id)
        context['books_of_same_type'] = books_of_same_type

        # Render the template for the single book
        return render(request, 'web/book.html', context)

    # If a specific type ID is provided, fetch all books of that type
    elif type_id:
        # Fetch the specific book type
        book_types = BookType.objects.all()

        # Fetch all books with their images
        books = Book.objects.all()
        book_type = get_object_or_404(BookType, id=type_id)
        context['book_type'] = book_type

        # Fetch all books that belong to this book type
        books_of_same_type = Book.objects.filter(book_type=book_type)


        # Render the template for all books of the same type
        return render(request, 'web/allbook.html',  {'books_of_same_type' : books_of_same_type,'book_types': book_types, 'books': books})

    # If neither book_id nor type_id is provided, you can fetch all books or show a message
    else:
        # Fetch all book types for the dropdown
        book_types = BookType.objects.all()

        # Fetch all books with their images
        books = Book.objects.all()

        return render(request, 'web/home.html', {'book_types': book_types, 'books': books})


def commande(request):
    book_id = request.GET.get('book_id')

    # Retrieve the specific book using the book_id
    book = get_object_or_404(Book, id=book_id)

    return render(request, 'web/commande.html', {'book': book})

def savecommande(request):
    # Get the book_id from GET parameters (could be from a form or URL query)
    book_id = request.GET.get('book_id')

    if book_id:
        book = get_object_or_404(Book, pk=book_id)

        # Assuming you're saving an order related to the book (adjust according to your model structure)
        if request.method == "POST":
            # Get the form data (adjust fields according to your form)
            name = request.POST.get('name')
            client = request.POST.get('client')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            message = request.POST.get('message')
            quantity = request.POST.get('quantity', 1)

            # Create a new Commande (order)
            Commande.objects.create(
                book=book,  # Book related to the order
                name=name,
                phone=phone,
                email=email,
                message=message,
                quantity=quantity
            )

            # Optionally, redirect or show a success message
            return render(request, 'web/book.html', {'book': book})

    # In case no book_id is passed or a failed POST request, render the form
    return render(request, 'web/book.html', {'book': book})

