from flask import Flask, render_template_string, request, jsonify
import re
import math

app = Flask(__name__)

HTML_PAGE = '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta name="description" content="A simple educational password strength checker.">\n  <title>Password Strength Checker</title>\n  <style>\n    :root { --bg:#0b1220; --panel:#121d31; --panel2:#17243a; --text:#eef4ff; --muted:#a7b6cc; --accent:#60a5fa; --border:#2a3a54; }\n    * { box-sizing:border-box; }\n    body { margin:0; min-height:100vh; padding:32px 16px; display:grid; place-items:center; font-family:Inter,system-ui,-apple-system,Segoe UI,Arial,sans-serif; color:var(--text); background:radial-gradient(ellipse at top,#1a3153 0%,var(--bg) 60%); }\n    .shell { width:100%; max-width:620px; }\n    .brand { text-align:center; margin-bottom:22px; }\n    .brand-icon { width:58px; height:58px; margin:0 auto 12px; display:grid; place-items:center; border:1px solid #36577e; border-radius:18px; background:#172c49; font-size:28px; }\n    h1 { margin:0; font-size:clamp(1.7rem,5vw,2.35rem); letter-spacing:-.04em; }\n    .subtitle { color:var(--muted); line-height:1.6; margin:10px auto 0; max-width:470px; }\n    .card { background:rgba(18,29,49,.96); border:1px solid var(--border); border-radius:22px; padding:clamp(20px,5vw,32px); box-shadow:0 24px 70px #0005; }\n    label { display:block; font-size:.94rem; font-weight:650; margin-bottom:10px; }\n    .input-row { display:flex; gap:8px; }\n    input[type=password], input[type=text] { flex:1; min-width:0; color:var(--text); background:#0b1425; border:1px solid #3a4b66; border-radius:12px; padding:14px; font-size:1rem; outline:none; }\n    input:focus { border-color:var(--accent); box-shadow:0 0 0 3px #60a5fa25; }\n    button { border:1px solid #405575; background:#1c2c44; color:var(--text); border-radius:12px; padding:0 14px; cursor:pointer; font-weight:650; }\n    button:hover { background:#263c5a; }\n    .privacy { color:var(--muted); font-size:.82rem; line-height:1.5; margin:10px 0 22px; }\n    .result { border:1px solid var(--border); border-radius:16px; padding:18px; background:#0e192b; }\n    .result-top { display:flex; align-items:center; justify-content:space-between; gap:12px; }\n    .result h2 { margin:0; font-size:1rem; }\n    .status { font-weight:750; }\n    .meter { height:9px; background:#27364d; border-radius:99px; overflow:hidden; margin:14px 0 8px; }\n    .meter-fill { height:100%; width:0; border-radius:99px; transition:width .2s ease; background:#64748b; }\n    .meter-caption { color:var(--muted); font-size:.82rem; }\n    .section-title { margin:22px 0 10px; font-size:.95rem; }\n    .checks { list-style:none; padding:0; margin:0; display:grid; grid-template-columns:1fr 1fr; gap:10px; }\n    .checks li { color:var(--muted); font-size:.88rem; display:flex; gap:8px; align-items:flex-start; }\n    .checks li.pass { color:#a7f3d0; }\n    .suggestions { margin:0; padding-left:20px; color:var(--muted); line-height:1.65; font-size:.9rem; }\n    .entropy { margin-top:15px; color:var(--muted); font-size:.8rem; }\n    .notice { margin-top:18px; border-radius:12px; padding:12px 14px; background:#17283e; color:#c5d7ef; font-size:.82rem; line-height:1.55; }\n    .error { color:#fca5a5; margin-top:12px; }\n    footer { text-align:center; color:#8496b0; font-size:.78rem; margin-top:18px; }\n    @media (max-width:480px) { .checks { grid-template-columns:1fr; } .input-row { flex-direction:column; } button { padding:12px; } .result-top { align-items:flex-start; flex-direction:column; } }\n  </style>\n</head>\n<body>\n  <main class="shell">\n    <header class="brand">\n      <div class="brand-icon" aria-hidden="true">🔐</div>\n      <h1>Password Strength Checker</h1>\n      <p class="subtitle">Get a quick estimate of password strength and practical tips for creating a less predictable password.</p>\n    </header>\n\n    <section class="card" aria-label="Password checker">\n      <label for="password">Try a sample password</label>\n      <div class="input-row">\n        <input id="password" type="password" autocomplete="off" spellcheck="false" maxlength="1024" placeholder="Enter a sample password" aria-describedby="privacy">\n        <button id="toggle" type="button" aria-label="Show password" aria-pressed="false">Show</button>\n      </div>\n      <p class="privacy" id="privacy">Privacy: this demo sends the entered sample to its own Flask endpoint for checking. Do not enter a password you currently use for a real account.</p>\n\n      <div class="result" aria-live="polite">\n        <div class="result-top">\n          <h2>Strength result</h2>\n          <span class="status" id="status">Waiting for input</span>\n        </div>\n        <div class="meter" role="progressbar" aria-label="Password strength" aria-valuemin="0" aria-valuemax="5" aria-valuenow="0" id="meter">\n          <div class="meter-fill" id="meterFill"></div>\n        </div>\n        <div class="meter-caption" id="meterCaption">Enter a sample password to begin.</div>\n\n        <h3 class="section-title">Password checklist</h3>\n        <ul class="checks" id="checks">\n          <li>○ At least 12 characters</li>\n          <li>○ Lowercase letters</li>\n          <li>○ Uppercase letters</li>\n          <li>○ Numbers</li>\n          <li>○ Special characters</li>\n        </ul>\n\n        <h3 class="section-title">Suggestions</h3>\n        <ul class="suggestions" id="suggestions"><li>Use a long, unique password that is difficult to guess.</li></ul>\n        <p class="entropy" id="entropy"></p>\n        <p class="error" id="error" role="alert" hidden></p>\n      </div>\n\n      <div class="notice"><strong>Remember:</strong> a strength score is only an estimate. Use a unique password for each account, consider a password manager, and enable multi-factor authentication.</div>\n    </section>\n    <footer>Educational cybersecurity project · Flask + HTML/CSS/JavaScript</footer>\n  </main>\n\n  <script>\n    const passwordInput = document.getElementById("password");\n    const toggleButton = document.getElementById("toggle");\n    const statusText = document.getElementById("status");\n    const meterFill = document.getElementById("meterFill");\n    const meter = document.getElementById("meter");\n    const meterCaption = document.getElementById("meterCaption");\n    const checksList = document.getElementById("checks");\n    const suggestionsList = document.getElementById("suggestions");\n    const entropyText = document.getElementById("entropy");\n    const errorText = document.getElementById("error");\n    let debounceTimer;\n\n    const colors = {\n      "Very Weak": "#f87171",\n      "Weak": "#fb923c",\n      "Moderate": "#facc15",\n      "Strong": "#60a5fa",\n      "Very Strong": "#34d399",\n      "Not entered": "#64748b"\n    };\n\n    function addListItem(list, text, className = "") {\n      const li = document.createElement("li");\n      li.textContent = text;\n      if (className) li.className = className;\n      list.appendChild(li);\n    }\n\n    function resetDisplay() {\n      statusText.textContent = "Waiting for input";\n      statusText.style.color = "";\n      meterFill.style.width = "0%";\n      meterFill.style.background = "#64748b";\n      meter.setAttribute("aria-valuenow", "0");\n      meterCaption.textContent = "Enter a sample password to begin.";\n      checksList.replaceChildren();\n      ["At least 12 characters", "Lowercase letters", "Uppercase letters", "Numbers", "Special characters"].forEach(x => addListItem(checksList, "○ " + x));\n      suggestionsList.replaceChildren();\n      addListItem(suggestionsList, "Use a long, unique password that is difficult to guess.");\n      entropyText.textContent = "";\n      errorText.hidden = true;\n    }\n\n    function displayResult(data) {\n      const color = colors[data.label] || "#64748b";\n      statusText.textContent = data.label;\n      statusText.style.color = color;\n      meterFill.style.width = `${(data.score / 5) * 100}%`;\n      meterFill.style.background = color;\n      meter.setAttribute("aria-valuenow", String(data.score));\n      meterCaption.textContent = `${data.score} out of 5 password checks passed`;\n      checksList.replaceChildren();\n      data.checks.forEach(item => {\n        addListItem(checksList, `${item.passed ? "✓" : "○"} ${item.name}`, item.passed ? "pass" : "");\n      });\n      suggestionsList.replaceChildren();\n      data.suggestions.forEach(item => addListItem(suggestionsList, item));\n      entropyText.textContent = `Approximate character-pool entropy: ${data.entropy} bits (educational estimate only).`;\n      errorText.hidden = true;\n    }\n\n    async function checkPassword(value) {\n      if (!value) {\n        resetDisplay();\n        return;\n      }\n      try {\n        const response = await fetch("/check", {\n          method: "POST",\n          headers: { "Content-Type": "application/json" },\n          body: JSON.stringify({ password: value })\n        });\n        const data = await response.json();\n        if (!response.ok) throw new Error(data.error || "Unable to check this input.");\n        displayResult(data);\n      } catch (error) {\n        errorText.textContent = error.message || "Could not connect to the checker. Please try again.";\n        errorText.hidden = false;\n      }\n    }\n\n    passwordInput.addEventListener("input", () => {\n      clearTimeout(debounceTimer);\n      const value = passwordInput.value;\n      if (!value) {\n        resetDisplay();\n        return;\n      }\n      debounceTimer = setTimeout(() => checkPassword(value), 180);\n    });\n\n    toggleButton.addEventListener("click", () => {\n      const showing = passwordInput.type === "password";\n      passwordInput.type = showing ? "text" : "password";\n      toggleButton.textContent = showing ? "Hide" : "Show";\n      toggleButton.setAttribute("aria-pressed", String(showing));\n      toggleButton.setAttribute("aria-label", showing ? "Hide password" : "Show password");\n    });\n  </script>\n</body>\n</html>\n'


