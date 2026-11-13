# ⚡ AutoFlow — Personal Automation Studio

**AutoFlow** is a Python-powered personal automation web application built with Flask. It helps users manage workflows, organize files automatically, schedule repetitive tasks, and track automation activity through a clean, modern dashboard.

This is the **Version 1 (V1)** release of AutoFlow.

---

## ✨ Features

### 📊 Interactive Dashboard
- Modern dark-themed interface.
- Overview of total workflows and automation runs.
- Files organized statistics.
- Recent workflow activity.
- Quick navigation to important features.

### ⚙️ Workflow Management
- Create and save custom workflows.
- Choose workflow categories:
  - File Management
  - Productivity
  - Other
- Store workflow information in an SQLite database.
- Execute supported workflows.

### 📁 Smart File Organizer
- Automatically organizes files into categorized folders.
- Supports multiple file types:
  - Images
  - Documents
  - Videos
  - Audio
  - Archives
  - Code
  - Others
- Preview files before organizing.
- Handles filename conflicts to avoid overwriting existing files.

### ⏰ Automation Scheduler
- Schedule workflows to run automatically.
- Supports three scheduling options:
  - Once
  - Daily
  - Weekly
- Powered by APScheduler.
- Automatically deactivates completed one-time schedules.
- Uses the Asia/Kolkata timezone.

### 📜 Automation History
- Tracks workflow execution activity.
- Records file organization operations.
- Displays automation details and timestamps.
- Keeps track of files moved.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| HTML | Page structure |
| CSS | Styling and responsive design |
| JavaScript | Frontend interactions |
| SQLite | Database and persistent storage |
| APScheduler | Task scheduling |

---

## 📂 Project Structure

```text
AutoFlow/
│
├── app.py
├── storage.py
├── organizer.py
├── engine.py
├── scheduler_engine.py
├── requirements.txt
│
├── database/
│   └── autoflow.db
│
├── templates/
│   ├── index.html
│   ├── workflows.html
│   ├── organizer.html
│   ├── history.html
│   └── scheduler.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── images/
│
└── .venv/
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd AutoFlow
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open AutoFlow

Visit the following address in your browser:

```text
http://127.0.0.1:5000/
```

---

## 🧠 What I Learned

Building AutoFlow helped me gain practical experience with:

- Developing web applications using Flask.
- Connecting Python applications with SQLite.
- Creating reusable Python modules.
- Working with file systems and directory operations.
- Implementing task scheduling using APScheduler.
- Building dynamic HTML templates with Jinja.
- Connecting frontend forms with backend routes.
- Designing responsive web interfaces.
- Debugging and integrating multiple application components.

---

## 🔮 Future Improvements

Planned features for future versions:

- Edit and delete existing workflows.
- Advanced file organization filters.
- Custom application settings.
- Workflow search and filtering.
- Dashboard analytics and visual reports.
- Support for additional automation types.

---

## 📌 Project Status

**AutoFlow V1 — Completed**

The first version includes the core dashboard, workflow system, file organizer, automation engine, scheduler, and history tracking.

Future improvements will be introduced in upcoming versions.

---

## 👨‍💻 Author

**Rahul Bishnoi**

GitHub: [@rbtechniques](https://github.com/rbtechniques)

---

*Built with Python, Flask, and a passion for automation.* ⚡
