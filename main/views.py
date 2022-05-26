import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from . import forms
from .models import Bakery, Favorite, Review


class IndexView(ListView):
    context_object_name = "review_list"
    model = Review
    queryset = Review.objects.order_by("-pub_date")[:5]
    template_name = "main/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        bakery_list = Bakery.objects.all()
        print(self.request.user)
        context["user"] = self.request.user
        context["bakery_list"] = bakery_list
        MAP_API_KEY = os.getenv("MAP_API_KEY")
        context["map_src"] = f"https://maps.googleapis.com/maps/api/js?key={MAP_API_KEY}&callback=initMap"  # noqa: E501
        # context["map_src"] = os.getenv("MAP_SRC")
        context["bakery_list_json"] = serializers.serialize(
            "json",
            bakery_list
        )
        return context


class BakeryDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/bakery_detail.html"
    model = Bakery
    context_object_name = "bakery"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pk = self.kwargs["pk"]
        context["reviews"] = Review.objects.filter(bakery=pk)
        print(Review.objects.filter(bakery=self.kwargs["pk"]))
        MAP_API_KEY = os.getenv("MAP_API_KEY")
        context["map_src"] = f"https://maps.googleapis.com/maps/api/js?key={MAP_API_KEY}&callback=initMap"  # noqa: E501
        # context["map_src"] = os.getenv("MAP_SRC")
        is_saved = Favorite.objects.filter(bakery=pk, user=self.request.user)
        if is_saved:
            context["is_saved"] = True
        else:
            context["is_saved"] = False
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    form_class = forms.ReviewForm
    model = Review
    success_url = reverse_lazy("main:index")
    template_name = "main/create_review.html"

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        print("form:", review)
        self.review = review
        return super().form_valid(form)


class CreateBakeryView(LoginRequiredMixin, CreateView):
    form_class = forms.CreateBakeryForm
    model = Bakery
    success_url = reverse_lazy("main:index")
    template_name = "main/create_bakery.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        MAP_API_KEY = os.getenv("MAP_API_KEY")
        context["map_src"] = f"https://maps.googleapis.com/maps/api/js?key={MAP_API_KEY}&callback=initMap"  # noqa: E501
        context["map_src"] = os.getenv("MAP_SRC")
        return context


class FavoriteListView(LoginRequiredMixin, TemplateView):
    template_name = "main/favorite_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        bakery_list = Bakery.objects.filter(
            favorite_bakery__user=self.request.user
        )
        print(bakery_list)
        context["bakery_list"] = bakery_list
        context["favorite_json"] = serializers.serialize(
            "json",
            bakery_list
        )
        MAP_API_KEY = os.getenv("MAP_API_KEY")
        context["map_src"] = f"https://maps.googleapis.com/maps/api/js?key={MAP_API_KEY}&callback=initMap"  # noqa: E501
        return context


def create_favorite(request, pk):
    bakery = Bakery.objects.get(pk=pk)
    existing_favorite = Favorite.objects.filter(
        user=request.user, bakery=bakery.pk
    )
    if bakery and not existing_favorite:
        print("new favorite")
        Favorite.objects.create(user=request.user, bakery=bakery)
    elif existing_favorite:
        existing_favorite.delete()
    else:
        print("no such bakery")
    return redirect(to="main:bakery_detail", pk=pk)
