const API = "http://127.0.0.1:8000";

function getToken() { return localStorage.getItem("token"); }
function showMsg(msg, color="green") {
    const el = document.getElementById("message");
    el.style.color = color;
    el.textContent = msg;
    setTimeout(() => el.textContent = "", 3000);
}

function showLogin() {
    document.getElementById("register-form").classList.add("hidden");
    document.getElementById("login-form").classList.remove("hidden");
}

function showRegister() {
    document.getElementById("login-form").classList.add("hidden");
    document.getElementById("register-form").classList.remove("hidden");
}

// ── Auth ──────────────────────────────────────────
async function register() {
    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    const res = await fetch(`${API}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
    });
    const data = await res.json();
    if (res.ok) { showMsg("Registered! Please login."); showLogin(); }
    else showMsg(data.detail, "red");
}

async function login() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
        localStorage.setItem("token", data.access_token);
        document.getElementById("auth-section").classList.add("hidden");
        document.getElementById("task-section").classList.remove("hidden");
        fetchTasks();
    } else showMsg(data.detail, "red");
}

function logout() {
    localStorage.removeItem("token");
    document.getElementById("auth-section").classList.remove("hidden");
    document.getElementById("task-section").classList.add("hidden");
}

// ── Tasks ─────────────────────────────────────────
async function fetchTasks(completed = null) {
    let url = `${API}/tasks/`;
    if (completed !== null) url += `?completed=${completed}`;

    const res = await fetch(url, {
        headers: { "Authorization": `Bearer ${getToken()}` }
    });
    const data = await res.json();
    renderTasks(data.tasks);
}

function renderTasks(tasks) {
    const list = document.getElementById("task-list");
    list.innerHTML = "";
    if (!tasks || tasks.length === 0) {
        list.innerHTML = `<p style="text-align:center;color:#888;">No tasks found!</p>`;
        return;
    }
    tasks.forEach(task => {
        list.innerHTML += `
        <div class="task-card ${task.completed ? 'done' : 'pending'}">
            <div class="task-info">
                <h3>${task.title}</h3>
                <p>${task.description || "No description"}</p>
                <p>${task.completed ? "✅ Completed" : "⏳ Pending"}</p>
            </div>
            <div class="task-actions">
                ${!task.completed ? `<button class="complete-btn" onclick="completeTask(${task.id})">Complete</button>` : ""}
                <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        </div>`;
    });
}

async function createTask() {
    const title = document.getElementById("task-title").value;
    const description = document.getElementById("task-desc").value;

    if (!title) { showMsg("Title is required!", "red"); return; }

    const res = await fetch(`${API}/tasks/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ title, description })
    });
    if (res.ok) {
        document.getElementById("task-title").value = "";
        document.getElementById("task-desc").value = "";
        showMsg("Task created!");
        fetchTasks();
    } else showMsg("Failed to create task", "red");
}

async function completeTask(id) {
    const res = await fetch(`${API}/tasks/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ completed: true })
    });
    if (res.ok) { showMsg("Task completed! ✅"); fetchTasks(); }
}

async function deleteTask(id) {
    const res = await fetch(`${API}/tasks/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${getToken()}` }
    });
    if (res.ok) { showMsg("Task deleted!"); fetchTasks(); }
}