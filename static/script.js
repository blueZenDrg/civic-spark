const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-message');
const sendButton = document.getElementById('send-button');
const generatePDFButton = document.getElementById('generate-pdf-button');
const generateReportButton = document.getElementById('generate-report-button');


let currentStep = 'start';
let ideaData = {};
let refiningQuestions = [];
let currentQuestionIndex = 0;
let refiningAnswers = [];

function addMessage(message, isUser = false) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', isUser ? 'user-message' : 'ai-message');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function processUserInput(input) {
    addMessage(input, true);

    switch (currentStep) {
        case 'start':
            ideaData.description = input;
            addMessage("Great! Now, please enter the country for your idea.");
            currentStep = 'country';
            break;
        case 'country':
            ideaData.country = input;
            addMessage("Excellent. What city is this idea for?");
            currentStep = 'city';
            break;
        case 'city':
            ideaData.city = input;
            addMessage("Thank you. Lastly, what's your age?");
            currentStep = 'age';
            break;
        case 'age':
            ideaData.user_age = parseInt(input);
            startIdeaProcess();
            break;
        case 'refining':
            handleRefiningQuestions(input);
            break;
        default:
            addMessage("I'm not sure how to process that input at this stage.");
    }
}

async function startIdeaProcess() {
    showLoadingIndicator('Starting the idea process...');
    const response = await fetch('/start_process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ideaData)
    });
    const data = await response.json();
    hideLoadingIndicator();
    currentStep = 'refining';
    refiningQuestions = data.questions;
    currentQuestionIndex = 0;
    refiningAnswers = [];
    askNextRefiningQuestion();
}

function askNextRefiningQuestion() {
    if (currentQuestionIndex < refiningQuestions.length) {
        addMessage(refiningQuestions[currentQuestionIndex]);
    } else {
        finishRefining();
    }
}

function handleRefiningQuestions(answer) {
    refiningAnswers.push(answer);
    currentQuestionIndex++;
    askNextRefiningQuestion();
}

async function finishRefining() {
    showLoadingIndicator('Refining your idea...');
    await fetch('/refine_idea', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: refiningAnswers })
    });
    hideLoadingIndicator();
    getGlobalExamples();
}

async function getGlobalExamples() {
    showLoadingIndicator('Fetching global examples...');
    const response = await fetch('/get_global_examples', { method: 'POST' });
    const data = await response.json();
    hideLoadingIndicator();
    data.examples.forEach(example => addMessage(example));
    assessFeasibility();
}

async function assessFeasibility() {
    showLoadingIndicator('Assessing feasibility...');
    const response = await fetch('/assess_feasibility', { method: 'POST' });
    const data = await response.json();
    hideLoadingIndicator();
    Object.entries(data.feasibility).forEach(([key, value]) => addMessage(`${key}: ${value}`));
    getBreakthroughs();
}

async function getBreakthroughs() {
    showLoadingIndicator('Fetching relevant breakthroughs...');
    const response = await fetch('/get_breakthroughs', { method: 'POST' });
    const data = await response.json();
    hideLoadingIndicator();
    data.breakthroughs.forEach(breakthrough => addMessage(breakthrough));
    getFullSolution();
}

async function getFullSolution() {
    showLoadingIndicator('Generating full solution...');
    const response = await fetch('/get_full_solution', { method: 'POST' });
    const data = await response.json();
    hideLoadingIndicator();
    addMessage("Here's the full solution for your idea:");
    addMessage(data.solution);
    currentStep = 'complete';
    generateReportButton.classList.remove('hidden');
}

generateReportButton.addEventListener('click', async () => {
    showLoadingIndicator('Generating HTML report...');
    const response = await fetch('/generate_report', { method: 'POST' });
    const data = await response.json();
    hideLoadingIndicator();
    if (data.success) {
        // Create a Blob with the HTML content
        const blob = new Blob([data.html_report], { type: 'text/html' });
        // Create a temporary URL for the Blob
        const url = window.URL.createObjectURL(blob);
        // Create a temporary anchor element
        const a = document.createElement('a');
        a.href = url;
        a.download = 'civic_idea_report.html';
        // Trigger the download
        document.body.appendChild(a);
        a.click();
        // Clean up
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        addMessage("HTML report generated and downloaded successfully.");
    } else {
        addMessage("There was an error generating the HTML report. Please try again.");
    }
});


function showLoadingIndicator(message) {
    const loadingIndicator = document.getElementById('loading-indicator');
    loadingIndicator.querySelector('.loading-text').textContent = message;
    loadingIndicator.classList.remove('hidden');
}

function hideLoadingIndicator() {
    document.getElementById('loading-indicator').classList.add('hidden');
}

sendButton.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        processUserInput(message);
        userInput.value = '';
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});

userInput.addEventListener('input', () => {
    document.getElementById('typing-indicator').classList.remove('hidden');
});

userInput.addEventListener('blur', () => {
    document.getElementById('typing-indicator').classList.add('hidden');
});

addMessage("Welcome to CivicSpark! Please describe your civic idea.");
