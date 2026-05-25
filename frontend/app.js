document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("user-input");
    const area = document.getElementById("message-area");
    let sid = localStorage.getItem("sessionId") || "sn_" + Math.random().toString(36).substring(2, 10);
    localStorage.setItem("sessionId", sid);

    function addBubble(text, sender) {
        const b = document.createElement("div");
        b.classList.add("bubble", sender); b.textContent = text;
        area.appendChild(b); area.scrollTop = area.scrollHeight;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); const msg = input.value.trim(); if(!msg) return;
        addBubble(msg, "user"); input.value = "";
        try {
            const res = await fetch("/api/chat", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ sessionId: sid, message: msg })
            });
            const data = await res.json();
            addBubble(data.reply || data.error, "assistant");
        } catch { addBubble("Connection error.", "assistant"); }
    });
    addBubble("Hello! Ask me anything about our system documentation rules.", "assistant");
});