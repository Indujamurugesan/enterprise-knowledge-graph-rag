// ==========================================
// HTML Elements
// ==========================================

const questionInput =
    document.getElementById("questionInput");

const sendButton =
    document.getElementById("sendButton");

const chatMessages =
    document.getElementById("chatMessages");


// ==========================================
// Add Message
// ==========================================

function addMessage(message, type) {

    const messageDiv =
        document.createElement("div");

    messageDiv.classList.add(
        "message",
        type === "user"
            ? "user-message"
            : "bot-message"
    );

    messageDiv.textContent = message;

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ==========================================
// Ask Backend API
// ==========================================

async function askBackend(question) {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Server error"
            );
        }


        return data.answer;


    } catch (error) {

        console.error(error);

        return (
            "❌ Unable to connect to the "
            + "Enterprise RAG backend."
        );
    }
}


// ==========================================
// Send Question
// ==========================================

async function sendQuestion() {

    const question =
        questionInput.value.trim();


    if (question === "") {
        return;
    }


    // Show user question
    addMessage(
        question,
        "user"
    );


    // Clear input
    questionInput.value = "";


    // Disable button while processing
    sendButton.disabled = true;

    sendButton.textContent = "⏳";


    // Show temporary message
    const loadingMessage =
        document.createElement("div");

    loadingMessage.classList.add(
        "message",
        "bot-message"
    );

    loadingMessage.textContent =
        "🔍 Searching company knowledge...";

    chatMessages.appendChild(
        loadingMessage
    );


    // Ask Python backend
    const answer =
        await askBackend(question);


    // Remove loading message
    loadingMessage.remove();


    // Show AI answer
    addMessage(
        answer,
        "bot"
    );


    // Enable button
    sendButton.disabled = false;

    sendButton.textContent = "➤";
}


// ==========================================
// Send Button
// ==========================================

sendButton.addEventListener(
    "click",
    sendQuestion
);


// ==========================================
// Enter Key
// ==========================================

questionInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();
        }
    }
);


// ==========================================
// Example Questions
// ==========================================

const exampleButtons =
    document.querySelectorAll(
        ".example-questions button"
    );


exampleButtons.forEach(
    function(button) {

        button.addEventListener(
            "click",
            function() {

                questionInput.value =
                    button.textContent.trim();

                questionInput.focus();
            }
        );

    }
);


// ==========================================
// File Upload UI
// ==========================================

// ==========================================
// File Upload
// ==========================================

const fileInput =
    document.getElementById("fileInput");


fileInput.addEventListener(
    "change",
    async function() {

        if (fileInput.files.length === 0) {
            return;
        }


        const file =
            fileInput.files[0];


        // Show selected file
        addMessage(
            `📄 Uploading: ${file.name}`,
            "user"
        );


        // Create FormData
        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:5000/upload",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Upload failed"
                );
            }


            addMessage(
                `✅ ${data.message}: ${data.filename}`,
                "bot"
            );


        } catch (error) {

            console.error(error);

            addMessage(
                `❌ Upload failed: ${error.message}`,
                "bot"
            );
        }


        // Reset file input
        fileInput.value = "";
    }
);