from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

class HomepageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'products/home.html'
