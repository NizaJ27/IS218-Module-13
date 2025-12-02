# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

## Running Tests Locally

Install dependencies and run pytest:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q
```

To run only integration tests:

```bash
pytest tests/integration/ -v
```

To run tests with coverage:

```bash
pytest --cov=app --cov-report=html
```

## Testing with OpenAPI Documentation

Start the FastAPI server locally:

```bash
python main.py
```

Access the interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Manual Testing Steps

1. **Register a User** (POST `/users/register`)
   - Endpoint: `/users/register`
   - Body: `{"username": "testuser", "email": "test@example.com", "password": "password123"}`
   - Expected: 200 OK with user data (without password)

2. **Login** (POST `/users/login`)
   - Endpoint: `/users/login`
   - Body: `{"username": "testuser", "password": "password123"}`
   - Expected: 200 OK with user data

3. **Create Calculation** (POST `/calculations`)
   - Endpoint: `/calculations`
   - Body: `{"a": 10, "b": 5, "type": "Add"}`
   - Expected: 200 OK with calculation result

4. **Browse Calculations** (GET `/calculations`)
   - Endpoint: `/calculations`
   - Expected: 200 OK with list of calculations

5. **Read Specific Calculation** (GET `/calculations/{id}`)
   - Endpoint: `/calculations/1`
   - Expected: 200 OK with calculation details

6. **Update Calculation** (PUT `/calculations/{id}`)
   - Endpoint: `/calculations/1`
   - Body: `{"a": 20, "b": 10, "type": "Multiply"}`
   - Expected: 200 OK with updated calculation

7. **Delete Calculation** (DELETE `/calculations/{id}`)
   - Endpoint: `/calculations/1`
   - Expected: 200 OK with deletion confirmation

## CI / Docker Hub

- The repository includes a GitHub Actions workflow at `.github/workflows/ci.yml` that runs tests against a Postgres service and (on success) builds and pushes a Docker image to Docker Hub.
- Docker Hub repository (replace with your repo): `docker.io/<your-username>/is218-module-12`

## Module 12 — User & Calculation CRUD with Integration Tests

This module completes the back-end logic with full CRUD operations for users and calculations.

### Features Implemented

- **User Endpoints**:
  - POST `/users/register` - Register new users with email validation and password hashing
  - POST `/users/login` - Authenticate users with username/password

- **Calculation Endpoints (BREAD)**:
  - POST `/calculations` - Add new calculations
  - GET `/calculations` - Browse all calculations with pagination
  - GET `/calculations/{id}` - Read specific calculation
  - PUT `/calculations/{id}` - Edit existing calculation
  - DELETE `/calculations/{id}` - Delete calculation

### Running with Docker

Pull and run the latest image from Docker Hub:

```bash
docker pull <your-dockerhub-username>/is218-module-12:latest
docker run -p 8000:8000 <your-dockerhub-username>/is218-module-12:latest
```

### Docker Hub Link

**Docker Hub Repository**: [https://hub.docker.com/r/<your-dockerhub-username>/is218-module-12](https://hub.docker.com/r/<your-dockerhub-username>/is218-module-12)

*Note: Replace `<your-dockerhub-username>` with your actual Docker Hub username.*

---

**Docker Hub**: Replace with your published image, e.g. `docker.io/<your-username>/is218-module-12`.

## Module 9 — PostgreSQL & pgAdmin (FastAPI + Postgres)

Follow these steps to satisfy the Module 9 assignment requirements.

- **Start services:** Run the Docker Compose configuration that includes FastAPI (web), PostgreSQL (db), and pgAdmin (optional) from the project root:

```bash
docker-compose up --build
```

- **Access pgAdmin:** Open `http://localhost:5050` in your browser. Use the credentials defined in the Compose file (if present). If your compose file exposes pgAdmin on a different port, use that port instead.

- **Connect to the database:** In pgAdmin create/connect to a server using:
   - Host: `db` (or `localhost` if using port forwarding)
   - User: `postgres` (or the user defined in `docker-compose.yml`)
   - Database: the database defined in Compose (commonly `fastapi_db`)

- **SQL files:** The repository includes SQL scripts you can run in pgAdmin Query Tool or via `psql`:
   - `sql/create_tables.sql` — create `users` and `calculations` tables
   - `sql/insert_data.sql` — insert sample rows
   - `sql/queries.sql` — run SELECT and JOIN queries
   - `sql/update_delete.sql` — examples of UPDATE and DELETE statements

- **Execution tips:**
   - In pgAdmin open the Query Tool, paste the contents of a script, and click the run button.
   - After each run, take a screenshot of the Query Tool results showing the "Query returned successfully" message (or rows displayed).

- **Documentation / Submission:** Create a Word document or PDF compiling the screenshots. For each screenshot include a short caption (one sentence) describing what the screenshot shows (e.g., "Created tables: users and calculations — 2 rows affected"). Include a short reflection (1–2 paragraphs) about challenges and what you learned.

If you want to run the SQL scripts directly from the host using `psql` and Docker, you can (alternative to pgAdmin):

```bash
# Run the create script inside the running postgres container (replace container name if different)
docker exec -i $(docker ps -qf "name=db") psql -U postgres -d postgres < sql/create_tables.sql
```

Replace `postgres` with the target database name if different.
