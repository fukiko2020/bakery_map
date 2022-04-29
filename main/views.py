from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "main/index.html"
