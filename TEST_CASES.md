# Test Cases – CyberAware Training Platform

This document captures the full test plan for the CyberAware platform,
covering both static (non-execution) analysis and dynamic (runtime) testing.

---

## Section 1 – Static Testing

Static tests are performed by reading code and configuration without executing
the application. They verify structural correctness, adherence to the build
contract, and security properties at the source-code level.

| Test Case ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| ST-01 | Model field names match contract | Review `app/models.py`; compare every field name against the build contract | All field names (e.g. `password_hash`, `correct_answer`, `is_phishing`, `responded_at`) match exactly | — | Pending |
| ST-02 | Password hashing scheme | Inspect `User.set_password()` in `app/models.py` | `generate_password_hash(password, method='pbkdf2:sha256')` is used; no plaintext storage | — | Pending |
| ST-03 | CSRF protection on all POST routes | Review `app/routes/*.py`; verify every blueprint registers under `csrf` and that plain POST forms include `csrf_token()` | All state-changing routes are protected; no `@csrf.exempt` without justification | — | Pending |
| ST-04 | No raw SQL interpolation | `grep -rn "execute\|text(" app/routes/` | No user-controlled strings are concatenated into SQL; all queries use ORM or explicit `db.text()` with bound params | — | Pending |
| ST-05 | `|safe` filter not used on user data | `grep -rn "|safe" app/templates/` | Only `module.content` (trusted author HTML) uses `|safe`; no user-supplied fields use `|safe` | — | Pending |
| ST-06 | Security headers in after_request | Inspect `app/__init__.py` `after_request` hook | All four headers present: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Content-Security-Policy` | — | Pending |
| ST-07 | Role decorators on admin routes | Review `app/routes/admin.py` and `reports.py` | Every route uses `@admin_required` or `@staff_required`; no unprotected state-changing endpoint | — | Pending |
| ST-08 | TestingConfig correctness | Inspect `app/config.py` `TestingConfig` | `WTF_CSRF_ENABLED=False`, `SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'`, `RATELIMIT_ENABLED=False`, `TESTING=True` | — | Pending |
| ST-09 | Blueprint and endpoint names match contract | Check all `Blueprint(name, ...)` declarations and route function names | Endpoint names match contract exactly (e.g. `auth.login`, `dashboard.home`, `reports.user_progress_csv`) | — | Pending |
| ST-10 | Quiz grading formula | Inspect quiz POST handler in `app/routes/training.py` | `score = round(correct / total * 100)`; `passed = score >= app.config['PASS_THRESHOLD']` (70) | — | Pending |
| ST-11 | Phishing grading rule | Inspect phishing respond handler in `app/routes/phishing.py` | `is_correct = (user_response == campaign.correct_response)` where `correct_response = 'phishing' if campaign.is_phishing else 'legitimate'` | — | Pending |
| ST-12 | Session timeout configuration | Inspect `before_request` hook in `app/__init__.py` | `session['last_active']` is updated each request; stale sessions are cleared and user is redirected | — | Pending |
| ST-13 | Secret key not hard-coded in production config | Review `app/config.py` and `.env.example` | `SECRET_KEY` is loaded from environment variable; `.env.example` uses a placeholder, not a real secret | — | Pending |
| ST-14 | Demo accounts not seeded with weak passwords | Review `seed.py` | Demo passwords meet minimum 8 characters and contain mixed case + digits (e.g. `Admin@12345`) | — | Pending |
| ST-15 | Dockerfile does not expose secrets | Review `Dockerfile` | No hard-coded secrets; env vars loaded via `env_file` in `docker-compose.yml` | — | Pending |
| ST-16 | `.gitignore` excludes `.env` and `*.db` | Read `.gitignore` | `.env`, `instance/`, and `*.db` are listed | — | Pending |
| ST-17 | Activity log records login events | Inspect auth route POST handler | `log_activity('login_success', user)` and `log_activity('login_failed', ...)` are called appropriately | — | Pending |
| ST-18 | Rate limit applied to login | Inspect `app/routes/auth.py` login view | `@limiter.limit("5 per minute")` decorates the POST handler or the function is decorated with appropriate limiter | — | Pending |

---

## Section 2 – Dynamic Testing

Dynamic tests execute the application (pytest automated tests and manual UI tests)
and verify runtime behaviour.

### 2a – Automated Pytest Tests

