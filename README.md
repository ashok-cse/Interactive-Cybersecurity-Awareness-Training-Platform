# CyberAware Training Platform

An interactive, role-based cybersecurity awareness training platform built with Flask.
Employees complete structured training modules, take auto-graded quizzes, and practise
identifying phishing emails in a safe simulated inbox. Trainers and admins manage content,
campaigns, and analytics.

---

## Features

- **Training Modules** – 21 modules covering the most common attack types
  (phishing, ransomware, malware, DDoS, MitM, supply-chain, zero-day, credential
  theft, cloud misconfig, BEC, living-off-the-land, AI/deepfakes, SQLi, IoT,
  insider threats, plus secure coding and threat modeling), each with structured
  content and an interactive in-page exercise.
- **Auto-graded Quizzes** – 30 questions per module (630 total); score =
  round(correct/total × 100); pass threshold 70 %, with retakes.
- **Simulated Phishing Inbox** – employees identify phishing vs. legitimate emails.
- **Role-based Dashboards** – tailored views for Employee, Trainer, and Admin.
- **Analytics** – completion rates, average scores, pass/fail charts (Chart.js).
- **CSV Reports** – downloadable user-progress, quiz-scores, and phishing reports.
- **Activity Logging** – every significant action is recorded with timestamp and IP.
- **Security-first design** – CSRF protection, password hashing, rate limiting, CSP headers.

---

## Tech Stack

| Layer        | Technology                                   |
|--------------|----------------------------------------------|
| Web framework | Flask 3.x (Python 3.11)                     |
| ORM          | Flask-SQLAlchemy 3.x + SQLite (dev/prod)     |
| Auth         | Flask-Login                                  |
| Forms / CSRF | Flask-WTF + WTForms                          |
| Rate limiting| Flask-Limiter                                |
| Passwords    | Werkzeug `generate_password_hash` (pbkdf2:sha256) |
| Charts       | Chart.js (CDN)                               |
| WSGI server  | Gunicorn (production / Docker)               |
| Testing      | Pytest 8                                     |

---

## Project Structure

```
Interactive-Cybersecurity-Awareness-Training-Platform/
├── app/
│   ├── __init__.py          # create_app() factory, blueprint registration
│   ├── config.py            # Config / DevelopmentConfig / ProductionConfig / TestingConfig
│   ├── extensions.py        # db, login_manager, csrf, limiter singletons
│   ├── models.py            # SQLAlchemy models
│   ├── forms.py             # WTForms form classes
│   ├── security.py          # roles_required, admin_required, staff_required, log_activity
│   ├── utils.py             # shared helpers (naive-UTC utcnow)
│   ├── routes/
│   │   ├── auth.py          # Blueprint 'auth'      – /register /login /logout /profile
│   │   ├── dashboard.py     # Blueprint 'dashboard' – / /dashboard
│   │   ├── training.py      # Blueprint 'training'  – /training/…
│   │   ├── phishing.py      # Blueprint 'phishing'  – /phishing/…
│   │   ├── admin.py         # Blueprint 'admin'     – /admin/…
│   │   └── reports.py       # Blueprint 'reports'   – /reports/…
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS + JS assets
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py
│   ├── test_quiz.py
│   ├── test_security.py
│   ├── test_admin.py
│   └── test_seed.py         # seed-data integrity (counts, demo accounts)
├── seed_data/               # Externalised quiz/module content
│   ├── attacks_a.py         # attack modules 7–11  (MODULES list)
│   ├── attacks_b.py         # attack modules 12–16
│   ├── attacks_c.py         # attack modules 17–21
│   └── existing_extra.py    # extra question banks for the 6 base modules
├── run.py                   # Development entry-point
├── db_init.py               # One-off DB initialisation script
├── seed.py                  # Demo data seeder (also `flask seed` CLI)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
└── .env.example
```

---

## Local Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd Interactive-Cybersecurity-Awareness-Training-Platform
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env: at minimum set SECRET_KEY to a strong random value
```

### 3. Initialise the database

```bash
python db_init.py
```

### 4. (Optional) Seed demo data

```bash
python seed.py
# or via the Flask CLI:
flask seed
```

### 5. Run the development server

```bash
python run.py
# or:
flask run
```

Visit http://localhost:5000

---

## Environment Variables

| Variable                  | Default                                | Description                                      |
|---------------------------|----------------------------------------|--------------------------------------------------|
| `FLASK_ENV`               | `production`                           | `development`, `production`, or `testing`        |
| `SECRET_KEY`              | `dev-secret-change-me`                 | Flask session signing key – **change in prod**   |
| `DATABASE_URL`            | `sqlite:///instance/cyberaware.db`     | SQLAlchemy DB URI (SQLite path or PostgreSQL DSN)|
| `SESSION_COOKIE_SECURE`   | `false`                                | Set `true` when serving over HTTPS               |
| `SESSION_TIMEOUT_MINUTES` | `30`                                   | Idle session timeout in minutes                  |
| `SEED_ON_START`           | `true`                                 | Auto-seed demo data on container startup         |
| `PORT`                    | `5000`                                 | TCP port Gunicorn listens on                     |
| `GUNICORN_WORKERS`        | `2`                                    | Number of Gunicorn worker processes              |
| `GUNICORN_TIMEOUT`        | `120`                                  | Gunicorn worker timeout in seconds               |

