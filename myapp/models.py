from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.timezone import now

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myapp_user_set',  # Use a unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myapp_user_permissions_set',  # Use a unique related_name
        blank=True
    )

    def __str__(self):
        return self.username

# Model for Book Type
class BookType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

# Model for Book
class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(max_length=200)
    book_type = models.ForeignKey(BookType, on_delete=models.CASCADE, related_name="books")
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

# Model for Image
class Image(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='book_images/')
    cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Image for {self.book.name}"

    def save(self, *args, **kwargs):
        if self.cover:
            Image.objects.filter(book=self.book).exclude(id=self.id).update(cover=False)
        super().save(*args, **kwargs)

class Commande(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=now)
    valider = models.BooleanField(default=False)  # Add the valider field

    def __str__(self):
        return f"Commande {self.id} - {self.book.name}"

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'