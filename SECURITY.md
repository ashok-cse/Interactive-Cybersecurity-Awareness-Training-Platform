# Security Architecture – CyberAware Training Platform

This document describes the security controls implemented in the CyberAware platform
and the rationale behind each decision.

---

## 1. Authentication Security

- **Login endpoint** (`POST /login`) is rate-limited to **5 requests per minute** per IP
  address using Flask-Limiter. Excess requests receive HTTP 429.
- **login_manager.login_view** is set to `'auth.login'`; any protected route accessed by
  an unauthenticated user triggers an automatic redirect to `/login`.
- **Session persistence** is enabled (`session.permanent = True`) so that the
  `PERMANENT_SESSION_LIFETIME` (default 30 minutes) is enforced; the idle timeout is
  tracked via `session['last_active']` in a `before_request` hook.
- **Login success and failure events** are recorded in `ActivityLog` with a timestamp
  and the client IP address, supporting incident investigation.

---

## 2. Password Hashing

Passwords are **never stored in plaintext**.

The `User.set_password()` method calls Werkzeug's `generate_password_hash()` with the
`pbkdf2:sha256` scheme:

```python
self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
```

PBKDF2-HMAC-SHA256 is an adaptive, key-stretching algorithm that:
- Produces a salted hash (the salt is embedded in the output string).
- Resists offline brute-force and rainbow-table attacks.
- Complies with NIST SP 800-63B guidelines for memorised secrets.

`User.check_password()` uses Werkzeug's `check_password_hash()`, which extracts the
embedded salt and algorithm from the stored hash before comparing.

---

## 3. CSRF Protection

All state-changing routes use HTTP POST, and every POST form is protected by
Flask-WTF's CSRF middleware (`CSRFProtect`):

- **WTForms forms** embed a hidden token via `{{ form.hidden_tag() }}`.
- **Plain HTML POST forms** (logout, quiz submit, phishing respond, start module,
  campaign assign) include the token via `{{ csrf_token() }}`:

  ```html
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  ```

- CSRF is **disabled only in `TestingConfig`** (`WTF_CSRF_ENABLED = False`) to allow
  automated pytest requests without a browser session.
- Cross-site request forgery attempts from other origins are rejected with HTTP 400.

---

## 4. SQL Injection Prevention

The platform uses **SQLAlchemy ORM exclusively**. No raw SQL strings are assembled by
concatenating user input. All queries use parameterised expressions:

```python
# Safe – parameterised binding
user = User.query.filter_by(email=email).first()
```

SQLAlchemy escapes all bound parameters before sending them to the database driver,
making SQL injection structurally impossible in the data layer.

---

## 5. XSS Prevention

### Jinja2 Autoescaping

Jinja2 autoescaping is enabled by default for all `.html` templates. Every template
variable is HTML-escaped unless explicitly marked safe:

```html
{{ user.name }}       {# rendered as &lt;script&gt;… — safe #}
{{ module.content|safe }}  {# only for trusted author-written HTML #}
```

User-supplied fields (`name`, `email`, `department`, quiz answers, phishing responses)
are **never rendered with `|safe`**.

### Content Security Policy (CSP)

An `after_request` hook adds the following CSP header to every response:

```
Content-Security-Policy: default-src 'self';
  script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline';
  style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
  img-src 'self' data:;
```

This prevents injection of scripts from untrusted origins even if a template
accidentally rendered unescaped data.

---

## 6. Rate Limiting

Flask-Limiter is configured with `get_remote_address` as the key function.

- **Login endpoint**: `5 per minute` – mitigates credential-stuffing attacks.
- **Global default limits**: empty (`default_limits=[]`) so only explicitly decorated
  routes are limited, avoiding false positives on content pages.
- Rate limiting is **disabled in `TestingConfig`** (`RATELIMIT_ENABLED = False`) to
  prevent test interference.

---

## 7. Secure Session Handling

