
const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");

const API_URL = "http://127.0.0.1:5000";

function addMessage(message, type) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(
        "message",
        type === "user" ? "user-message" : "bot-message"
    );

    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function askBackend(question) {
    const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Server error");
    }

    return data.answer;
}

async function sendQuestion() {
    const question = questionInput.value.trim();

    if (!question) return;

    addMessage(question, "user");
    questionInput.value = "";
    sendButton.disabled = true;

    const loadingMessage = document.createElement("div");
    loadingMessage.classList.add("message", "bot-message");
    loadingMessage.textContent = "Searching company knowledge...";
    chatMessages.appendChild(loadingMessage);

    try {
        const answer = await askBackend(question);
        loadingMessage.remove();
        addMessage(answer || "No answer received.", "bot");
    } catch (error) {
        loadingMessage.remove();
        console.error("Backend error:", error);
        addMessage(
            "Backend connection failed: " + error.message,
            "bot"
        );
    } finally {
        sendButton.disabled = false;
        questionInput.focus();
    }
}

sendButton.addEventListener("click", sendQuestion);

questionInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendQuestion();
    }
});

const exampleButtons = document.querySelectorAll(
    ".example-questions button"
);

exampleButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        questionInput.value = button.textContent.trim();
        questionInput.focus();
    });
});

const fileInput = document.getElementById("fileInput");

if (fileInput) {
    fileInput.addEventListener("change", async function() {
        if (!fileInput.files.length) return;

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append("file", file);

        addMessage("Uploading: " + file.name, "user");

        try {
            const response = await fetch(`${API_URL}/upload`, {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Upload failed");
            }

            addMessage(
                data.message + ": " + data.filename,
                "bot"
            );
        } catch (error) {
            console.error("Upload error:", error);
            addMessage("Upload failed: " + error.message, "bot");
        } finally {
            fileInput.value = "";
        }
    });
}
