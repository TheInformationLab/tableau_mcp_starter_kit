// Simple chat functionality

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    // Don't send empty messages
    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    // Disable button while processing
    const btn = document.getElementById('sendBtn');
    btn.disabled = true;
    btn.textContent = 'Thinking...';

    try {
        // Send message to the API
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        if (response.ok) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('Sorry, something went wrong! Please try again.', 'bot');
        }
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I couldn\'t connect to the server. Please try again.', 'bot');
    }
    
    // Re-enable the send button
    btn.disabled = false;
    btn.textContent = 'Send';
}

function addMessage(text, type) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = text.replace(/\n/g, '<br>');
    chatBox.appendChild(messageDiv);
    
    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

function handleEnter(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Focus on input when page loads
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('messageInput').focus();
});