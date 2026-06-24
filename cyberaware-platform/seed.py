"""Seed the CyberAware database with demo data.

Idempotent-ish: skips if the admin user already exists.
Run: python seed.py   (or: flask seed)
"""
from datetime import datetime, timedelta

from app import create_app
from app.extensions import db
from app.models import (
    User, TrainingModule, QuizQuestion, QuizAttempt, UserProgress,
    PhishingCampaign, PhishingAssignment, ActivityLog
)


# ---------------------------------------------------------------------------
# Module content (authored / trusted HTML).
# ---------------------------------------------------------------------------

SECURE_CODING_CONTENT = """
<section>
  <h2>Secure Coding Practices</h2>
  <p>Most breaches start with a single insecure line of code. In this module you
  will learn to recognize and remediate three of the most damaging classes of
  vulnerability: <strong>SQL Injection</strong>, <strong>Cross-Site Scripting
  (XSS)</strong>, and <strong>Buffer Overflows</strong>.</p>
</section>

<section>
  <h3>1. SQL Injection (SQLi)</h3>
  <p>SQL injection happens when untrusted input is concatenated directly into a
  query. Attackers can read, modify, or destroy data. The fix is
  <em>parameterized queries</em>.</p>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code># VULNERABLE: string concatenation
query = "SELECT * FROM users WHERE email = '" + email + "'"
db.execute(query)
# Input:  ' OR '1'='1  -> returns every user</code></pre>
    <pre class="code-block secure"><code># SECURE: parameterized query
query = "SELECT * FROM users WHERE email = ?"
db.execute(query, (email,))
# The driver escapes the value safely</code></pre>
  </div>
</section>

<section>
  <h3>2. Cross-Site Scripting (XSS)</h3>
  <p>XSS occurs when an application reflects untrusted input into HTML without
  encoding it, letting attackers run JavaScript in a victim's browser. Encode on
  output and rely on template auto-escaping.</p>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>// VULNERABLE: raw HTML injection
element.innerHTML = "Hello " + userName;
// userName = &lt;img src=x onerror=alert(1)&gt;</code></pre>
    <pre class="code-block secure"><code>// SECURE: assign as text, not HTML
element.textContent = "Hello " + userName;
// Browser never parses it as markup</code></pre>
  </div>
</section>

<section>
  <h3>3. Buffer Overflow</h3>
  <p>In memory-unsafe languages, copying more bytes than a buffer can hold lets
  attackers overwrite adjacent memory and hijack control flow. Always use
  bounded operations.</p>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>/* VULNERABLE: no bounds check */
char buf[16];
strcpy(buf, user_input);   /* overflows if &gt;16 bytes */</code></pre>
    <pre class="code-block secure"><code>/* SECURE: bounded copy */
char buf[16];
strncpy(buf, user_input, sizeof(buf) - 1);
buf[sizeof(buf) - 1] = '\\0';</code></pre>
  </div>
</section>

<section class="exercise" data-exercise="code-review">
  <h3>Quick check: Is this snippet secure or vulnerable?</h3>
  <pre class="code-block"><code>cursor.execute("DELETE FROM logs WHERE id = " + str(req.id))</code></pre>
  <p>Click your answer:</p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="secure">Secure</button>
    <button type="button" class="btn btn-secondary" data-answer="vulnerable" data-correct="true">Vulnerable</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""


SOCIAL_ENGINEERING_CONTENT = """
<section>
  <h2>Social Engineering Awareness</h2>
  <p>Attackers often skip technology entirely and target people. This module
  covers the most common human-focused attacks: <strong>phishing</strong>,
  <strong>pretexting</strong>, and <strong>baiting</strong>.</p>
</section>

<section>
  <h3>1. Phishing</h3>
  <p>Fraudulent messages that impersonate a trusted brand or colleague to steal
  credentials or money. Watch for urgency, mismatched sender domains, generic
  greetings, and links that do not match their display text.</p>
  <ul>
    <li>Hover over links before clicking to reveal the true destination.</li>
    <li>Verify unexpected requests through a second channel.</li>
    <li>Never enter credentials after following an email link.</li>
  </ul>
</section>

<section>
  <h3>2. Pretexting</h3>
  <p>The attacker invents a believable scenario (the "pretext") to extract
  information. For example, posing as IT support to "verify" your password, or
  as a vendor needing updated bank details.</p>
  <ul>
    <li>Legitimate IT will never ask for your password.</li>
    <li>Confirm identity using official directory contacts, not numbers the
    caller provides.</li>
  </ul>
