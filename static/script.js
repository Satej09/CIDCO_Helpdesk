
let state         = "GREETING";
let dept_key      = null;
let awaitingInput = false;

const chat    = document.getElementById("chat");
const input   = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

chat.addEventListener("click", function (e) {
  const btn = e.target.closest(".opt-btn");
  if (!btn || btn.disabled) return;
  const key = btn.getAttribute("data-key");
  if (key) sendToServer(key);
});

function scrollBottom() {
  setTimeout(() => (chat.scrollTop = chat.scrollHeight), 50);
}

function addMsg(text, who = "bot") {
  const row     = document.createElement("div");
  row.className = `msg ${who}`;
  const avatar  = who === "bot" ? "🏛️" : "👤";
  row.innerHTML = `<div class="avatar">${avatar}</div><div class="bubble">${text}</div>`;
  chat.appendChild(row);
  scrollBottom();
}

function addBotWithOptions(text, options) {
  const row     = document.createElement("div");
  row.className = "msg bot";

  let optHTML = `<div class="options-grid">`;
  for (const opt of options) {
    const cls = opt.key === "0" ? "opt-btn exit-btn"
              : opt.key === "9" ? "opt-btn back-btn"
              : "opt-btn";
    optHTML += `<button class="${cls}" data-key="${opt.key}">
      <span class="num">${opt.key}</span> ${opt.label}
    </button>`;
  }
  optHTML += `</div>`;

  row.innerHTML = `<div class="avatar">🏛️</div><div class="bubble">${text}${optHTML}</div>`;
  chat.appendChild(row);
  scrollBottom();
}

function showTyping(cb, delay = 800) {
  const row     = document.createElement("div");
  row.className = "msg bot";
  row.id        = "typing-row";
  row.innerHTML = `<div class="avatar">🏛️</div>
    <div class="typing"><span></span><span></span><span></span></div>`;
  chat.appendChild(row);
  scrollBottom();
  setTimeout(() => {
    const el = document.getElementById("typing-row");
    if (el) el.remove();
    cb();
  }, delay);
}

function disableOptions() {
  document.querySelectorAll(".opt-btn").forEach(btn => {
    btn.disabled      = true;
    btn.style.opacity = "0.4";
    btn.style.cursor  = "default";
  });
}

function addRestartBtn() {
  const btn       = document.createElement("button");
  btn.className   = "restart-btn";
  btn.textContent = "↺ Start a new session";
  btn.addEventListener("click", () => {
    chat.innerHTML = "";
    startSession();
  });
  chat.appendChild(btn);
  scrollBottom();
}

function sendToServer(userInput) {
  disableOptions();

  fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ state, input: userInput, dept_key })
  })
  .then(res => res.json())
  .then(data => {
  
    state    = data.state;
    dept_key = data.dept_key;

    showTyping(() => {
      if (data.options && data.options.length > 0) {
        addBotWithOptions(data.message, data.options);
      } else {
        addMsg(data.message);
      }

      if (state === "DONE") addRestartBtn();
    });
  })
  .catch(err => {
    console.error("API error:", err);
    addMsg("⚠️ Something went wrong. Please try again.");
  });
}

function handleSend() {
  if (!awaitingInput) return;
  const val = input.value.trim();
  if (!val) return;
  input.value      = "";
  awaitingInput    = false;
  sendBtn.disabled = true;
  addMsg(val, "user");
  sendToServer(val);
}

input.addEventListener("keydown", e => { if (e.key === "Enter") handleSend(); });
sendBtn.addEventListener("click", handleSend);


setInterval(() => {
  if (awaitingInput) {
    sendBtn.disabled  = false;
    input.placeholder = state === "GREETING" ? "Type your name…" : "Type here…";
  } else {
    sendBtn.disabled  = true;
    input.placeholder = "Choose an option above…";
  }
}, 200);

function startSession() {
  state            = "GREETING";
  dept_key         = null;
  awaitingInput    = true;
  sendBtn.disabled = false;

  showTyping(() => {
    addMsg('<span class="greeting-emoji">🙏</span> <strong>Namaste!</strong> Welcome to CIDCO Unified Helpdesk.');
    showTyping(() => {
      addMsg("May I know your name?");
      input.focus();
    }, 500);
  }, 700);
}

startSession();
