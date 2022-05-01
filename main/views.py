from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from . import forms
from .models import Bakery, Review


class IndexView(LoginRequiredMixin, ListView):
    context_object_name = "review_list"
    model = Review
    queryset = Review.objects.order_by("-pub_date")[:5]
    template_name = "main/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["bakery_list"] = Bakery.objects.all()
        return context


class BakeryDetailView(LoginRequiredMixin, DetailView):
    template_name = "main/bakery_detail.html"


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