Flask session cookies are configured with the following security attributes:

| Attribute                    | Value                    | Effect                                              |
|------------------------------|--------------------------|-----------------------------------------------------|
| `SESSION_COOKIE_HTTPONLY`    | `True`                   | Cookie inaccessible to JavaScript (`document.cookie`) |
| `SESSION_COOKIE_SAMESITE`    | `'Lax'`                  | Mitigates CSRF in cross-site navigations            |
| `SESSION_COOKIE_SECURE`      | `False` (dev) / `True` (prod) | Restricts cookie to HTTPS in production       |
| `PERMANENT_SESSION_LIFETIME` | 30 minutes (configurable)| Session expires after idle timeout                  |

An idle-timeout check in `before_request` compares `session['last_active']` against
`SESSION_TIMEOUT_MINUTES`. Expired sessions are cleared and the user is redirected to
the login page.

---

## 8. Security Headers

An `after_request` hook adds the following HTTP security headers to every response:

| Header                      | Value                                      | Protection                         |
|-----------------------------|--------------------------------------------|------------------------------------|
| `X-Frame-Options`           | `DENY`                                     | Prevents clickjacking via iframes  |
| `X-Content-Type-Options`    | `nosniff`                                  | Prevents MIME-type sniffing        |
| `Referrer-Policy`           | `no-referrer-when-downgrade`               | Controls Referer leakage           |
| `Content-Security-Policy`   | (see Section 5)                            | XSS mitigation                     |

---

## 9. Role-Based Access Control (RBAC)

Three roles are enforced: `employee`, `trainer` (staff), and `admin`.

The `roles_required(*roles)` decorator in `app/security.py`:
- Returns **HTTP 401** (redirected to login by `login_manager`) for unauthenticated users.
- Returns **HTTP 403** for authenticated users whose role is not in the allowed list.

Convenience decorators:
- `@admin_required` – admin only.
- `@staff_required` – admin or trainer.

Every admin and staff route is decorated with one of these.

---

## 10. Activity Logging

`log_activity(action, user=None)` creates an `ActivityLog` record containing:
- `user_id` (nullable for anonymous actions)
- `action` – free-text description (e.g. `"login_success"`, `"quiz_attempt"`)
- `ip_address` – `request.remote_addr`
- `created_at` – UTC timestamp

Logged events include:
- Login success and failure (with email attempted)
- Quiz submissions (module ID, score, pass/fail)
- Module completion milestones
- Phishing simulation responses (correct/incorrect)

---

## 11. Limitations and Future Improvements

| Area                      | Current State                               | Recommended Improvement                              |
|---------------------------|---------------------------------------------|------------------------------------------------------|
| Database                  | SQLite (file-based)                         | Migrate to PostgreSQL for production workloads       |
| Password policy           | Minimum 8 characters, no complexity enforcement at DB layer | Add server-side strength validation (zxcvbn or regex) |
| Account lockout           | Rate limit on IP; no per-account lockout    | Implement per-email failed-attempt counter           |
| MFA / 2FA                 | Not implemented                             | Add TOTP (e.g. PyOTP + QR enrollment)                |
| Email verification        | Not implemented                             | Send confirmation email on registration              |
| Password reset            | Not implemented                             | Add time-limited reset tokens via email              |
| Audit log retention       | Unlimited growth in DB                      | Add log rotation / export to external SIEM           |
| Dependency scanning       | Not automated                               | Add `pip-audit` or Dependabot to CI pipeline         |
| Secret management         | `.env` file                                 | Use a secrets manager (Vault, AWS Secrets Manager)   |
| HTTPS enforcement         | Relies on reverse proxy (EasyPanel / Nginx) | Set `SESSION_COOKIE_SECURE=true` and HSTS header     |
| CSP `unsafe-inline`       | Required for inline styles / scripts        | Move to nonce-based CSP to eliminate `unsafe-inline` |
