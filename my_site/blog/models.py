from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField("Category Name", max_length=200, unique=True)
    slug = models.SlugField(db_index=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField("Author Name", max_length=100)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="posts-images")
    slug = models.SlugField(db_index=True, unique=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title} + {self.category.name}")
        return super().save(*args, **kwargs)


class Member(models.Model):
    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(validators=[MinLengthValidator(8)], max_length=250)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=250)
    joined_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return f"{ self.first_name } { self.last_name }"


class Comment(models.Model):
    comment_text = models.TextField()
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.member.__str__()
