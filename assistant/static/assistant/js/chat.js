(function () {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send-btn');
    const messagesBox = document.getElementById('chat-messages');
    const clearBtn = document.getElementById('clear-chat-btn');

    if (!chatForm || !chatInput || !messagesBox) {
        return;
    }

    const apiUrl = chatForm.dataset.apiUrl;
    const clearUrl = clearBtn ? clearBtn.dataset.clearUrl : '';

    function getCsrfToken() {
        const tokenInput = chatForm.querySelector('input[name="csrfmiddlewaretoken"]');
        if (tokenInput && tokenInput.value) {
            return tokenInput.value;
        }
        const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function isSafeUrl(url) {
        return typeof url === 'string' && (
            url.startsWith('/') ||
            url.startsWith('https://') ||
            url.startsWith('http://')
        );
    }

    function scrollToBottom() {
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function appendMessageBubble(msg) {
        const welcomeEl = document.getElementById('welcome-message');
        if (welcomeEl) {
            welcomeEl.remove();
        }

        const isUser = msg.sender === 'user';
        const row = document.createElement('div');
        row.className = 'message-row ' + (isUser ? 'user-row' : 'bot-row');

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble ' + (isUser ? 'user-bubble' : 'bot-bubble');

        const meta = document.createElement('div');
        meta.className = 'message-meta';
        const authorSpan = document.createElement('span');
        authorSpan.textContent = isUser ? 'You' : 'Chatbot Assistant';
        const timeSpan = document.createElement('span');
        timeSpan.textContent = msg.created_at || '';
        meta.appendChild(authorSpan);
        meta.appendChild(timeSpan);

        const body = document.createElement('p');
        body.className = 'message-text';
        body.textContent = msg.message || '';

        bubble.appendChild(meta);
        bubble.appendChild(body);

        if (Array.isArray(msg.links) && msg.links.length > 0) {
            const linksWrap = document.createElement('div');
            linksWrap.className = 'message-links';

            msg.links.forEach(function (link) {
                if (!link || !isSafeUrl(link.url)) {
                    return;
                }
                const anchor = document.createElement('a');
                anchor.href = link.url;
                const isExternal = link.type === 'external';
                anchor.className = 'chat-link ' + (isExternal ? 'chat-link-external' : 'chat-link-internal');
                anchor.textContent = (link.label || 'Open Guide') + (isExternal ? ' ↗' : ' →');
                if (isExternal) {
                    anchor.target = '_blank';
                    anchor.rel = 'noopener noreferrer';
                }
                linksWrap.appendChild(anchor);
            });

            if (linksWrap.children.length > 0) {
                bubble.appendChild(linksWrap);
            }
        }

        row.appendChild(bubble);
        messagesBox.appendChild(row);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const row = document.createElement('div');
        row.className = 'message-row bot-row';
        row.id = 'typing-indicator';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble bot-bubble';
        const text = document.createElement('p');
        text.className = 'message-text muted';
        text.textContent = 'Chatbot Assistant is finding the right guide...';
        bubble.appendChild(text);
        row.appendChild(bubble);
        messagesBox.appendChild(row);
        scrollToBottom();
        return row;
    }

    async function sendMessage(rawText) {
        const text = rawText.trim();
        if (!text) {
            return;
        }

        chatInput.value = '';
        sendBtn.disabled = true;
        chatInput.disabled = true;

        const typingEl = appendTypingIndicator();

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ message: text }),
            });

            const data = await response.json();
            typingEl.remove();

            if (!response.ok) {
                appendMessageBubble({
                    sender: 'bot',
                    message: data.error || 'Could not process your request. Please try again.',
                    links: [],
                });
                return;
            }

            if (data.user_message) {
                appendMessageBubble(data.user_message);
            }
            if (data.bot_message) {
                appendMessageBubble(data.bot_message);
            }
        } catch (err) {
            typingEl.remove();
            appendMessageBubble({
                sender: 'bot',
                message: 'Network error while reaching the chatbot server. Please try again.',
                links: [],
            });
        } finally {
            sendBtn.disabled = false;
            chatInput.disabled = false;
            chatInput.focus();
        }
    }

    chatForm.addEventListener('submit', function (event) {
        event.preventDefault();
        sendMessage(chatInput.value);
    });

    document.querySelectorAll('.prompt-chip').forEach(function (chip) {
        chip.addEventListener('click', function () {
            const prompt = chip.dataset.prompt || chip.textContent;
            sendMessage(prompt);
        });
    });

    if (clearBtn && clearUrl) {
        clearBtn.addEventListener('click', async function () {
            clearBtn.disabled = true;
            try {
                const response = await fetch(clearUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                    },
                });
                if (response.ok) {
                    window.location.reload();
                }
            } finally {
                clearBtn.disabled = false;
            }
        });
    }

    scrollToBottom();
})();
