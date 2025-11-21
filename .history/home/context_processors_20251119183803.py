# home/context_processors.py
from .models import SocialLink, Location, Profile

def global_vars(request):
    """
    Global template variables used across the site.
    Returns small lists (not QuerySets) to avoid surprising lazy-eval issues in templates.
    """
    # social links (visible)
    social_links = list(
        SocialLink.objects.filter(is_visible=True).order_by('order')[:10]
    )

    # locations (head office first)
    locations = list(
        Location.objects.all().order_by('-is_head_office')[:5]
    )

    # team members (staff and volunteers)
    team_members = list(
        Profile.objects.filter(role__in=['staff', 'volunteer']).order_by('full_name')[:10]
    )

    return {
        'site_name': 'Your NGO Name',
        'social_links': social_links,
        'locations': locations,
        'team_members': team_members,
    }