</section>

<section>
  <h3>3. Baiting</h3>
  <p>Baiting lures victims with something enticing: a "Salary_2026.xlsx" file, a
  free gift card, or a USB drive left in the parking lot. Curiosity delivers the
  malware.</p>
  <ul>
    <li>Never plug in unknown USB devices.</li>
    <li>Be skeptical of "too good to be true" downloads.</li>
  </ul>
</section>

<section class="exercise" data-exercise="scenario">
  <h3>Scenario: How should you respond?</h3>
  <p><em>You receive a call: "Hi, this is IT. We detected a virus on your laptop.
  Read me the 6-digit code we just texted you so we can secure your account."</em></p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="unsafe">Read out the code to help them</button>
    <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Hang up and call IT through the official help desk</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""


THREAT_MODELING_CONTENT = """
<section>
  <h2>Threat Modeling</h2>
  <p>Threat modeling is the practice of systematically finding what can go wrong
  with a system before attackers do. Two classic frameworks are
  <strong>STRIDE</strong> (for identifying threats) and <strong>DREAD</strong>
  (for rating their risk).</p>
</section>

<section>
  <h3>STRIDE</h3>
  <table class="table">
    <thead><tr><th>Letter</th><th>Threat</th><th>Property violated</th></tr></thead>
    <tbody>
      <tr><td>S</td><td>Spoofing</td><td>Authentication</td></tr>
      <tr><td>T</td><td>Tampering</td><td>Integrity</td></tr>
      <tr><td>R</td><td>Repudiation</td><td>Non-repudiation</td></tr>
      <tr><td>I</td><td>Information Disclosure</td><td>Confidentiality</td></tr>
      <tr><td>D</td><td>Denial of Service</td><td>Availability</td></tr>
      <tr><td>E</td><td>Elevation of Privilege</td><td>Authorization</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>DREAD</h3>
  <p>Score each threat 1-10 on: <strong>D</strong>amage, <strong>R</strong>eproducibility,
  <strong>E</strong>xploitability, <strong>A</strong>ffected users, and
  <strong>D</strong>iscoverability, then average to prioritize remediation.</p>
</section>

<section class="exercise" data-exercise="threat">
  <h3>Match the threat to its STRIDE category</h3>
  <p>An attacker forges a session cookie to log in as another user. Which STRIDE
  category best fits?</p>
  <div class="exercise-options">
    <label><input type="checkbox" data-answer="spoofing" data-correct="true"> Spoofing</label>
    <label><input type="checkbox" data-answer="dos"> Denial of Service</label>
    <label><input type="checkbox" data-answer="repudiation"> Repudiation</label>
  </div>
  <button type="button" class="btn btn-primary" data-action="check">Check</button>
  <p class="exercise-feedback" hidden></p>
</section>
"""


# ---------------------------------------------------------------------------
# Quiz definitions: list of (question, a, b, c, d, correct, explanation)
# ---------------------------------------------------------------------------

SECURE_CODING_QUIZ = [
    ("What is the most effective defense against SQL injection?",
     "Hiding error messages", "Using parameterized queries",
     "Encrypting the database", "Renaming database tables", "B",
     "Parameterized (prepared) statements separate code from data so user input "
     "can never be interpreted as SQL."),
    ("Cross-site scripting (XSS) primarily allows an attacker to:",
     "Crash the database server", "Run arbitrary JavaScript in a victim's browser",
     "Overwrite the stack", "Bypass TLS encryption", "B",
     "XSS injects script that executes in the victim's browser context, enabling "
     "session theft and UI redressing."),
    ("Which function call is safest when copying a string in C?",
     "strcpy(dst, src)", "gets(dst)", "strncpy(dst, src, sizeof(dst)-1)",
     "sprintf(dst, src)", "C",
     "strncpy with an explicit length (and manual null termination) bounds the "
     "copy and prevents buffer overflows."),
    ("In a web template engine, output auto-escaping helps prevent:",
     "SQL injection", "Buffer overflow", "Cross-site scripting (XSS)",
     "Denial of service", "C",
     "Auto-escaping encodes special HTML characters on output, neutralizing "
     "reflected and stored XSS."),
    ("Why is concatenating user input into a query string dangerous?",
     "It is slower than other methods", "Input can alter the query's logic",
     "It uses more memory", "It breaks Unicode support", "B",
     "Concatenation lets attacker-controlled characters change the structure of "
     "the query, which is the root of SQL injection."),
    ("The principle of 'never trust user input' means you should:",
     "Validate and sanitize all external data", "Disable all input fields",
     "Only accept input from admins", "Log every keystroke", "A",
     "All data crossing a trust boundary must be validated and properly handled "
     "before use."),
]

