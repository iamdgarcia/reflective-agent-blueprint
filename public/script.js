// Reflective Agent Frontend JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const iterationsList = document.getElementById('iterations-list');
    let conversationHistory = [];
    
    function addMessage(content, type = 'assistant') {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.innerHTML = `<div class="message-content">${content}</div><div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function displayIterations(iterations, finalScore) {
        iterationsList.innerHTML = '';
        iterations.forEach(iter => {
            const scoreClass = iter.critique.score >= 0.8 ? 'score-high' : (iter.critique.score >= 0.6 ? 'score-medium' : 'score-low');
            const itemDiv = document.createElement('div');
            itemDiv.className = 'iteration-item';
            itemDiv.innerHTML = `<div class="iteration-header">Iteration ${iter.iteration} <span class="score-badge ${scoreClass}">Score: ${iter.critique.score.toFixed(2)}</span></div><div class="iteration-issues">${iter.critique.issues.length > 0 ? 'Issues: ' + iter.critique.issues.join(', ') : 'No issues found'}</div>`;
            iterationsList.appendChild(itemDiv);
        });
        
        const finalDiv = document.createElement('div');
        finalDiv.style.marginTop = '10px';
        finalDiv.style.fontWeight = 'bold';
        finalDiv.textContent = `Final Score: ${finalScore.toFixed(2)}`;
        iterationsList.appendChild(finalDiv);
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        userInput.disabled = sendButton.disabled = true;
        sendButton.textContent = 'Reflecting...';
        addMessage(message, 'user');
        userInput.value = '';
        
        try {
            const response = await fetch('/.netlify/functions/reflective-agent', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, history: conversationHistory })
            });
            
            const data = await response.json();
            addMessage(data.response, 'assistant');
            displayIterations(data.iterations, data.final_score);
            conversationHistory = data.history;
        } catch (error) {
            addMessage('Error processing request.', 'assistant');
        } finally {
            userInput.disabled = sendButton.disabled = false;
            sendButton.textContent = 'Send';
            userInput.focus();
        }
    }
    
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
    userInput.focus();
    addMessage('Hello! I am a Reflective Agent. I generate responses, then self-critique and improve them through multiple iterations. Try asking me to explain something or write code.', 'assistant');
});