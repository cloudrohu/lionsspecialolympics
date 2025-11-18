from django.urls import path
from django.contrib.auth import views as auth_views # 👈 ADDED for default login/logout views
# You will likely need to add a custom view for signup/registration, 
# for now, I will assume it's imported as 'RegisterView'.
# If you are using django-allauth or a similar package, the import will be different.
from .views import ( 
    HomeView, AboutView,
    ProjectListView, ProjectDetailView,
    CampaignListView, CampaignDetailView, CampaignDonateView,
    EventListView, EventDetailView, EventRegisterView,
    DonateView, VolunteerView, VolunteerApplyView,
    NewsListView, NewsDetailView,
    GalleryView, ContactView,
    FAQView, TestimonialView, PartnerView, LocationView,
    DashboardView,
    # Assuming you have a custom registration view in .views
    RegisterView # 👈 ADDED (You must ensure this view exists in your .views file) 
)

app_name = 'home'

urlpatterns = [
    # AUTHENTICATION PATHS (MISSING IN ORIGINAL FILE)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # 👈 ADDED
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # 👈 ADDED
    path('signup/', RegisterView.as_view(), name='signup'), # 👈 ADDED - This fixes the error!
    
    # -------------------------------------------------------------
    # EXISTING URLS BELOW
    # -------------------------------------------------------------
    
    # homepage named 'index' to match templates
    path('', HomeView.as_view(), name='index'),

    path('about/', AboutView.as_view(), name='about'),

    # Projects
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),

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

    # Misc
    path('faq/', FAQView.as_view(), name='faq'),
    path('testimonials/', TestimonialView.as_view(), name='testimonials'),
    path('partners/', PartnerView.as_view(), name='partners'),
    path('locations/', LocationView.as_view(), name='locations'),

    # Staff dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]