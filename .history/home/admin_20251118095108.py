

# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
Profile, Volunteer, Donor, Donation, Project, Campaign, Event, EventRegistration,
NewsPost, ContactMessage, GalleryImage, Partner, FAQ, Testimonial, ImpactMetric, Location
)




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