SOCIAL_ENGINEERING_QUIZ = [
    ("An email creates a sense of urgency and asks you to 'verify your password "
     "immediately'. This is a sign of:",
     "A system update", "A phishing attempt", "A newsletter", "A calendar invite",
     "B",
     "Urgency plus a credential request is a classic phishing pressure tactic."),
    ("Pretexting is best described as:",
     "Sending bulk spam", "Inventing a false scenario to extract information",
     "Installing a keylogger", "Guessing passwords", "B",
     "Pretexting relies on a fabricated but believable story to manipulate the "
     "target into divulging information."),
    ("You find a USB drive labeled 'Payroll' in the parking lot. You should:",
     "Plug it in to find the owner", "Hand it to IT/security without plugging it in",
     "Take it home to check", "Email its contents to HR", "B",
     "Unknown USB devices are a baiting vector; never connect them. Report to "
     "security instead."),
    ("Which is the safest way to verify a suspicious request from your 'CEO' for "
     "a wire transfer?",
     "Reply to the email", "Call back the number in the email",
     "Confirm via a known internal channel", "Just process it to be safe", "C",
     "Always verify out-of-band using contact details you already trust, never "
     "details supplied by the message."),
    ("Legitimate IT support will:",
     "Ask for your password to help you", "Never ask for your password",
     "Email you a login link to click", "Request your MFA code by phone", "B",
     "Real IT never needs your password or one-time codes; requests for them are "
     "social engineering."),
    ("Hovering over a link before clicking helps you:",
     "Speed up the page", "See the true destination URL",
     "Encrypt the connection", "Block cookies", "B",
     "Hovering reveals the actual target so you can spot mismatched or malicious "
     "domains before clicking."),
]

THREAT_MODELING_QUIZ = [
    ("What does the 'S' in STRIDE stand for?",
     "Scanning", "Spoofing", "Sniffing", "Spamming", "B",
     "STRIDE's S is Spoofing, which violates the authentication property."),
    ("Tampering threats violate which security property?",
     "Confidentiality", "Availability", "Integrity", "Authentication", "C",
     "Tampering is unauthorized modification of data or code, breaking "
     "integrity."),
    ("Elevation of Privilege most directly threatens:",
     "Authorization controls", "Network bandwidth", "Backup schedules",
     "Code readability", "A",
     "Elevation of Privilege lets an attacker gain rights beyond what they are "
     "authorized for."),
    ("DREAD is used to:",
     "Discover new threats", "Rate and prioritize the risk of threats",
     "Encrypt traffic", "Generate passwords", "B",
     "DREAD scores threats on Damage, Reproducibility, Exploitability, Affected "
     "users, and Discoverability to rank them."),
    ("A denial-of-service attack primarily impacts which property?",
     "Confidentiality", "Integrity", "Availability", "Non-repudiation", "C",
     "DoS aims to make a system or service unavailable to legitimate users."),
    ("When should threat modeling ideally be performed?",
     "Only after a breach", "Early in the design phase",
     "Never, it is optional", "Only during a yearly audit", "B",
     "Modeling threats during design lets you address them before they are built "
     "into the system, which is far cheaper."),
]


def _add_questions(module, quiz):
    for (q, a, b, c, d, correct, expl) in quiz:
        db.session.add(QuizQuestion(
            module_id=module.id, question=q,
            option_a=a, option_b=b, option_c=c, option_d=d,
            correct_answer=correct, explanation=expl,
        ))


def seed():
    """Populate demo data. No-op if admin already exists."""
    app = None
    # Allow running both inside an existing app context and standalone.
    from flask import current_app
    try:
        current_app._get_current_object()
        _do_seed()
        return
    except RuntimeError:
        app = create_app()
        with app.app_context():
            _do_seed()


