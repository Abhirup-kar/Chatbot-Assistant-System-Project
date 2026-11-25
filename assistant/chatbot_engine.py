from difflib import SequenceMatcher
import re
from django.urls import reverse

from .models import TechGuide

STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can', 'could', 'do',
    'does', 'for', 'from', 'get', 'help', 'how', 'i', 'in', 'is', 'it', 'me',
    'my', 'need', 'of', 'on', 'or', 'please', 'should', 'some', 'tell', 'the',
    'this', 'to', 'troubleshoot', 'fix', 'issue', 'issues', 'problem', 'problems',
    'setup', 'install', 'with', 'what', 'why', 'where', 'when', 'you', 'your',
}

GREETING_WORDS = {
    'hi', 'hello', 'hey', 'hii', 'greetings', 'morning', 'afternoon', 'evening',
}

THANKS_WORDS = {
    'thanks', 'thank', 'bye', 'goodbye', 'cheers', 'awesome', 'great',
}

HELP_PHRASES = (
    'what can you do', 'show topics', 'list topics', 'all guides',
    'all topics', 'browse guides', 'help menu',
)

PROFILE_PHRASES = (
    'edit profile', 'edit my profile', 'update profile', 'edit details',
    'edit my details', 'personal details', 'change password', 'update password',
    'account settings', 'my account', 'user details',
)


def normalize_text(text: str) -> str:
    """Lowercase and strip punctuation while keeping alphanumeric tokens and spaces."""
    cleaned = re.sub(r'[^a-z0-9\s]+', ' ', text.lower())
    return re.sub(r'\s+', ' ', cleaned).strip()


def tokenize(text: str, drop_stop_words: bool = True) -> list[str]:
    tokens = normalize_text(text).split()
    if not drop_stop_words:
        return tokens
    return [tok for tok in tokens if tok not in STOP_WORDS and len(tok) > 1]


def _fuzzy_token_score(query_tokens: list[str], target_tokens: list[str]) -> float:
    if not query_tokens or not target_tokens:
        return 0.0
    score = 0.0
    for qt in query_tokens:
        best = 0.0
        for tt in target_tokens:
            if qt == tt:
                best = 1.0
                break
            if len(qt) >= 4 and len(tt) >= 4:
                ratio = SequenceMatcher(None, qt, tt).ratio()
                if ratio >= 0.80 and ratio > best:
                    best = ratio * 0.85
        score += best
    return score


def _score_guide(normalized_query: str, query_tokens: list[str], guide: TechGuide) -> float:
    score = 0.0
    title_norm = normalize_text(guide.title)
    title_tokens = tokenize(guide.title, drop_stop_words=True)

    keyword_phrases = [normalize_text(kw) for kw in guide.keyword_list()]
    keyword_phrases = [kp for kp in keyword_phrases if kp]

    # 1. Exact phrase matches in keywords or title
    for phrase in keyword_phrases:
        if f' {phrase} ' in f' {normalized_query} ':
            score += 4.5 if ' ' in phrase else 3.2
    if title_norm and title_norm in normalized_query:
        score += 5.0

    # 2. Token & fuzzy matching against keywords and title
    kw_tokens = tokenize(' '.join(keyword_phrases), drop_stop_words=False)
    score += _fuzzy_token_score(query_tokens, kw_tokens) * 2.2
    score += _fuzzy_token_score(query_tokens, title_tokens) * 1.8

    # 3. Sample questions & summary overlap
    sample_tokens = tokenize(' '.join(guide.sample_questions or []), drop_stop_words=True)
    summary_tokens = tokenize(guide.summary, drop_stop_words=True)
    score += _fuzzy_token_score(query_tokens, sample_tokens) * 0.9
    score += _fuzzy_token_score(query_tokens, summary_tokens) * 0.45

    # 4. Whole-phrase fuzzy similarity boost for short queries with typos
    if normalized_query and len(query_tokens) <= 4:
        for phrase in keyword_phrases:
            if len(phrase) >= 4 and SequenceMatcher(None, normalized_query, phrase).ratio() >= 0.78:
                score += 2.5
                break

    return score


def _build_guide_links(guide: TechGuide, related_guides: list[TechGuide]) -> list[dict]:
    links = [
        {
            'label': f'Open Setup/Help Guide: {guide.title}',
            'url': guide.get_absolute_url(),
            'type': 'internal',
        }
    ]
    if guide.external_url:
        links.append(
            {
                'label': guide.external_label or 'Official Documentation',
                'url': guide.external_url,
                'type': 'external',
            }
        )
    for rel in related_guides[:2]:
        links.append(
            {
                'label': f'Related Guide: {rel.title}',
                'url': rel.get_absolute_url(),
                'type': 'internal',
            }
        )
    return links


