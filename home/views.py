
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
    Volunteer, GalleryImage, FAQ, Testimonial, Partner, ImpactMetric, Location, SocialLink,CarouselSlide ,Profile,
    SiteSetting,Highlight,
)
from .forms import ContactForm, DonationForm, VolunteerForm, EventRegistrationForm



class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # adapt these queries to your actual models and fields
        ctx['hero_image_url'] = '/static/images/about-hero.jpg'
        ctx['hero_heading'] = "About Cloud Rohu"
        ctx['hero_sub'] = "Empowering communities through compassion, innovation and action."

        ctx['mission_text'] = "To support underserved communities through welfare campaigns, education and health initiatives."
        ctx['vision_text'] = "A world where every person has access to opportunities and dignity."

        ctx['impact_metrics'] = ImpactMetric.objects.all().order_by('order')[:6]
        # Build team_members list from Profile model - adapt attribute names
        team = Profile.objects.filter(role__in=['admin','staff']).order_by('user__id')[:6]
        ctx['team_members'] = [
            {
                'photo_url': (p.photo.url if p.photo else '/static/images/avatar-placeholder.png'),
                'name': p.full_name or getattr(p, 'user').get_full_name() or str(getattr(p,'user')),
                'role': p.get_role_display() if hasattr(p,'get_role_display') else p.role,
                'bio': p.bio or '',
                'social_links': p.social_links.all() if hasattr(p,'social_links') else []
            } for p in team
        ]
        ctx['partners'] = [{'logo_url': (p.logo.url if p.logo else ''), 'name': p.name} for p in Partner.objects.all()[:12]]
        ctx['timeline_events'] = [
            {'year': '2009', 'title': 'Founded', 'desc':'Started with small local projects.'},
            {'year': '2016', 'title': 'Scaled up', 'desc':'Expanded to multiple cities.'},
        ]  # replace with your Timeline model if you have one

        ctx['gallery'] = [{'image_url': g.image.url, 'caption': g.caption} for g in GalleryImage.objects.order_by('-uploaded_on')[:9]]
        ctx['social_links'] = SocialLink.objects.filter(is_visible=True)

        ctx['cta_text'] = "Join Our Movement"
        ctx['cta_link'] = '/volunteer/'

        return ctx

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        site_setting = SiteSetting.objects.order_by('-id').first()
        featured_projects = Project.objects.filter
        latest_news = NewsPost.objects.filter(is_published=True).order_by('-published_on')[:3]
        campaigns = Campaign.objects.filter(is_active=True)[:3]
        impact_metrics = ImpactMetric.objects.all().order_by('order')[:6]
        partners = Partner.objects.all()[:8]
        gallery = GalleryImage.objects.order_by('-uploaded_on')[:6]
        highlights = Highlight.objects.filter(is_active=True).order_by('order')
        social_links = SocialLink.objects.filter(is_visible=True)
        slides = CarouselSlide.objects.filter(is_active=True).order_by('order')[:10]  # NEW

        context = {

            'highlights': highlights,
            'site_setting': site_setting,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['site_setting'] = SiteSetting.objects.order_by('-id').first()
        context['featured_projects'] = Project.objects.all()[:6]
        context['latest_news'] = NewsPost.objects.filter(is_published=True).order_by('-published_on')[:3]
        context['campaigns'] = Campaign.objects.filter(is_active=True)[:3]
        context['impact_metrics'] = ImpactMetric.objects.order_by('order')[:6]
        context['partners'] = Partner.objects.all()[:8]
        context['gallery'] = GalleryImage.objects.order_by('-uploaded_on')
        context['highlights'] = Highlight.objects.filter(is_active=True).order_by('order')
        context['social_links'] = SocialLink.objects.filter(is_visible=True)
        context['slides'] = CarouselSlide.objects.filter(is_active=True).order_by('order')[:10]

        return context
    
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

