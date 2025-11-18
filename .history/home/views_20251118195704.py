
# Expanded views.py (all pages scaffold)
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import (
    Project, NewsPost, Campaign, Event, ContactMessage, Donation,
    Volunteer, GalleryImage, FAQ, Testimonial, Partner, ImpactMetric, Location, SocialLink,CarouselSlide  
)
from .forms import ContactForm, DonationForm, VolunteerForm, EventRegistrationForm

class RegisterView(View):
    """
    Handles user registration using a custom form.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:index') # Prevent already logged-in users from accessing registration
        form = UserRegistrationForm() # You must define this form in forms.py
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user and save to database
            user = form.save()
            # Log the user in immediately after successful registration
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('home:dashboard') # Redirect to the dashboard or home page
        
        # If form is invalid, render the page again with errors
        return render(request, 'registration/signup.html', {'form': form})

# --- END AUTHENTICATION VIEWS ADDED ---

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        featured_projects = Project.objects.filter(status='ongoing')[:6]
        latest_news = NewsPost.objects.filter(is_published=True).order_by('-published_on')[:3]
        campaigns = Campaign.objects.filter(is_active=True)[:3]
        impact_metrics = ImpactMetric.objects.all().order_by('order')[:6]
        partners = Partner.objects.all()[:8]
        gallery = GalleryImage.objects.order_by('-uploaded_on')[:6]
        social_links = SocialLink.objects.filter(is_visible=True)
        slides = CarouselSlide.objects.filter(is_active=True).order_by('order')[:10]  # NEW

        context = {
            'featured_projects': featured_projects,
            'latest_news': latest_news,
            'campaigns': campaigns,
            'impact_metrics': impact_metrics,
            'partners': partners,
            'gallery': gallery,
            'social_links': social_links,
            'slides': slides,   # pass to template
        }
        return render(request, self.template_name, context)
class AboutView(TemplateView):
    template_name = 'about.html'


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.filter(status__in=['ongoing', 'completed']).order_by('-created_on')


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'


class CampaignListView(ListView):
    model = Campaign
    template_name = 'campaigns/list.html'
    context_object_name = 'campaigns'
    paginate_by = 12

    def get_queryset(self):
        return Campaign.objects.filter(is_active=True).order_by('-created_on')


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'campaigns/detail.html'
    context_object_name = 'campaign'


class CampaignDonateView(FormView):
    template_name = 'campaigns/donate.html'
    form_class = DonationForm

    def dispatch(self, request, *args, **kwargs):
        self.campaign = get_object_or_404(Campaign, slug=kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'campaign': self.campaign}

    def form_valid(self, form):
        Donation.objects.create(
            donor=form.cleaned_data.get('donor'),
            amount=form.cleaned_data['amount'],
            campaign=self.campaign,
            method=form.cleaned_data.get('method', 'offline'),
            status='initiated'
        )
        messages.success(self.request, 'Thank you — your pledge has been recorded.')
        return redirect('main:campaign_detail', slug=self.campaign.slug)


class EventListView(ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        return Event.objects.order_by('date')


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'


class EventRegisterView(FormView):
    template_name = 'events/register.html'
    form_class = EventRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        EventRegistration = form.save(commit=False)
        EventRegistration.event = self.event
        if self.request.user.is_authenticated:
            EventRegistration.user = self.request.user
        EventRegistration.save()
        messages.success(self.request, 'You have successfully registered for the event.')
        return redirect('main:event_detail', pk=self.event.pk)


class DonateView(FormView):
    template_name = 'donate.html'
    form_class = DonationForm
    success_url = reverse_lazy('main:donate')

    def form_valid(self, form):
        Donation.objects.create(
            donor=form.cleaned_data.get('donor'),
            amount=form.cleaned_data['amount'],
            method=form.cleaned_data.get('method', 'offline'),
            campaign=form.cleaned_data.get('campaign'),
            status='initiated'
        )
        messages.success(self.request, 'Donation recorded. We will contact you for confirmation.')
        return super().form_valid(form)


class VolunteerView(TemplateView):
    template_name = 'volunteer/info.html'


class VolunteerApplyView(FormView):
    template_name = 'volunteer/apply.html'
    form_class = VolunteerForm
    success_url = reverse_lazy('main:volunteer_apply')

    def form_valid(self, form):
        volunteer = form.save(commit=False)
        if self.request.user.is_authenticated:
            volunteer.profile = self.request.user.profile
        volunteer.save()
        messages.success(self.request, 'Thank you for applying as a volunteer. We will get back to you.')
        return super().form_valid(form)


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


class GalleryView(ListView):
    model = GalleryImage
    template_name = 'gallery/list.html'
    context_object_name = 'images'
    paginate_by = 24

    def get_queryset(self):
        return GalleryImage.objects.order_by('-uploaded_on')


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


class FAQView(ListView):
    model = FAQ
    template_name = 'faq/list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('order')


class TestimonialView(ListView):
    model = Testimonial
    template_name = 'testimonials/list.html'
    context_object_name = 'testimonials'

    def get_queryset(self):
        return Testimonial.objects.order_by('-is_featured', '-created_on')


class PartnerView(ListView):
    model = Partner
    template_name = 'partners/list.html'
    context_object_name = 'partners'


class LocationView(ListView):
    model = Location
    template_name = 'locations/list.html'
    context_object_name = 'locations'


# Simple staff dashboard (requires is_staff)
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_donations'] = Donation.objects.count()
        ctx['recent_donations'] = Donation.objects.order_by('-date')[:10]
        ctx['upcoming_events'] = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]
        ctx['pending_volunteers'] = Volunteer.objects.filter(status='pending')[:10]
        return ctx

