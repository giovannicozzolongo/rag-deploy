var defined = false;      // health checked at least once

function qs(sel) { return document.querySelector(sel); }

async function checkHealth() {
    try {
        const r = await fetch(location.origin + "/health", { signal: AbortSignal.timeout(5000) });
        const h = await r.json();
        qs("#health-dot").className = "health-dot " + (h.status === "ok" ? "ok" : "degraded");
        qs("#health-text").textContent = h.status === "ok" ? "connected" : "degraded";
    } catch {
        qs("#health-dot").className = "health-dot down";
        qs("#health-text").textContent = "offline";
    }
    defined = true;
}

function useExample(btn) {
    qs("#query-input").value = btn.textContent;
    sendQuery();
}

function clearEmpty() {
    var s = qs("#empty-state");
    if (s) s.remove();
}

function toBottom() {
    var a = qs("#chat-area");
    a.scrollTop = a.scrollHeight;
}

function safe(text) {
    var d = document.createElement("div");
    d.textContent = text;
    return d.innerHTML;
}

function renderMd(text) {
    return text
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^/, '<p>').replace(/$/, '</p>');
}

function pushUserMsg(text) {
    clearEmpty();
    var div = document.createElement("div");
    div.className = "msg msg-user";
    div.innerHTML = '<div class="msg-bubble">' + safe(text) + '</div>';
    qs("#chat-area").appendChild(div);
    toBottom();
}

function showLoading() {
    var div = document.createElement("div");
    div.className = "msg msg-assistant";
    div.id = "loading-msg";
    div.innerHTML = '<div class="loading-indicator">searching</div>';
    qs("#chat-area").appendChild(div);
    toBottom();
}

function hideLoading() {
    var x = qs("#loading-msg");
    if (x) x.remove();
}

function pushAnswer(data) {
    hideLoading();
    var div = document.createElement("div");
    div.className = "msg msg-assistant";

    var src = data.sources.map(function(s) {
        return '<div class="source-item">' +
            '<div class="source-header"><span class="source-name">' + safe(s.source) + ' p.' + s.page + '</span>' +
            '<span class="source-score">' + s.score.toFixed(3) + '</span></div>' +
            '<div class="source-preview">' + safe(s.text.slice(0, 180)) + '\u2026</div></div>';
    }).join("");

    div.innerHTML =
        '<div class="msg-answer">' + renderMd(data.answer) + '</div>' +
        '<div class="msg-meta"><span>' + safe(data.model) + '</span><span>' + data.latency_s + 's</span>' +
        '<button class="sources-toggle" onclick="toggleSources(this)">' +
        data.sources.length + ' sources <span class="arrow">\u25BE</span></button></div>' +
        '<div class="sources-list">' + src + '</div>';

    qs("#chat-area").appendChild(div);
    toBottom();
}

function pushError(text) {
    hideLoading();
    var div = document.createElement("div");
    div.className = "msg msg-assistant";
    div.innerHTML = '<div class="msg-answer" style="border-color:var(--red);color:var(--red);">' + safe(text) + '</div>';
    qs("#chat-area").appendChild(div);
    toBottom();
}

function toggleSources(btn) {
    btn.classList.toggle("open");
    btn.closest(".msg-assistant").querySelector(".sources-list").classList.toggle("show");
}

async function sendQuery() {
    var input = qs("#query-input");
    var q = input.value.trim();
    if (!q) return;

    input.value = "";
    qs("#send-btn").disabled = true;
    pushUserMsg(q);
    showLoading();

    try {
        var resp = await fetch(location.origin + "/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: q, top_k: 5 }),
        });
        if (!resp.ok) {
            var err = await resp.json().catch(function() { return { detail: "request failed" }; });
            pushError(err.detail || "Error " + resp.status);
        } else {
            pushAnswer(await resp.json());
        }
    } catch {
        pushError("Can't reach the API. Is the backend running?");
    }

    qs("#send-btn").disabled = false;
    input.focus();
}

document.addEventListener("DOMContentLoaded", function() {
    checkHealth();
    setInterval(checkHealth, 30000);
    var input = qs("#query-input");
    input.focus();
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendQuery(); }
    });
});