| Test Case ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| DT-AUTH-01 | Registration creates a User record | `POST /register` with valid name, email, department, password, confirm_password | HTTP 200 or 302; `User.query.filter_by(email=...).first()` is not None | — | Pending |
| DT-AUTH-02 | Registration defaults role to 'employee' | `POST /register`, then query DB | `user.role == 'employee'` | — | Pending |
| DT-AUTH-03 | Login with valid credentials redirects to dashboard | `POST /login` with correct email + password | HTTP 302; `Location` header contains `/dashboard` | — | Pending |
| DT-AUTH-04 | Login with wrong password does not authenticate | `POST /login` with correct email + wrong password | HTTP 200 or redirect to `/login`; no redirect to `/dashboard` | — | Pending |
| DT-AUTH-05 | Login with unknown email does not authenticate | `POST /login` with non-existent email | No redirect to `/dashboard`; no server error | — | Pending |
| DT-AUTH-06 | Login with empty credentials does not crash | `POST /login` with empty strings | HTTP 200 or 400; no HTTP 500 | — | Pending |
| DT-AUTH-07 | Password stored as pbkdf2:sha256 hash | Create user, inspect `user.password_hash` | Hash starts with `pbkdf2:sha256`; value != raw password | — | Pending |
| DT-AUTH-08 | check_password correct password | Create user; call `user.check_password(correct_pw)` | Returns `True` | — | Pending |
| DT-AUTH-09 | check_password wrong password | Create user; call `user.check_password(wrong_pw)` | Returns `False` | — | Pending |
| DT-AUTH-10 | Logout clears session | Login; `POST /logout`; `GET /dashboard` | Dashboard redirects to `/login` (302 or 401) | — | Pending |
| DT-SEC-01 | Employee denied access to /admin/users | Login as employee; `GET /admin/users` | HTTP 403 or redirect | — | Pending |
| DT-SEC-02 | Employee denied access to /admin/analytics | Login as employee; `GET /admin/analytics` | HTTP 403 or redirect | — | Pending |
| DT-SEC-03 | Employee denied access to CSV reports | Login as employee; `GET /reports/user-progress.csv` | HTTP 403 or redirect | — | Pending |
| DT-SEC-04 | Anonymous redirected from /dashboard | `GET /dashboard` without login | HTTP 302 to `/login` | — | Pending |
| DT-SEC-05 | Anonymous redirected from /profile | `GET /profile` without login | HTTP 302 or 401 | — | Pending |
| DT-SEC-06 | Anonymous redirected from /training/ | `GET /training/` without login | HTTP 302 or 401 | — | Pending |
| DT-SEC-07 | SQL injection in login email – no 500 | `POST /login` with `' OR '1'='1` as email | HTTP 200; no server error | — | Pending |
| DT-SEC-08 | SQL injection – no auth bypass | `POST /login` with injection payload | No redirect to `/dashboard` | — | Pending |
| DT-SEC-09 | SQL injection – DROP TABLE payload | `POST /login` with `'; DROP TABLE user;--` | HTTP 200; no error; DB intact | — | Pending |
| DT-SEC-10 | XSS payload in registration name escaped | `POST /register` with `<script>alert('xss')</script>` as name | Response body does not contain raw `<script>alert('xss')</script>` | — | Pending |
| DT-SEC-11 | XSS payload escaped on profile page | Create user with `<script>` name; login; `GET /profile` | Response body does not contain raw `<script>alert('xss')</script>` | — | Pending |
| DT-SEC-12 | X-Frame-Options header present | `GET /` | `X-Frame-Options: DENY` header present | — | Pending |
| DT-SEC-13 | X-Content-Type-Options header present | `GET /` | `X-Content-Type-Options: nosniff` header present | — | Pending |
| DT-SEC-14 | Content-Security-Policy header present | `GET /` | `Content-Security-Policy` header present | — | Pending |
| DT-SEC-15 | Security headers on authenticated route | Login; `GET /dashboard` | Both `X-Frame-Options` and `X-Content-Type-Options` present | — | Pending |
| DT-QUIZ-01 | All correct answers → score 100, passed=True | Login; submit quiz with all 'A' answers (all correct) | `QuizAttempt.score == 100`, `passed == True` | — | Pending |
| DT-QUIZ-02 | All wrong answers → score 0, passed=False | Login; submit quiz with all 'B' answers | `QuizAttempt.score == 0`, `passed == False` | — | Pending |
| DT-QUIZ-03 | 4/5 correct → score 80, passed=True | Login; submit 4 correct + 1 wrong | `score == 80`, `passed == True` (>= 70) | — | Pending |
| DT-QUIZ-04 | 2/5 correct → score 40, passed=False | Login; submit 2 correct + 3 wrong | `score == 40`, `passed == False` (< 70) | — | Pending |
| DT-QUIZ-05 | QuizAttempt persisted after submission | Login; submit quiz; query DB | One new `QuizAttempt` row exists | — | Pending |
| DT-QUIZ-06 | Multiple attempts all persisted | Login; submit quiz 3 times; query DB | Three `QuizAttempt` rows exist | — | Pending |
| DT-QUIZ-07 | Pass → UserProgress.status='completed' | Login; submit all-correct quiz | `UserProgress.status == 'completed'`, `completion_percentage == 100`, `completed_at` not None | — | Pending |
| DT-QUIZ-08 | Fail → UserProgress not 'completed' | Login; submit all-wrong quiz | `UserProgress.status != 'completed'` (or no record); `completed_at == None` | — | Pending |
| DT-ADM-01 | Admin can list users | Login as admin; `GET /admin/users` | HTTP 200 | — | Pending |
| DT-ADM-02 | Trainer denied /admin/users | Login as trainer; `GET /admin/users` | HTTP 403 or redirect | — | Pending |
| DT-ADM-03 | Trainer can access analytics | Login as trainer; `GET /admin/analytics` | HTTP 200 | — | Pending |
| DT-ADM-04 | Admin can access analytics | Login as admin; `GET /admin/analytics` | HTTP 200 | — | Pending |
| DT-ADM-05 | Phishing response 'phishing' → is_correct=True | Create assignment (is_phishing=True); login as employee; `POST /phishing/email/<id>/respond` with `response=phishing` | `is_correct == True`, `responded_at` set | — | Pending |
| DT-ADM-06 | Phishing response 'legitimate' → is_correct=False | Same campaign; respond with `response=legitimate` | `is_correct == False` | — | Pending |
| DT-ADM-07 | Legitimate email: correct response → is_correct=True | Campaign with `is_phishing=False`; respond 'legitimate' | `is_correct == True` | — | Pending |
| DT-ADM-08 | User-progress CSV returns 200 + text/csv | Login as admin; `GET /reports/user-progress.csv` | HTTP 200; `Content-Type` contains `text/csv` | — | Pending |
| DT-ADM-09 | Quiz-scores CSV returns 200 + text/csv | Login as admin; `GET /reports/quiz-scores.csv` | HTTP 200; `Content-Type` contains `text/csv` | — | Pending |
| DT-ADM-10 | Phishing CSV returns 200 + text/csv | Login as admin; `GET /reports/phishing.csv` | HTTP 200; `Content-Type` contains `text/csv` | — | Pending |
| DT-ADM-11 | Employee denied CSV reports | Login as employee; `GET /reports/user-progress.csv` | HTTP 403 or redirect | — | Pending |

