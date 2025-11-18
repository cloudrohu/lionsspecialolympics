from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Profile(models.Model):
    """Extended user profile for volunteers/donors/staff."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='profiles/%Y/%m/', blank=True, null=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('volunteer', 'Volunteer'),
        ('donor', 'Donor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.full_name or str(self.user)


class Volunteer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='volunteer_profiles')
    skills = models.TextField(blank=True, help_text='Comma separated or free text of skills')
    availability = models.CharField(max_length=200, blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Volunteer: {self.profile.full_name or self.profile.user}" 


class Donor(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='donor_profiles')
    donor_type = models.CharField(max_length=50, choices=[('individual', 'Individual'), ('organization', 'Organization')], default='individual')
    notes = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.profile and self.profile.full_name:
            return f"Donor: {self.profile.full_name}"
        return f"Donor #{self.pk}"


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    projects = models.ManyToManyField('Project', blank=True, related_name='campaigns')

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured_image = models.ImageField(upload_to='projects/%Y/%m/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Donation(models.Model):
    PAYMENT_METHODS = [
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('offline', 'Offline'),
    ]
    STATUS = [
        ('initiated', 'Initiated'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='offline')
    date = models.DateTimeField(default=timezone.now)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    transaction_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='initiated')
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Donation {self.pk} - {self.amount}"


class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    registration_required = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    STATUS = [
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='event_registrations')
    name = models.CharField(max_length=255, blank=True)  # for guest registrations
    email = models.EmailField(blank=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='registered')
    extra_info = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = (('event', 'user'),)

    def __str__(self):
        who = self.user or self.name
        return f"{who} -> {self.event.title}"


class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_posts')
    published_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_on', '-created_on']

    def publish(self):
        self.is_published = True
        if not self.published_on:
            self.published_on = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    received_on = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-received_on']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='gallery/%Y/%m/')
    caption = models.CharField(max_length=500, blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    album = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-uploaded_on']

    def __str__(self):
        return self.title or f"Image {self.pk}"


class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='partners/%Y/%m/', blank=True, null=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    sponsorship_level = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Optional models: FAQ, Testimonial, ImpactMetric, Location
class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Smaller numbers appear first')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_on']

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    author_name = models.CharField(max_length=255)
    author_title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    photo = models.ImageField(upload_to='testimonials/%Y/%m/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_on']

    def __str__(self):
        return f"{self.author_name} - {'Featured' if self.is_featured else 'Testimonial'}"


class ImpactMetric(models.Model):
    title = models.CharField(max_length=255)
    value = models.CharField(max_length=100, help_text='E.g. "10,000+" or "95%"')
    description = models.CharField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_on']

    def __str__(self):
        return f"{self.title}: {self.value}"


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    is_head_office = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_head_office', 'name']

    def __str__(self):
        return self.name
    

class SocialLink(models.Model):
    """Represent social media profiles or external links for Profiles, Partners, or the organisation."""
    PLATFORM_CHOICES = [
    ('facebook', 'Facebook'),
    ('twitter', 'Twitter/X'),
    ('instagram', 'Instagram'),
    ('linkedin', 'LinkedIn'),
    ('youtube', 'YouTube'),
    ('tiktok', 'TikTok'),
    ('whatsapp', 'WhatsApp'),
    ('telegram', 'Telegram'),
    ('website', 'Website'),
    ('other', 'Other'),
    ]


    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='website')
    url = models.URLField(help_text='Full URL to the social profile or link')
    handle = models.CharField(max_length=255, blank=True, help_text='Optional username/handle')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='social_links')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, related_name='social_links')
    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    icon = models.ImageField(upload_to='social_icons/%Y/%m/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['order', '-created_on']
        unique_together = (('platform', 'profile', 'partner'),)


    def __str__(self):
        owner = self.profile or self.partner or 'Organisation'
        return f"{self.platform} ({owner})"

# add near other models in home/models.py
class CarouselSlide(models.Model):
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='carousel/%Y/%m/')
    link = models.URLField(blank=True, help_text='Optional link when slide is clicked')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_on']

    def __str__(self):
        return self.title or f"Slide {self.pk}"
