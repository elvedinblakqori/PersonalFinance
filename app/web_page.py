def get_homepage_html() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Personal Finance Tracker</title>
  <style>
    :root {
      --bg: #f3f7fb;
      --card: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --brand: #0f766e;
      --brand-2: #115e59;
      --danger: #b91c1c;
      --border: #dbe4ee;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(120deg, #e6f4ff 0%, var(--bg) 45%, #f8fafc 100%);
      color: var(--text);
    }
    .wrap {
      max-width: 1100px;
      margin: 24px auto;
      padding: 0 16px 24px;
    }
    h1 {
      margin: 0 0 6px;
      font-size: 2rem;
    }
    p { color: var(--muted); margin-top: 0; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
    }
    .card h2 {
      margin: 0 0 10px;
      font-size: 1.05rem;
    }
    label { display: block; font-size: 0.85rem; margin: 8px 0 4px; color: #374151; }
    input, button {
      width: 100%;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      padding: 10px;
      font-size: 0.95rem;
    }
    button {
      border: none;
      background: var(--brand);
      color: white;
      font-weight: 600;
      cursor: pointer;
      margin-top: 10px;
    }
    button:hover { background: var(--brand-2); }
    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    .status {
      margin-top: 10px;
      font-size: 0.88rem;
      color: #0f5132;
      white-space: pre-wrap;
    }
    .status.error { color: var(--danger); }
    .mono {
      font-family: Consolas, "Courier New", monospace;
      background: #0f172a;
      color: #e2e8f0;
      border-radius: 8px;
      padding: 10px;
      font-size: 0.82rem;
      overflow: auto;
      max-height: 220px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      margin-top: 8px;
      background: #fff;
    }
    th, td {
      border: 1px solid #e2e8f0;
      padding: 8px;
      text-align: left;
    }
    th { background: #f8fafc; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Personal Finance Expense Tracker</h1>
    <p>Website dashboard for register, login, expense tracking, and monthly report.</p>
    <div class="grid">
      <section class="card">
        <h2>Register</h2>
        <label>Email</label>
        <input id="regEmail" type="email" placeholder="you@email.com" />
        <label>Full Name</label>
        <input id="regName" placeholder="Your name" />
        <label>Password</label>
        <input id="regPass" type="password" placeholder="At least 8 chars" />
        <button onclick="registerUser()">Create Account</button>
        <div id="regStatus" class="status"></div>
      </section>

      <section class="card">
        <h2>Login</h2>
        <label>Email</label>
        <input id="loginEmail" type="email" />
        <label>Password</label>
        <input id="loginPass" type="password" />
        <button onclick="loginUser()">Login</button>
        <div id="loginStatus" class="status"></div>
        <label>JWT Token</label>
        <textarea id="tokenBox" class="mono" style="width:100%; height:120px;" readonly></textarea>
      </section>

      <section class="card">
        <h2>Add Expense</h2>
        <label>Title</label>
        <input id="title" placeholder="Groceries" />
        <div class="row">
          <div>
            <label>Category</label>
            <input id="category" placeholder="Food" />
          </div>
          <div>
            <label>Amount</label>
            <input id="amount" type="number" step="0.01" />
          </div>
        </div>
        <label>Date</label>
        <input id="expenseDate" type="date" />
        <label>Notes</label>
        <input id="notes" placeholder="Optional notes" />
        <button onclick="addExpense()">Save Expense</button>
        <div id="addStatus" class="status"></div>
      </section>

      <section class="card">
        <h2>Reports</h2>
        <div class="row">
          <div>
            <label>Year</label>
            <input id="reportYear" type="number" value="2026" />
          </div>
          <div>
            <label>Month</label>
            <input id="reportMonth" type="number" min="1" max="12" value="2" />
          </div>
        </div>
        <button onclick="loadSummary()">Load Monthly Summary</button>
        <div id="summaryBox" class="mono"></div>
      </section>
    </div>

    <section class="card" style="margin-top:14px;">
      <h2>My Expenses</h2>
      <button onclick="loadExpenses()">Refresh List</button>
      <table id="expenseTable">
        <thead>
          <tr>
            <th>ID</th><th>Title</th><th>Category</th><th>Amount</th><th>Date</th><th>Notes</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </section>
  </div>

  <script>
    const api = "";
    let token = "";

    function showStatus(id, text, error = false) {
      const el = document.getElementById(id);
      el.textContent = text;
      el.className = error ? "status error" : "status";
    }

    async function apiCall(path, options = {}) {
      const headers = options.headers || {};
      headers["Content-Type"] = "application/json";
      if (token) headers["Authorization"] = `Bearer ${token}`;
      const res = await fetch(api + path, { ...options, headers });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.detail || JSON.stringify(data) || "Request failed");
      }
      return data;
    }

    async function registerUser() {
      try {
        const body = {
          email: document.getElementById("regEmail").value,
          full_name: document.getElementById("regName").value,
          password: document.getElementById("regPass").value
        };
        const data = await apiCall("/auth/register", { method: "POST", body: JSON.stringify(body) });
        showStatus("regStatus", "Registered: " + data.email);
      } catch (e) {
        showStatus("regStatus", e.message, true);
      }
    }

    async function loginUser() {
      try {
        const body = {
          email: document.getElementById("loginEmail").value,
          password: document.getElementById("loginPass").value
        };
        const data = await apiCall("/auth/login", { method: "POST", body: JSON.stringify(body) });
        token = data.access_token;
        document.getElementById("tokenBox").value = token;
        showStatus("loginStatus", "Login successful");
      } catch (e) {
        showStatus("loginStatus", e.message, true);
      }
    }

    async function addExpense() {
      try {
        const body = {
          title: document.getElementById("title").value,
          category: document.getElementById("category").value,
          amount: Number(document.getElementById("amount").value),
          expense_date: document.getElementById("expenseDate").value,
          notes: document.getElementById("notes").value
        };
        const data = await apiCall("/expenses/", { method: "POST", body: JSON.stringify(body) });
        showStatus("addStatus", "Saved expense #" + data.id);
        await loadExpenses();
      } catch (e) {
        showStatus("addStatus", e.message, true);
      }
    }

    async function loadExpenses() {
      try {
        const data = await apiCall("/expenses/");
        const tbody = document.querySelector("#expenseTable tbody");
        tbody.innerHTML = "";
        data.items.forEach(item => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>${item.id}</td>
            <td>${item.title}</td>
            <td>${item.category}</td>
            <td>${item.amount}</td>
            <td>${item.expense_date}</td>
            <td>${item.notes || ""}</td>
          `;
          tbody.appendChild(tr);
        });
      } catch (e) {
        alert("Load expenses failed: " + e.message);
      }
    }

    async function loadSummary() {
      try {
        const year = document.getElementById("reportYear").value;
        const month = document.getElementById("reportMonth").value;
        const data = await apiCall(`/reports/monthly-summary?year=${year}&month=${month}`);
        document.getElementById("summaryBox").textContent = JSON.stringify(data, null, 2);
      } catch (e) {
        document.getElementById("summaryBox").textContent = e.message;
      }
    }
  </script>
</body>
</html>
"""
