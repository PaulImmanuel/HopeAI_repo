const chatWidget = document.getElementById("chatWidget");
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.querySelector(".send-btn");

let typingIndicator = null;
let isSending = false;
const TYPING_TIMEOUT_MS = 25000; // Auto-remove dots after 25 seconds

function toggleChat() {
  chatWidget.classList.toggle("open");
  if (chatWidget.classList.contains("open")) {
    setTimeout(() => userInput.focus(), 100);
  }
}

function appendMessage(text, senderClass) {
  const msg = document.createElement("div");
  msg.className = "message " + senderClass;
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
  return msg;
}

function showTypingIndicator() {
  // Remove any existing indicator first
  removeTypingIndicator();

  const msg = document.createElement("div");
  msg.className = "message bot typing-indicator";
  msg.id = "typing-indicator";
  msg.innerHTML = `<span></span><span></span><span></span>`;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
  typingIndicator = msg;

  // Safety: auto-remove after timeout so it never gets stuck forever
  typingIndicator._timeoutId = setTimeout(() => {
    removeTypingIndicator();
    appendMessage("The response is taking longer than expected. Please try again.", "bot");
    isSending = false;
    setSendEnabled(true);
  }, TYPING_TIMEOUT_MS);

  return msg;
}

function removeTypingIndicator() {
  if (typingIndicator) {
    if (typingIndicator._timeoutId) {
      clearTimeout(typingIndicator._timeoutId);
    }
    if (typingIndicator.parentNode === chatBox) {
      chatBox.removeChild(typingIndicator);
    }
    typingIndicator = null;
  }
}

function setSendEnabled(enabled) {
  if (sendBtn) sendBtn.disabled = !enabled;
  if (userInput) userInput.disabled = !enabled;
  if (!enabled) {
    if (sendBtn) sendBtn.style.opacity = "0.5";
    if (userInput) userInput.style.opacity = "0.7";
  } else {
    if (sendBtn) sendBtn.style.opacity = "1";
    if (userInput) userInput.style.opacity = "1";
    setTimeout(() => userInput.focus(), 50);
  }
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message || isSending) return;

  isSending = true;
  setSendEnabled(false);

  appendMessage(message, "user");
  userInput.value = "";

  showTypingIndicator();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({ message }),
    });

    clearTimeout(timeoutId);
    removeTypingIndicator();

    const data = await response.json();
    appendMessage(data.reply || "Sorry, I didn't get a response.", "bot");
  } catch (error) {
    removeTypingIndicator();
    if (error.name === "AbortError") {
      appendMessage("The request timed out. Please try again.", "bot");
    } else {
      appendMessage("Unable to reach the server. Please try again.", "bot");
    }
  } finally {
    isSending = false;
    setSendEnabled(true);
  }
}

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && !isSending) {
    e.preventDefault();
    sendMessage();
  }
});
