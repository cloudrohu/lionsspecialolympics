from django.urls import path
from .views import (
    HomeView, AboutView,
    ProjectListView, ProjectDetailView,
    CampaignListView, CampaignDetailView, CampaignDonateView,
    EventListView, EventDetailView, EventRegisterView,
    DonateView, VolunteerView, VolunteerApplyView,
    NewsListView, NewsDetailView,
    GalleryView, ContactView,
    FAQView, TestimonialView, PartnerView, LocationView,
    DashboardView, ThankYouView,

    sports_setup,
    food_refreshments,
    awards_recognition,
    participant_kits,
    assistive_devices,
    medical_safety,
    media_coverage,
    honour_felicitation,
    administration,
    leadership_detail
)

app_name = 'home'

urlpatterns = [

    path('', HomeView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),

    # Projects
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),

    path('leadership/<slug:slug>/',leadership_detail,name='leadership_detail'),

    # Campaigns
    path('campaigns/', CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/<slug:slug>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<slug:slug>/donate/', CampaignDonateView.as_view(), name='campaign_donate'),

    # Events
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/register/', EventRegisterView.as_view(), name='event_register'),

    # Donate & Volunteer
    path('donate/', DonateView.as_view(), name='donate'),
    path('volunteer/', VolunteerView.as_view(), name='volunteer'),
    path('volunteer/apply/', VolunteerApplyView.as_view(), name='volunteer_apply'),

    # News & Blog
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),

    # Gallery & Contact
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('thank-you/', ThankYouView.as_view(), name='thank_you'),

    # Misc
    path('faq/', FAQView.as_view(), name='faq'),
    path('testimonials/', TestimonialView.as_view(), name='testimonials'),
    path('partners/', PartnerView.as_view(), name='partners'),
    path('locations/', LocationView.as_view(), name='locations'),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # ================= INITIATIVES =================
    path('initiatives/sports-setup/', sports_setup, name='sports_setup'),
    path('initiatives/food-refreshments/', food_refreshments, name='food_refreshments'),
    path('initiatives/awards-recognition/', awards_recognition, name='awards_recognition'),
    path('initiatives/participant-kits/', participant_kits, name='participant_kits'),
    path('initiatives/assistive-devices/', assistive_devices, name='assistive_devices'),
    path('initiatives/medical-safety/', medical_safety, name='medical_safety'),
    path('initiatives/media-coverage/', media_coverage, name='media_coverage'),
    path('initiatives/honour-felicitation/', honour_felicitation, name='honour_felicitation'),
    path('initiatives/administration/', administration, name='administration'),
]
