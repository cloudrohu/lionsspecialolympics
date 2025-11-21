# home/context_processors.py

from .models import SocialLink, Location, Profile, SiteSetting

def global_vars(request):
    """
    Global template variables used across the site.
    Returns small lists to avoid lazy-eval issues.
    """

    # Organisation settings (logo, email, phone, etc)
    try:
        site_setting = SiteSetting.objects.first()
    except:
        site_setting = None

    # Social links
    social_links = list(
        SocialLink.objects.filter(is_visible=True).order_by('order')[:10]
    )

    # Office locations
    locations = list(
        Location.objects.all().order_by('-is_head_office')[:5]
    )

    # Staff & Volunteers
    team_members = list(
        Profile.objects.filter(role__in=['staff', 'volunteer'])
        .order_by('full_name')[:10]
    )

    return {
        "site_setting": site_setting,
        "social_links": social_links,
        "locations": locations,
        "team_members": team_members,
    }
