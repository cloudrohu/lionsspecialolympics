from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import *

from django.utils.html import format_html

@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'is_active', 'created_on', 'preview')
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_on',)
    search_fields = ('title', 'subtitle')

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:48px; object-fit:cover;"/>', obj.image.url)
        return '-'
    preview.short_description = 'Preview'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'role', 'phone')
    search_fields = ('full_name', 'user__username', 'phone')
    list_filter = ('role',)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'status', 'applied_on')
    search_fields = ('profile__full_name', 'skills')
    list_filter = ('status', 'availability')
    readonly_fields = ('applied_on',)


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'donor_type', 'created_on')
    search_fields = ('profile__full_name',)
    list_filter = ('donor_type',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'amount', 'method', 'status', 'date', 'campaign', 'project')
    search_fields = ('donor__profile__full_name', 'transaction_id')
    list_filter = ('method', 'status', 'campaign')
    readonly_fields = ('date',)
    actions = ['mark_completed', 'mark_refunded']

    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} donation(s) marked as completed.")
    mark_completed.short_description = "Mark selected donations as completed"

    def mark_refunded(self, request, queryset):
        updated = queryset.update(status='refunded')
        self.message_user(request, f"{updated} donation(s) marked as refunded.")
    mark_refunded.short_description = "Mark selected donations as refunded"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'end_date', 'budget')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'summary', 'description')
    list_filter = ('status',)
    date_hierarchy = 'start_date'


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal_amount', 'deadline', 'is_active')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'description')
    list_filter = ('is_active',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'registration_required')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'location', 'description')
    list_filter = ('registration_required',)
    date_hierarchy = 'date'


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('registered_on',)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'name', 'email', 'status', 'registered_on')
    search_fields = ('user__username', 'name', 'email')
    list_filter = ('status', 'event')
    readonly_fields = ('registered_on',)


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'published_on')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('is_published', 'author')
    actions = ['publish_posts', 'unpublish_posts']

    def publish_posts(self, request, queryset):
        updated = 0
        for post in queryset:
            post.is_published = True
            if not post.published_on:
                post.published_on = timezone.now()
            post.save()
            updated += 1
        self.message_user(request, f"{updated} post(s) published.")
    publish_posts.short_description = "Publish selected posts"

    def unpublish_posts(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} post(s) unpublished.")
    unpublish_posts.short_description = "Unpublish selected posts"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'received_on', 'is_handled')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('is_handled',)
    readonly_fields = ('received_on',)
    actions = ['mark_handled']

    def mark_handled(self, request, queryset):
        updated = queryset.update(is_handled=True)
        self.message_user(request, f"{updated} message(s) marked as handled.")
    mark_handled.short_description = "Mark selected messages as handled"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'uploaded_on', 'album')
    search_fields = ('title', 'caption', 'album')
    list_filter = ('album',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'sponsorship_level')
    search_fields = ('name', 'website')
    list_filter = ('sponsorship_level',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order')
    search_fields = ('question', 'answer')
    list_editable = ('is_active', 'order')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'is_featured', 'created_on')
    search_fields = ('author_name', 'content')
    list_filter = ('is_featured',)


@admin.register(ImpactMetric)
class ImpactMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'order')
    search_fields = ('title', 'description')
    list_editable = ('order',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'is_head_office')
    search_fields = ('name', 'address', 'city', 'state')
    list_filter = ('is_head_office', 'country')


# Customizations: quick link to view image/logo in admin (optional)

    def logo_tag(self, obj):
        if getattr(obj, 'logo', None):
            return format_html('<img src="{}" style="height:40px;" />', obj.logo.url)
        return ''
    logo_tag.short_description = 'Logo'

# End of admin.py


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'profile', 'partner', 'is_visible', 'order')
    search_fields = ('platform', 'handle', 'url', 'profile__full_name', 'partner__name')
    list_filter = ('platform', 'is_visible')
    list_editable = ('is_visible', 'order')




@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_on')
    search_fields = ('name', 'role')
    readonly_fields = ('created_on',)

@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'order')
    list_editable = ('order',)
    search_fields = ('year', 'title')

@admin.register(AboutPageContent)
class AboutPageContentAdmin(admin.ModelAdmin):
    list_display = ('hero_heading', 'created_on', 'updated_on')
    readonly_fields = ('created_on', 'updated_on')
    # If you prefer single instance workflow, you can remove add permission later or enforce via code.


# End of admin.py