SPECIAL_CHARS = r"""!@#$%^&*(),.?":{}|<>[]/\-_+=;~`'"""

def check_password(password):
    """Return a strength score, label, checks, and suggestions for a password."""
    if not isinstance(password, str) or not password:
        return {
            "score": 0,
            "label": "Not entered",
            "checks": [],
            "suggestions": ["Enter a sample password to check its strength."],
            "entropy": 0.0,
        }

    checks = [
        {"name": "At least 12 characters", "passed": len(password) >= 12},
        {"name": "Contains lowercase letters", "passed": bool(re.search(r"[a-z]", password))},
        {"name": "Contains uppercase letters", "passed": bool(re.search(r"[A-Z]", password))},
        {"name": "Contains numbers", "passed": bool(re.search(r"\d", password))},
        {"name": "Contains special characters", "passed": bool(re.search(r"[^A-Za-z0-9]", password))},
    ]

    # Approximate character pool used only for an educational estimate.
    pool_size = 0
    if re.search(r"[a-z]", password):
        pool_size += 26
    if re.search(r"[A-Z]", password):
        pool_size += 26
    if re.search(r"\d", password):
        pool_size += 10
    if re.search(r"[^A-Za-z0-9]", password):
        pool_size += 32
    entropy = len(password) * math.log2(pool_size) if pool_size > 1 else 0.0

    score = sum(item["passed"] for item in checks)
    suggestions = [item["name"] for item in checks if not item["passed"]]

    common_patterns = [
        r"password", r"qwerty", r"12345", r"abcde", r"admin",
        r"letmein", r"welcome", r"(.)\1{2,}"
    ]
    looks_common = any(re.search(pattern, password, re.IGNORECASE) for pattern in common_patterns)
    if looks_common:
        score = max(0, score - 2)
        suggestions.append("Avoid common words, predictable sequences, and repeated characters.")

    if len(password) < 8:
        suggestions.append("Use a longer password. Aim for at least 12 characters.")
    elif len(password) < 12:
        suggestions.append("Consider using 12–16 or more characters.")

    if not suggestions:
        suggestions.append("Good job. Use a unique password for every account and enable multi-factor authentication.")

    if looks_common:
        label = "Very Weak" if score <= 1 else "Weak"
    elif score <= 1:
        label = "Very Weak"
    elif score == 2:
        label = "Weak"
    elif score == 3:
        label = "Moderate"
    elif score == 4:
        label = "Strong"
    else:
        label = "Very Strong"

    return {
        "score": int(score),
        "label": label,
        "checks": checks,
        "suggestions": suggestions,
        "entropy": round(entropy, 1),
    }


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/check", methods=["POST"])
def check():
    if not request.is_json:
        return jsonify({"error": "Send a JSON request."}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data."}), 400

    password = data.get("password")
    if not isinstance(password, str):
        return jsonify({"error": "Password must be text."}), 400

    if len(password) > 1024:
        return jsonify({"error": "Please enter a password under 1025 characters."}), 400

    return jsonify(check_password(password))


if __name__ == "__main__":
    # Local development only. Use a production WSGI server such as gunicorn when deploying.
    app.run(host="127.0.0.1", port=5000, debug=False)
