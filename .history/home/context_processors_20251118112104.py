from .models import SocialLink, Location

def global_vars(request):
    return {
        'site_name': 'Your NGO Name',
        'social_links': SocialLink.objects.filter(is_visible=True).order_by('order')[:10],
        'locations': Location.objects.all().order_by('-is_head_office')[:5],
    }
