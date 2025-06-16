document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const faqsContainer = document.getElementById('faqs-container');


    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("You", message, "user");
        userInput.value = "";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            appendMessage("Coucou", data.reply, "bot");
        } catch (error) {
            console.error('Error sending message to chatbot:', error);
            appendMessage("Coucou", "Oops! I couldn't connect right now. Please try again later.", "bot error");
        }
    });

    function appendMessage(sender, text, type) {
        const msgWrapper = document.createElement('div');
        msgWrapper.classList.add('chat-bubble', type);

        msgWrapper.innerHTML = `
            <div><strong>${sender}:</strong></div>
            <div>${text}</div>
        `;

        chatBox.appendChild(msgWrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }


    const faqData = [
        {
            question: "What does 'Coucou' mean?",
            answer: "Coucou is a sweet, sincere way of saying hi, normally reserved for close friends and family."
        },
        {
            question: "What is the inspiration behind this chatbot?",
            answer: "Immersion is the best language tool; the human brain can naturally pick up phrases. Hence, this chatbot is a low-effort language learning tool – just talk to it daily!"
        },
        {
            question: "What are the features of this chatbot?",
            answer: "This chatbot offers time-based greetings, guides you through basic French conversations like introductions and daily inquiries, and provides English-to-French translation. It also includes humorous elements (memes) and lets you end or restart the chat with mood-based farewells."
        },
        {
            question: "How was this chatbot made?",
            answer: "It's built using Python, Flask, HTML, CSS, JS, and is powered by a self-hosted LibreTranslate API, thanks to Docker."
        }
    ];

    function renderFAQs() {
        faqData.forEach(item => {
            const article = document.createElement('article');
            article.className = 'faq-item';

            const markup = `
                <div class="item-question">
                    <span class="question-text">${item.question}</span>
                    <span class="arrows-container">
                        <span class="expand">🔻</span>
                        <span class="close">🔺</span>
                    </span>
                </div>
                <div class="item-answer">
                    <span class="answer-text">${item.answer}</span>
                </div>
            `;

            article.innerHTML = markup;
            faqsContainer.appendChild(article);
        });
    }

    faqsContainer.addEventListener('click', (e) => {
        const itemQuestion = e.target.closest('.item-question');
        if (itemQuestion) {
            const parent = itemQuestion.parentElement;
            parent.classList.toggle('show-answer');
        }
    });

    renderFAQs();
});