import json

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .chatbot_engine import get_bot_response
from .forms import (
    ProfileUpdateForm,
    StyledPasswordChangeForm,
    UserLoginForm,
    UserRegisterForm,
    UserUpdateForm,
)
from .management.commands.seed_kb import ensure_knowledge_base_seeded
from .models import ChatMessage, TechGuide, UserProfile


def _ensure_kb_populated() -> None:
    """Seed guides on demand if the database table is empty."""
    if not TechGuide.objects.exists():
        ensure_knowledge_base_seeded()


def _serialize_message(msg: ChatMessage) -> dict:
    return {
        'id': msg.id,
        'sender': msg.sender,
        'message': msg.message,
        'links': msg.links or [],
        'created_at': msg.created_at.strftime('%H:%M'),
    }


@require_GET
def home_view(request):
    _ensure_kb_populated()
    guide_count = TechGuide.objects.count()
    featured_guides = TechGuide.objects.all()[:6]
    return render(
        request,
        'assistant/home.html',
        {
            'guide_count': guide_count,
            'featured_guides': featured_guides,
        },
    )


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('assistant:chat')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f'Account "{user.username}" created successfully! Please log in to open the Chatbot Assistant.',
            )
            return redirect('assistant:login')
    else:
        form = UserRegisterForm()

    return render(request, 'assistant/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('assistant:chat')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            UserProfile.objects.get_or_create(user=user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('assistant:chat')
    else:
        form = UserLoginForm(request)

    return render(
        request,
        'assistant/login.html',
        {
            'form': form,
            'next': request.GET.get('next', ''),
        },
    )


@require_POST
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('assistant:login')


@login_required
@require_GET
def chat_view(request):
    _ensure_kb_populated()
    UserProfile.objects.get_or_create(user=request.user)
    chat_messages = ChatMessage.objects.filter(user=request.user).select_related('matched_guide')
    guides = TechGuide.objects.all()
    quick_prompts = [
        'How do I set up a Django project?',
        'How do I install Python and add it to PATH?',
        'My XAMPP MySQL port 3306 fails to start',
        'My Wi-Fi says connected with no internet',
        'Why is my computer running slow?',
        'How do I edit my user details?',
    ]
    return render(
        request,
        'assistant/chat.html',
        {
            'chat_messages': chat_messages,
            'guides': guides[:8],
            'total_guides': guides.count(),
            'quick_prompts': quick_prompts,
        },
    )


@login_required
@require_POST
def chat_api_view(request):
    _ensure_kb_populated()
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'error': 'Invalid request format.'}, status=400)

    raw_message = payload.get('message', '')
    if not isinstance(raw_message, str) or not raw_message.strip():
        return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

    user_text = raw_message.strip()
    user_msg = ChatMessage.objects.create(
        user=request.user,
        sender=ChatMessage.SENDER_USER,
        message=user_text,
    )

    bot_result = get_bot_response(user_text)
    bot_msg = ChatMessage.objects.create(
        user=request.user,
        sender=ChatMessage.SENDER_BOT,
        message=bot_result['reply'],
        links=bot_result['links'],
        matched_guide=bot_result['matched_guide'],
    )

    return JsonResponse(
        {
            'user_message': _serialize_message(user_msg),
            'bot_message': _serialize_message(bot_msg),
        },
        status=200,
    )


@login_required
@require_POST
def clear_chat_api_view(request):
    deleted_count, _ = ChatMessage.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'ok', 'deleted': deleted_count})


@login_required
@require_http_methods(['GET', 'POST'])
def edit_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=profile)
    password_form = StyledPasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'profile')
        if form_type == 'password':
            password_form = StyledPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been updated.')
                return redirect('assistant:edit_profile')
        else:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your personal details have been updated.')
                return redirect('assistant:edit_profile')

    return render(
        request,
        'assistant/edit_profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form,
        },
    )


@login_required
@require_GET
def guide_list_view(request):
    _ensure_kb_populated()
    category = request.GET.get('category', '').strip()
    query = request.GET.get('q', '').strip()

    guides = TechGuide.objects.all()
    valid_categories = {choice[0] for choice in TechGuide.CATEGORY_CHOICES}
    if category in valid_categories:
        guides = guides.filter(category=category)
    else:
        category = ''

    if query:
        guides = guides.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(keywords__icontains=query)
        )

    return render(
        request,
        'assistant/guide_list.html',
        {
            'guides': guides,
            'categories': TechGuide.CATEGORY_CHOICES,
            'selected_category': category,
            'search_query': query,
        },
    )


@login_required
@require_GET
def guide_detail_view(request, slug: str):
    _ensure_kb_populated()
    guide = get_object_or_404(TechGuide, slug=slug)
    related_guides = TechGuide.objects.filter(category=guide.category).exclude(id=guide.id)[:4]
    return render(
        request,
        'assistant/guide_detail.html',
        {
            'guide': guide,
            'related_guides': related_guides,
        },
    )