def get_bot_response(user_message: str) -> dict:
    """Return a structured reply with clickable links for a technical query."""
    normalized = normalize_text(user_message)
    all_tokens = tokenize(user_message, drop_stop_words=False)
    meaningful_tokens = tokenize(user_message, drop_stop_words=True)

    if not normalized:
        return {
            'reply': 'Please type a technical question or setup topic so I can help you.',
            'links': [
                {
                    'label': 'Browse All Technical Guides',
                    'url': reverse('assistant:guide_list'),
                    'type': 'internal',
                }
            ],
            'matched_guide': None,
        }

    # Account / profile management redirect
    if any(phrase in normalized for phrase in PROFILE_PHRASES):
        return {
            'reply': (
                'You can update your name, email, phone, occupation, address, bio, or password '
                'from your profile settings page using the link below.'
            ),
            'links': [
                {
                    'label': 'Go to Edit User Details',
                    'url': reverse('assistant:edit_profile'),
                    'type': 'internal',
                }
            ],
            'matched_guide': None,
        }

    # Explicit help / topic directory request
    if normalized == 'help' or any(phrase in normalized for phrase in HELP_PHRASES):
        return {
            'reply': (
                'I can assist with software setups (Python, Django, XAMPP/MySQL, Git, VS Code) '
                'and troubleshooting (Wi-Fi, slow PC, BSOD, audio, Bluetooth, printers, updates, '
                'browser SSL/cache, databases, email, and malware). Ask a question or open the full '
                'directory below.'
            ),
            'links': [
                {
                    'label': 'Browse All Technical Guides',
                    'url': reverse('assistant:guide_list'),
                    'type': 'internal',
                },
                {
                    'label': 'Edit User Details',
                    'url': reverse('assistant:edit_profile'),
                    'type': 'internal',
                },
            ],
            'matched_guide': None,
        }

    # Greetings (only if the user isn't also asking a real technical question)
    if len(all_tokens) <= 3 and any(tok in GREETING_WORDS for tok in all_tokens):
        return {
            'reply': (
                'Hello! I am your Technical Support Chatbot Assistant. Ask me about software '
                'setups like Python, Django, XAMPP/MySQL, or troubleshooting issues such as Wi-Fi, '
                'slow performance, audio, printers, or system updates.'
            ),
            'links': [
                {
                    'label': 'Browse All Technical Guides',
                    'url': reverse('assistant:guide_list'),
                    'type': 'internal',
                }
            ],
            'matched_guide': None,
        }

    # Farewells / gratitude
    if len(all_tokens) <= 4 and any(tok in THANKS_WORDS for tok in all_tokens):
        return {
            'reply': (
                'You are welcome! Feel free to ask another technical question anytime, or browse '
                'our step-by-step guides.'
            ),
            'links': [
                {
                    'label': 'Browse All Technical Guides',
                    'url': reverse('assistant:guide_list'),
                    'type': 'internal',
                }
            ],
            'matched_guide': None,
        }

    guides = list(TechGuide.objects.all())
    scored: list[tuple[float, TechGuide]] = []
    # Fallback to all tokens if every word happened to be a stop word (e.g. "setup install")
    query_tokens = meaningful_tokens if meaningful_tokens else all_tokens

    for guide in guides:
        score = _score_guide(normalized, query_tokens, guide)
        if score > 0:
            scored.append((score, guide))

    scored.sort(key=lambda item: item[0], reverse=True)

    match_threshold = 2.0
    if scored and scored[0][0] >= match_threshold:
        best_score, best_guide = scored[0]
        related = [
            g for s, g in scored[1:4]
            if s >= max(2.2, best_score * 0.45) and g.id != best_guide.id
        ]
        return {
            'reply': f'{best_guide.summary} Click the guide link below for full step-by-step instructions.',
            'links': _build_guide_links(best_guide, related),
            'matched_guide': best_guide,
        }

    # Unrecognized / low-confidence query fallback
    partial_links = [
        {
            'label': f'Suggested Guide: {g.title}',
            'url': g.get_absolute_url(),
            'type': 'internal',
        }
        for s, g in scored[:2]
        if s >= 0.8
    ]
    partial_links.append(
        {
            'label': 'Browse All Technical Guides',
            'url': reverse('assistant:guide_list'),
            'type': 'internal',
        }
    )

    return {
        'reply': (
            "I couldn't find an exact match for that query. Try including keywords such as "
            '"Django setup", "XAMPP MySQL", "Python PATH", "Wi-Fi", "slow PC", "Bluetooth", '
            '"printer", or "browser SSL", or browse all guides below.'
        ),
        'links': partial_links,
        'matched_guide': None,
    }