### 2b – Manual UI Tests

| Test Case ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| DT-UI-01 | End-to-end registration flow | Open `/register`; fill form with valid data; submit | User is created and redirected to login; flash success message displayed | — | Pending |
| DT-UI-02 | Registration with mismatched passwords | Open `/register`; enter different values in password/confirm; submit | Form re-renders with validation error; no user created | — | Pending |
| DT-UI-03 | Login and employee dashboard | Login as `employee@cyberaware.local`; verify dashboard | Dashboard shows modules, pending phishing assignments, and progress stats | — | Pending |
| DT-UI-04 | Trainer dashboard stat cards | Login as `trainer@cyberaware.local` | Dashboard shows total_users, completion_rate, avg_score, total_campaigns | — | Pending |
| DT-UI-05 | Admin dashboard activity log | Login as `admin@cyberaware.local` | Dashboard shows recent ActivityLog entries | — | Pending |
| DT-UI-06 | Take a training module quiz | Login as employee; navigate to a module; click Start; take the quiz | Quiz form renders with questions; after submit, result page shows score and pass/fail | — | Pending |
| DT-UI-07 | Phishing inbox and response | Login as employee; open phishing inbox; click an email; select phishing or legitimate | Result page shows whether response was correct; red flags listed | — | Pending |
| DT-UI-08 | Admin creates phishing campaign | Login as trainer; navigate to Campaigns; fill CampaignForm; submit | Campaign appears in list; can be assigned to users | — | Pending |
| DT-UI-09 | Download CSV report | Login as admin; open Reports page; click user-progress CSV link | File download starts; CSV contains header row and data rows | — | Pending |
| DT-UI-10 | Analytics charts render | Login as admin; open Analytics page | All four Chart.js canvases (completionChart, avgScoreChart, passFailChart, phishingChart) render | — | Pending |
| DT-UI-11 | Logout via UI | Login as employee; click Logout in sidebar | Session is cleared; browser redirected to login page | — | Pending |
| DT-UI-12 | Session idle timeout | Login; wait longer than `SESSION_TIMEOUT_MINUTES`; attempt any action | User is redirected to login with session-expired message | — | Pending |
| DT-UI-13 | 404 error page | Navigate to `/this-does-not-exist` | Custom 404 error page rendered (not Flask default) | — | Pending |
| DT-UI-14 | 403 error page | Login as employee; navigate to `/admin/users` | Custom 403 error page rendered | — | Pending |
| DT-UI-15 | Responsive layout on mobile | Open app on 375 px wide viewport | Sidebar collapses; content remains readable; buttons are tappable | — | Pending |

---

*Actual Result* and *Status* columns are filled in during test execution.
Acceptable status values: **Pass**, **Fail**, **Blocked**, **Not Run**.
