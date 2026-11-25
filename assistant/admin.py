from django.contrib import admin

from .models import ChatMessage, TechGuide, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'occupation', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone', 'occupation')


@admin.register(TechGuide)
class TechGuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'updated_at')
    list_filter = ('category',)
    search_fields = ('title', 'slug', 'keywords', 'summary')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender', 'short_message', 'matched_guide', 'created_at')
    list_filter = ('sender', 'created_at')
    search_fields = ('user__username', 'message')
    raw_id_fields = ('user', 'matched_guide')

    @admin.display(description='Message')
    def short_message(self, obj: ChatMessage) -> str:
        return obj.message[:70]
