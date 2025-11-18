# views.py (public scaffold)
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Project, NewsPost, Campaign, Event, ContactMessage, Donation
from .forms import ContactForm, DonationForm


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        featured_projects = Project.objects.filter(status='ongoing')[:6]
        latest_news = NewsPost.objects.filter(is_published=True).order_by('-published_on')[:3]
        campaigns = Campaign.objects.filter(is_active=True)[:3]
        context = {
            'featured_projects': featured_projects,
            'latest_news': latest_news,
            'campaigns': campaigns,
        }
        return render(request, self.template_name, context)


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.filter(status='ongoing')


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'


class NewsListView(ListView):
    model = NewsPost
    template_name = 'news/list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return NewsPost.objects.filter(is_published=True).order_by('-published_on')


class NewsDetailView(DetailView):
    model = NewsPost
    template_name = 'news/detail.html'
    context_object_name = 'post'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('main:contact')

    def form_valid(self, form):
        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data.get('subject', ''),
            message=form.cleaned_data['message']
        )
        messages.success(self.request, 'Thank you — your message has been received.')
        return super().form_valid(form)


class DonateView(FormView):
    template_name = 'donate.html'
    form_class = DonationForm
    success_url = reverse_lazy('main:donate')

    def form_valid(self, form):
        donor = form.cleaned_data.get('donor')
        amount = form.cleaned_data['amount']
        campaign = form.cleaned_data.get('campaign')
        # create offline donation record; payment integration handled separately
        Donation.objects.create(
            donor=donor,
            amount=amount,
            method='offline',
            campaign=campaign,
            status='initiated'
        )
        messages.success(self.request, 'Donation recorded. We will contact you for confirmation.')
        return super().form_valid(form)



# Note: create simple ContactForm and DonationForm in forms.py; templates under templates/ as referenced.
