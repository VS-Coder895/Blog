from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import DetailView, ListView

from .models import Post, Category, Member, Comment
from .forms import (
    SignUpForm,
    UserProfileForm,
    LoginForm,
    ChangePasswordForm,
    CommentForm,
)

# Create your views here.


class HomeView(View):
    def get(self, request):

        try:
            all_posts = Post.objects.all()
            all_categories = Category.objects.all()
            return render(
                request,
                "blog/all_posts.html",
                {
                    "has_posts": True,
                    "all_posts": all_posts,
                    "all_categories": all_categories,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )

        except Post.DoesNotExist:
            return render(
                request,
                "blog/all_posts.html",
                {
                    "has_posts": False,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


class PostDetailView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        post_comments = post.comments.all().order_by("-created_at")
        has_comments = len(post_comments) > 0
        comments_form = CommentForm()

        if request.session.get("is_logged_in"):
            return render(
                request,
                "blog/post-details.html",
                {
                    "post": post,
                    "has_comments": has_comments,
                    "post_comments": post_comments,
                    "comments_form": comments_form,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )
        return redirect("login")


class SignUpView(View):
    def get(self, request):
        sign_up_form = SignUpForm()
        return render(
            request,
            "blog/sign-up.html",
            {
                "sign_up_form": sign_up_form,
                "is_logged_in": request.session.get("is_logged_in"),
            },
        )

    def post(self, request):
        new_user = SignUpForm(request.POST)

        if new_user.is_valid():
            new_user.save()
            return redirect("login")
        else:
            return render(
                request,
                "blog/sign-up.html",
                {
                    "sign_up_form": new_user,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


class UserProfileView(View):
    def get(self, request):
        user_id = request.session.get("user_id")
        user = Member.objects.get(pk=user_id)
        user_profile_form = UserProfileForm(instance=user)
        return render(
            request,
            "blog/profile.html",
            {
                "user_profile_form": user_profile_form,
                "is_logged_in": request.session.get("is_logged_in"),
            },
        )

    def post(self, request):
        user_id = request.session.get("user_id")
        user = Member.objects.get(pk=user_id)
        user_profile_form = UserProfileForm(request.POST, instance=user)

        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect("home")
        else:
            return render(
                request,
                "blog/profile.html",
                {
                    "user_profile_form": user_profile_form,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


class ChangePasswordView(View):
    def get(self, request):
        change_password_form = ChangePasswordForm()
        return render(
            request,
            "blog/change-password.html",
            {
                "change_password_form": change_password_form,
                "is_logged_in": request.session.get("is_logged_in"),
            },
        )

    def post(self, request):
        change_password_form = ChangePasswordForm(request.POST)
        user_id = request.session.get("user_id")
        user = Member.objects.get(pk=user_id)

        if change_password_form.is_valid():

            if user.password == request.POST["password"]:
                if request.POST["confirm_password"] == request.POST["new_password"]:
                    user.password = request.POST["new_password"]
                    user.save()
                    return redirect("home")

                else:
                    return render(
                        request,
                        "blog/change-password.html",
                        {
                            "change_password_form": change_password_form,
                            "is_logged_in": request.session.get("is_logged_in"),
                            "error-message": "New Password Incorrect!",
                        },
                    )
            else:
                return render(
                    request,
                    "blog/change-password.html",
                    {
                        "change_password_form": change_password_form,
                        "is_logged_in": request.session.get("is_logged_in"),
                        "error-message": "Your Password Incorrect!",
                    },
                )

        else:
            return render(
                request,
                "blog/change-password.html",
                {
                    "change_password_form": change_password_form,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(
            request,
            "blog/login.html",
            {
                "login_form": login_form,
                "is_logged_in": request.session.get("is_logged_in"),
            },
        )

    def post(self, request):
        form_data = LoginForm(request.POST)

        try:
            if form_data.is_valid():
                user_email = form_data.cleaned_data["email"]
                user_password = form_data.cleaned_data["password"]

                user = Member.objects.get(email=user_email)

                if user:
                    if user.password == user_password:
                        request.session["user_id"] = user.id
                        request.session["is_logged_in"] = True

                        return redirect("home")
            return render(request, "blog/login.html", {"login_form": form_data})

        except Member.DoesNotExist:
            return redirect("login")


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("home")


class SpecificCategoryView(View):
    def get(self, request, slug):
        if request.session.get("is_logged_in"):
            category_posts = Post.objects.filter(category__slug=slug)
            has_posts = category_posts.count() > 0
            return render(
                request,
                "blog/specific-category.html",
                {
                    "has_posts": has_posts,
                    "category_posts": category_posts,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )
        return redirect("login")


class AddCommentView(View):
    def post(self, request, slug):
        comments_form = CommentForm(request.POST)

        try:
            if comments_form.is_valid():
                user = Member.objects.get(id=request.session.get("user_id"))
                post = Post.objects.get(slug=slug)
                comment = comments_form.save(commit=False)
                comment.member = user
                comment.post = post
                comment.save()
            return redirect("/post-details/" + post.slug)

        except:
            return render(
                request,
                "blog/post-details.html",
                {
                    "comments_form": comments_form,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


class SearchedPostsView(View):
    def get(self, request):
        try:
            user_input = request.GET["search_bar"]
            searched_posts = Post.objects.filter(title__icontains=user_input)
            return render(
                request,
                "blog/all_posts.html",
                {
                    "has_posts": True,
                    "all_posts": searched_posts,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )

        except Post.DoesNotExist:
            return render(
                request,
                "blog/all_posts.html",
                {
                    "has_posts": False,
                    "is_logged_in": request.session.get("is_logged_in"),
                },
            )


def custom_400_error_page(request, exception):
    return render(request, "blog/400.html", status=400)


def custom_404_error_page(request, exception):
    return render(request, "blog/404.html", status=404)
