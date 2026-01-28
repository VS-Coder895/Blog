from django.contrib import admin

from .models import Category, Author, Post, Member, Comment

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("created_at", "category")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "joined_date")
    list_filter = ("joined_date",)
    prepopulated_fields = {"slug": ("first_name", "last_name")}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("member", "post", "created_at")
    list_filter = (
        "post",
        "created_at",
    )