---

## How to Run Tests

```bash
# Activate the virtual environment first
source .venv/bin/activate

# Run all tests
pytest

# Verbose output
pytest -v

# Run a single test file
pytest tests/test_auth.py -v

# Run a specific test
pytest tests/test_security.py::TestSecurityHeaders::test_x_frame_options_deny -v
```

Tests use an in-memory SQLite database (`TestingConfig`). CSRF is disabled in tests
so forms can be posted directly. Rate limiting is also disabled.

---

## Demo Accounts

Seeded by `seed.py` (or `SEED_ON_START=true`):

| Role     | Email                         | Password        |
|----------|-------------------------------|-----------------|
| Admin    | admin@cyberaware.local        | Admin@12345     |
| Trainer  | trainer@cyberaware.local      | Trainer@12345   |
| Employee | employee@cyberaware.local     | Employee@12345  |
| Employee | employee2@cyberaware.local    | Employee@12345  |
| Employee | employee3@cyberaware.local    | Employee@12345  |

---

## Docker Run

### Quick start

```bash
# Copy and edit environment file
cp .env.example .env

# Build and start
docker compose up --build

# Run in the background
docker compose up --build -d
```

The app is available at http://localhost:5000.

Demo data is seeded automatically because `.env.example` sets `SEED_ON_START=true`.

### Manual seed (after first boot)

```bash
docker compose exec web flask seed
```

### Stop

```bash
docker compose down
```

To remove the persistent volume as well:

```bash
docker compose down -v
```

---

## EasyPanel Deployment

EasyPanel is a Docker-based self-hosted PaaS. Follow these steps to deploy CyberAware:

### 1. Create a new App

In the EasyPanel dashboard, click **+ New Service → App**.

Choose one of:
- **Git source** – point to this repository and use the `Dockerfile` (EasyPanel
  will build automatically on push).
- **Docker Compose** – upload/paste `docker-compose.yml`.

### 2. Set Environment Variables

In the app's **Environment** tab, add the following variables (copied from
`.env.example` and adjusted for production):

| Variable                  | Recommended Production Value                               |
|---------------------------|------------------------------------------------------------|
| `FLASK_ENV`               | `production`                                               |
| `SECRET_KEY`              | A long random string (generate with `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DATABASE_URL`            | `sqlite:////data/cyberaware.db`                            |
| `SESSION_COOKIE_SECURE`   | `true` (EasyPanel terminates TLS)                          |
| `SESSION_TIMEOUT_MINUTES` | `30`                                                       |
| `SEED_ON_START`           | `true` (for the very first deployment; set `false` after)  |
| `PORT`                    | `5000`                                                     |

### 3. Mount a Persistent Volume

In the **Volumes** tab, add a named volume:

```
Mount path (container): /data
```

This ensures the SQLite database survives container restarts and redeployments.

### 4. Configure the Internal Port

In the **Ports** tab (or Network settings), set the container internal port to **5000**.
EasyPanel will handle the reverse-proxy and TLS termination on its configured domain.

### 5. Deploy

Click **Deploy**. EasyPanel will:
1. Build the Docker image from the `Dockerfile`.
2. Start the container, which runs `docker-entrypoint.sh`:
   - Initialises the database (`python db_init.py`).
   - Seeds demo data if `SEED_ON_START=true`.
   - Starts Gunicorn on port 5000.

### 6. Access the App

Navigate to the domain configured in EasyPanel. Log in with one of the demo accounts
listed above.

### 7. Post-deployment

- After the first successful deployment, set `SEED_ON_START=false` to prevent
  re-seeding on every restart.
- For a one-off manual seed: use EasyPanel's **Console** tab to run
  `flask seed` inside the container.
- Monitor logs in EasyPanel's **Logs** tab.

---

## Contributing

1. Fork the repository and create a feature branch.
2. Install dependencies and run tests locally.
3. Open a pull request against `main`.

Please do not commit `.env` or any file containing secrets.
