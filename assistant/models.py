from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserProfile(models.Model):
    """Stores extended personal details for a registered user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile({self.user.username})"


class TechGuide(models.Model):
    """Technical setup and troubleshooting guide linked from chatbot answers."""

    CATEGORY_SETUP = 'setup'
    CATEGORY_OS = 'os'
    CATEGORY_NETWORK = 'network'
    CATEGORY_DEVTOOLS = 'devtools'
    CATEGORY_SECURITY = 'security'
    CATEGORY_HARDWARE = 'hardware'

    CATEGORY_CHOICES = [
        (CATEGORY_SETUP, 'Software & Environment Setup'),
        (CATEGORY_OS, 'Operating System & Performance'),
        (CATEGORY_NETWORK, 'Network & Connectivity'),
        (CATEGORY_DEVTOOLS, 'Developer Tools & Databases'),
        (CATEGORY_SECURITY, 'Security & Accounts'),
        (CATEGORY_HARDWARE, 'Hardware & Peripherals'),
    ]

    slug = models.SlugField(unique=True, max_length=120)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_SETUP)
    summary = models.TextField()
    steps_json = models.JSONField(default=list)
    keywords = models.TextField(help_text='Comma-separated keywords and phrases.')
    sample_questions = models.JSONField(default=list)
    external_url = models.URLField(blank=True)
    external_label = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('assistant:guide_detail', kwargs={'slug': self.slug})

    def keyword_list(self) -> list[str]:
        return [kw.strip() for kw in self.keywords.split(',') if kw.strip()]


class ChatMessage(models.Model):
    """Persisted message between an authenticated user and the technical chatbot."""

    SENDER_USER = 'user'
    SENDER_BOT = 'bot'
    SENDER_CHOICES = [
        (SENDER_USER, 'User'),
        (SENDER_BOT, 'Bot'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    links = models.JSONField(default=list, blank=True)
    matched_guide = models.ForeignKey(
        TechGuide,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='matched_messages',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self) -> str:
        preview = self.message[:40].replace('\n', ' ')
        return f"[{self.sender}] {self.user.username}: {preview}"