def _do_seed():
    if User.query.filter_by(email='admin@cyberaware.local').first():
        print('Admin already exists; skipping seed.')
        return

    db.create_all()

    # --- Users ---
    admin = User(name='Alice Admin', email='admin@cyberaware.local',
                 role='admin', department='Security')
    admin.set_password('Admin@12345')

    trainer = User(name='Trevor Trainer', email='trainer@cyberaware.local',
                   role='trainer', department='Learning & Development')
    trainer.set_password('Trainer@12345')

    emp1 = User(name='Emma Employee', email='employee@cyberaware.local',
                role='employee', department='Finance')
    emp1.set_password('Employee@12345')
    emp2 = User(name='Evan Employee', email='employee2@cyberaware.local',
                role='employee', department='Engineering')
    emp2.set_password('Employee@12345')
    emp3 = User(name='Erin Employee', email='employee3@cyberaware.local',
                role='employee', department='Marketing')
    emp3.set_password('Employee@12345')

    db.session.add_all([admin, trainer, emp1, emp2, emp3])
    db.session.commit()

    employees = [emp1, emp2, emp3]

    # --- Training modules ---
    m1 = TrainingModule(
        title='Secure Coding Practices',
        description='Identify and fix SQL injection, XSS, and buffer overflow '
                    'vulnerabilities with side-by-side code examples.',
        content=SECURE_CODING_CONTENT,
        category='Application Security', is_active=True, order=1,
    )
    m2 = TrainingModule(
        title='Social Engineering Awareness',
        description='Recognize phishing, pretexting, and baiting attacks that '
                    'target people instead of systems.',
        content=SOCIAL_ENGINEERING_CONTENT,
        category='Human Risk', is_active=True, order=2,
    )
    m3 = TrainingModule(
        title='Threat Modeling',
        description='Use STRIDE and DREAD to systematically find and prioritize '
                    'security threats during design.',
        content=THREAT_MODELING_CONTENT,
        category='Security Design', is_active=True, order=3,
    )
    db.session.add_all([m1, m2, m3])
    db.session.commit()

    _add_questions(m1, SECURE_CODING_QUIZ)
    _add_questions(m2, SOCIAL_ENGINEERING_QUIZ)
    _add_questions(m3, THREAT_MODELING_QUIZ)
    db.session.commit()

    modules = [m1, m2, m3]

    # --- Assign all modules to all employees (UserProgress rows) ---
    for emp in employees:
        for m in modules:
            db.session.add(UserProgress(
                user_id=emp.id, module_id=m.id,
                status='not_started', completion_percentage=0,
            ))
    db.session.commit()

    # --- Some completed attempts & progress so dashboards have data ---
    def set_progress(user, module, status, pct, completed_at=None):
        p = UserProgress.query.filter_by(
            user_id=user.id, module_id=module.id
        ).first()
        p.status = status
        p.completion_percentage = pct
        p.completed_at = completed_at
        return p

    now = datetime.utcnow()

    # emp1: completed m1 (90) and m2 (75), in progress m3
    db.session.add(QuizAttempt(user_id=emp1.id, module_id=m1.id, score=90,
                               passed=True, created_at=now - timedelta(days=5)))
    set_progress(emp1, m1, 'completed', 100, now - timedelta(days=5))
    db.session.add(QuizAttempt(user_id=emp1.id, module_id=m2.id, score=75,
                               passed=True, created_at=now - timedelta(days=3)))
    set_progress(emp1, m2, 'completed', 100, now - timedelta(days=3))
    set_progress(emp1, m3, 'in_progress', 50)

    # emp2: completed m1 (100), failed m2 (50) then passed (80)
    db.session.add(QuizAttempt(user_id=emp2.id, module_id=m1.id, score=100,
                               passed=True, created_at=now - timedelta(days=4)))
    set_progress(emp2, m1, 'completed', 100, now - timedelta(days=4))
    db.session.add(QuizAttempt(user_id=emp2.id, module_id=m2.id, score=50,
                               passed=False, created_at=now - timedelta(days=2)))
    db.session.add(QuizAttempt(user_id=emp2.id, module_id=m2.id, score=83,
                               passed=True, created_at=now - timedelta(days=1)))
    set_progress(emp2, m2, 'completed', 100, now - timedelta(days=1))

    # emp3: only started m1
    set_progress(emp3, m1, 'in_progress', 50)
    db.session.add(QuizAttempt(user_id=emp3.id, module_id=m1.id, score=60,
                               passed=False, created_at=now - timedelta(hours=6)))

    db.session.commit()

    # --- Phishing campaigns (mix of phishing/legitimate) ---
    c1 = PhishingCampaign(
        title='Password Expiry Notice',
        subject='ACTION REQUIRED: Your password expires in 24 hours',
        sender_name='IT Helpdesk', sender_email='it-support@cyberware-secure.com',
        body='<p>Dear User,</p><p>Our records show your password will expire in '
             '24 hours. To avoid losing access, please '
             '<a href="http://cyberware-secure.com/reset">verify your account '
             'here</a> immediately.</p><p>Regards,<br>IT Helpdesk</p>',
        red_flags='Mismatched/look-alike sender domain (cyberware-secure.com)\n'
                  'Urgency and threat of losing access\n'
                  'Generic greeting "Dear User"\n'
                  'Link points to an external non-corporate domain',
        difficulty='easy', is_phishing=True, created_by=trainer.id,
    )
    c2 = PhishingCampaign(
        title='Gift Card Reward',
        subject='Congratulations! You have been selected for a $500 gift card',
        sender_name='HR Rewards', sender_email='rewards@amaz0n-perks.net',
        body='<p>You have been randomly selected to receive a $500 gift card as '
             'part of our employee appreciation program. '
             '<a href="http://amaz0n-perks.net/claim">Click here to claim within '
             '1 hour</a>.</p>',
        red_flags='Too-good-to-be-true reward (baiting)\n'
                  'Look-alike domain using a zero (amaz0n-perks.net)\n'
                  'High-pressure 1-hour deadline\n'
                  'Unsolicited prize you never entered for',
        difficulty='medium', is_phishing=True, created_by=trainer.id,
    )
    c3 = PhishingCampaign(
        title='Quarterly All-Hands Invite',
        subject='Invitation: Q3 All-Hands Meeting on Friday',
        sender_name='People Team', sender_email='people@cyberaware.local',
        body='<p>Hi team,</p><p>You are invited to our Q3 All-Hands on Friday at '
             '10:00 in the main auditorium. The agenda and slides are on the '
             'internal wiki. No action needed if you already RSVP\'d.</p>'
             '<p>Thanks,<br>The People Team</p>',
        red_flags='', difficulty='easy', is_phishing=False, created_by=trainer.id,
    )
    c4 = PhishingCampaign(
        title='Invoice Payment Update',
        subject='Updated banking details for invoice #INV-4821',
        sender_name='Acme Vendor Billing', sender_email='billing@acme-vendor-pay.com',
        body='<p>Hello,</p><p>Please note our bank account has changed. Kindly '
             'remit payment for invoice #INV-4821 to the new account attached. '
             'Confirm once processed.</p><p>Accounts Receivable</p>',
        red_flags='Unexpected change of banking details (BEC pretexting)\n'
                  'External pay-themed domain (acme-vendor-pay.com)\n'
                  'Pressure to act and confirm quickly\n'
                  'No prior verification through a known channel',
        difficulty='hard', is_phishing=True, created_by=trainer.id,
    )
    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()

    campaigns = [c1, c2, c3, c4]

    # --- Phishing assignments to all employees ---
    for emp in employees:
        for c in campaigns:
            db.session.add(PhishingAssignment(campaign_id=c.id, user_id=emp.id))
    db.session.commit()

    # --- Some phishing responses (mix correct/incorrect) ---
    def respond(user, campaign, response):
        a = PhishingAssignment.query.filter_by(
            campaign_id=campaign.id, user_id=user.id
        ).first()
        a.user_response = response
        a.is_correct = (response == campaign.correct_response)
        a.responded_at = datetime.utcnow()

    respond(emp1, c1, 'phishing')      # correct
    respond(emp1, c3, 'legitimate')    # correct
    respond(emp2, c1, 'legitimate')    # incorrect (it was phishing)
    respond(emp2, c2, 'phishing')      # correct
    respond(emp3, c3, 'phishing')      # incorrect (it was legitimate)
    db.session.commit()

    # --- A few activity log entries ---
    db.session.add_all([
        ActivityLog(user_id=admin.id, action='seed: demo data created',
                    ip_address='127.0.0.1'),
        ActivityLog(user_id=emp1.id, action='login_success',
                    ip_address='127.0.0.1'),
        ActivityLog(user_id=emp2.id, action='quiz_attempt: module=1 score=100',
                    ip_address='127.0.0.1'),
    ])
    db.session.commit()

    print('Seed complete: 5 users, 3 modules, %d questions, %d campaigns.'
          % (QuizQuestion.query.count(), PhishingCampaign.query.count()))


if __name__ == '__main__':
    seed()
