/**
 * Tiger Logistics Chat Widget
 * Connects to Project Dwight Backend API
 */

// Configuration - Update API_BASE_URL after deploying backend to Railway
const CONFIG = {
    // For local development: 'http://127.0.0.1:8000'
    // For production: Your Railway URL like 'https://dwight-backend-production.up.railway.app'
    API_BASE_URL: 'https://dwight-the-chatbot-international-freight-fo-production.up.railway.app',
    ENDPOINTS: {
        CHAT: '/api/chat',
        LEAD: '/api/lead',
        HEALTH: '/health'
    }
};

// DOM Elements
const chatToggle = document.getElementById('chatToggle');
const chatWidget = document.getElementById('chatWidget');
const minimizeBtn = document.getElementById('minimizeBtn');
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');
const quickActions = document.getElementById('quickActions');
const leadModal = document.getElementById('leadModal');
const modalClose = document.getElementById('modalClose');
const leadForm = document.getElementById('leadForm');

// State
let isOpen = false;
let isProcessing = false;
let conversationHistory = [];

// =============================================
// Initialization
// =============================================
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    checkBackendHealth();
});

function initEventListeners() {
    // Toggle chat widget
    chatToggle.addEventListener('click', toggleChat);
    minimizeBtn.addEventListener('click', toggleChat);
    
    // Send message
    chatForm.addEventListener('submit', handleSubmit);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    });
    
    // Quick action buttons
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const message = btn.dataset.message;
            if (message) {
                sendMessage(message);
                // Hide quick actions after first use
                quickActions.classList.add('hidden');
            }
        });
    });
    
    // Lead modal
    modalClose.addEventListener('click', () => leadModal.classList.add('hidden'));
    leadModal.addEventListener('click', (e) => {
        if (e.target === leadModal) leadModal.classList.add('hidden');
    });
    leadForm.addEventListener('submit', handleLeadSubmit);
}

// =============================================
// Chat Toggle
// =============================================
function toggleChat() {
    isOpen = !isOpen;
    chatWidget.classList.toggle('hidden', !isOpen);
    chatToggle.classList.toggle('active', isOpen);
    
    if (isOpen) {
        chatInput.focus();
    }
}

// =============================================
// Message Handling
// =============================================
async function handleSubmit(e) {
    e.preventDefault();
    const message = chatInput.value.trim();
    
    if (!message || isProcessing) return;
    
    sendMessage(message);
}

async function sendMessage(message) {
    if (isProcessing) return;
    
    // Add user message to UI
    addMessage(message, 'user');
    chatInput.value = '';
    
    // Hide quick actions after first message
    quickActions.classList.add('hidden');
    
    // Show typing indicator
    isProcessing = true;
    showTyping();
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.CHAT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        hideTyping();
        
        if (response.ok) {
            addMessage(data.response, 'bot');
            
            // Store conversation
            conversationHistory.push({
                user: message,
                bot: data.response,
                intent: data.intent,
                timestamp: data.timestamp
            });
            
            // Check if lead prompt is suggested
            if (data.lead_prompt) {
                setTimeout(() => showLeadPrompt(), 1000);
            }
        } else {
            addMessage("I'm having trouble right now. Please try again or contact us at info@tigerlogistics.in", 'bot');
        }
    } catch (error) {
        console.error('Chat error:', error);
        hideTyping();
        addMessage("I'm unable to connect right now. Please check your connection or contact us at +91 22 4015 7070", 'bot');
    } finally {
        isProcessing = false;
    }
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Convert markdown-like formatting
    const formattedContent = formatMessage(content);
    contentDiv.innerHTML = `<p>${formattedContent}</p>`;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

function formatMessage(text) {
    // Convert newlines to <br>
    let formatted = text.replace(/\n/g, '<br>');
    
    // Convert bullet points
    formatted = formatted.replace(/^- (.+)$/gm, '• $1');
    
    // Bold text between **
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    return formatted;
}

function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

function showTyping() {
    typingIndicator.classList.remove('hidden');
    scrollToBottom();
}

function hideTyping() {
    typingIndicator.classList.add('hidden');
}

// =============================================
// Lead Capture
// =============================================
function showLeadPrompt() {
    // Add a prompt message
    addMessage("I'd love to connect you with our team for personalized assistance. Would you like to share your contact details for a callback?", 'bot');
    
    // Add action buttons
    const actionDiv = document.createElement('div');
    actionDiv.className = 'message bot';
    actionDiv.innerHTML = `
        <div class="message-content">
            <div style="display: flex; gap: 10px; margin-top: 8px;">
                <button onclick="openLeadModal()" style="padding: 8px 16px; background: #FF6B00; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 500;">Yes, Contact Me</button>
                <button onclick="this.parentElement.parentElement.parentElement.remove()" style="padding: 8px 16px; background: #e9ecef; color: #333; border: none; border-radius: 6px; cursor: pointer;">No Thanks</button>
            </div>
        </div>
    `;
    chatMessages.appendChild(actionDiv);
    scrollToBottom();
}

function openLeadModal() {
    leadModal.classList.remove('hidden');
    document.getElementById('leadName').focus();
}

async function handleLeadSubmit(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('leadName').value,
        email: document.getElementById('leadEmail').value,
        phone: document.getElementById('leadPhone').value || '',
        company: document.getElementById('leadCompany').value || '',
        message: document.getElementById('leadMessage').value || '',
        source: 'chat_widget',
        conversation_context: conversationHistory.slice(-5) // Last 5 messages
    };
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.LEAD}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            // Close modal
            leadModal.classList.add('hidden');
            leadForm.reset();
            
            // Show success message
            addMessage(`Thank you, ${formData.name}! 🎉 Our team will reach out to you within 24 hours at ${formData.email}. In the meantime, feel free to ask me any other questions.`, 'bot');
        } else {
            alert('There was an error submitting your details. Please try again or call us directly.');
        }
    } catch (error) {
        console.error('Lead submission error:', error);
        alert('Unable to submit. Please contact us at info@tigerlogistics.in or +91 22 4015 7070');
    }
}

// =============================================
// Health Check
// =============================================
async function checkBackendHealth() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.HEALTH}`);
        const data = await response.json();
        console.log('Backend health:', data);
    } catch (error) {
        console.warn('Backend not reachable:', error);
        // Optionally show offline status
    }
}

// Global function for inline buttons
window.openLeadModal = openLeadModal;
