/* ============================================================
   GREEN TIME MARINE TIME — Chat Widget Scripts
   Vanilla JS • Connects to GTMT AI Backend
   ============================================================ */

(function () {
  'use strict';

  // ---- Configuration ----
  var API_BASE_URL = window.GTMT_API_URL || 'https://dwight-the-chatbot-international-freight.onrender.com';
  var CHAT_ENDPOINT = API_BASE_URL + '/api/chat';

  // ---- Session ----
  var sessionId = 'gtmt-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);

  // ---- DOM Elements ----
  var chatToggle = document.getElementById('chatToggle');
  var chatWidget = document.getElementById('chatWidget');
  var chatClose = document.getElementById('chatClose');
  var chatMessages = document.getElementById('chatMessages');
  var chatForm = document.getElementById('chatForm');
  var chatInput = document.getElementById('chatInput');
  var chatSend = document.getElementById('chatSend');
  var quickBtns = document.querySelectorAll('.quick-btn');

  if (!chatToggle || !chatWidget) return;

  // ---- Toggle Chat Open/Close ----
  function openChat() {
    chatWidget.classList.add('open');
    chatToggle.classList.add('active');
    chatInput.focus();
  }

  function closeChat() {
    chatWidget.classList.remove('open');
    chatToggle.classList.remove('active');
  }

  chatToggle.addEventListener('click', function () {
    if (chatWidget.classList.contains('open')) {
      closeChat();
    } else {
      openChat();
    }
  });

  if (chatClose) {
    chatClose.addEventListener('click', closeChat);
  }

  // Close with Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && chatWidget.classList.contains('open')) {
      closeChat();
    }
  });

  // ---- Add Message to Chat ----
  function addMessage(text, type) {
    var msgDiv = document.createElement('div');
    msgDiv.className = 'message ' + type + '-message';

    var contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;

    msgDiv.appendChild(contentDiv);
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
  }

  function addBotMessageHTML(html) {
    var msgDiv = document.createElement('div');
    msgDiv.className = 'message bot-message';

    var contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = html;

    msgDiv.appendChild(contentDiv);
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
  }

  function addErrorMessage(text) {
    var msgDiv = document.createElement('div');
    msgDiv.className = 'message bot-message error-message';

    var contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text || 'Sorry, something went wrong. Please try again.';

    msgDiv.appendChild(contentDiv);
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
  }

  // ---- Typing Indicator ----
  function showTyping() {
    var typing = document.createElement('div');
    typing.className = 'typing-indicator';
    typing.id = 'typingIndicator';
    typing.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(typing);
    scrollToBottom();
  }

  function hideTyping() {
    var typing = document.getElementById('typingIndicator');
    if (typing) typing.remove();
  }

  // ---- Scroll to Bottom ----
  function scrollToBottom() {
    requestAnimationFrame(function () {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    });
  }

  // ---- Disable/Enable Input ----
  function setInputDisabled(disabled) {
    chatInput.disabled = disabled;
    chatSend.disabled = disabled;
    quickBtns.forEach(function (btn) { btn.disabled = disabled; });
  }

  // ---- Send Message to API ----
  function sendMessage(text) {
    if (!text || !text.trim()) return;

    var message = text.trim();

    // Add user message to UI
    addMessage(message, 'user');

    // Hide quick actions after first message
    var quickActions = document.querySelector('.chat-quick-actions');
    if (quickActions) {
      quickActions.style.display = 'none';
    }

    // Show typing and disable input
    showTyping();
    setInputDisabled(true);

    // API call
    fetch(CHAT_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        session_id: sessionId,
      }),
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Server returned ' + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        hideTyping();
        setInputDisabled(false);

        if (data.response) {
          // Format the response (handle newlines and basic markdown)
          var formatted = formatResponse(data.response);
          addBotMessageHTML(formatted);
        } else {
          addMessage('I received your message but couldn\'t generate a response. Please try again.', 'bot');
        }

        chatInput.focus();
      })
      .catch(function (error) {
        hideTyping();
        setInputDisabled(false);
        console.error('Chat API Error:', error);

        addErrorMessage('Unable to connect to our assistant. Please check your connection and try again.');
        chatInput.focus();
      });
  }

  // ---- Basic Markdown Formatting ----
  function formatResponse(text) {
    // Escape HTML
    var escaped = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Bold: **text**
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Bullet points
    escaped = escaped.replace(/^[\-•]\s+(.+)/gm, '<li>$1</li>');
    escaped = escaped.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // Numbered lists
    escaped = escaped.replace(/^\d+\.\s+(.+)/gm, '<li>$1</li>');

    // Line breaks
    escaped = escaped.replace(/\n/g, '<br>');

    // Clean up double <br> tags
    escaped = escaped.replace(/<br><br>/g, '<br>');

    return escaped;
  }

  // ---- Form Submit ----
  chatForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var message = chatInput.value;
    chatInput.value = '';
    sendMessage(message);
  });

  // ---- Quick Buttons ----
  quickBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var query = this.getAttribute('data-query');
      if (query) {
        sendMessage(query);
      }
    });
  });

  // ---- Enter Key Handling ----
  chatInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event('submit'));
    }
  });

})();
