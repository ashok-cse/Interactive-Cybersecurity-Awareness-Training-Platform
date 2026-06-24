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

# Externalised content: 15 "top attack" modules + 20 extra questions per
# existing module (see seed_data/). Kept in separate files so the large quiz
# content stays out of this orchestration module.
from seed_data.attacks_a import MODULES as _ATTACKS_A
from seed_data.attacks_b import MODULES as _ATTACKS_B
from seed_data.attacks_c import MODULES as _ATTACKS_C
from seed_data.existing_extra import EXTRA_QUESTIONS

NEW_ATTACK_MODULES = _ATTACKS_A + _ATTACKS_B + _ATTACKS_C


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


PASSWORD_ATTACKS_CONTENT = """
<section>
  <h2>Password &amp; Authentication Attacks</h2>
  <p>Credentials are the keys to the kingdom. This module covers how attackers
  defeat passwords &mdash; <strong>brute force</strong>, <strong>credential
  stuffing</strong>, <strong>password spraying</strong>, and <strong>MFA
  fatigue</strong> &mdash; and the controls that stop them.</p>
</section>

<section>
  <h3>1. Brute force &amp; password spraying</h3>
  <p>Brute force tries many passwords against one account; password spraying
  tries one common password (e.g. <code>Spring2024!</code>) across many accounts
  to dodge lockouts. Both are beaten by rate limiting, lockouts, and long unique
  passphrases.</p>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code># VULNERABLE: unlimited login attempts
def login(user, pw):
    return check(user, pw)   # no throttling, no lockout</code></pre>
    <pre class="code-block secure"><code># SECURE: throttle + lockout
@limiter.limit("5 per minute")
def login(user, pw):
    if locked_out(user): abort(429)
    return check(user, pw)</code></pre>
  </div>
</section>

<section>
  <h3>2. Credential stuffing</h3>
  <p>Attackers replay username/password pairs leaked from <em>other</em> breaches,
  betting that people reuse passwords. A unique password per site plus MFA makes a
  leaked password useless elsewhere.</p>
  <ul>
    <li>Use a password manager so every login is unique.</li>
    <li>Turn on multi-factor authentication (MFA) everywhere.</li>
    <li>Check exposure at your org's breach-monitoring tool.</li>
  </ul>
</section>

<section>
  <h3>3. MFA fatigue (push bombing)</h3>
  <p>Once an attacker has your password, they spam you with approval prompts
  hoping you tap &ldquo;Approve&rdquo; out of annoyance. Never approve a prompt you
  did not start &mdash; deny it and change your password.</p>
</section>

<section class="exercise" data-exercise="scenario">
  <h3>Scenario: How should you respond?</h3>
  <p><em>Your phone buzzes with repeated &ldquo;Approve sign-in?&rdquo; prompts you
  did not request, at 2 a.m.</em></p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="unsafe">Approve one so they stop</button>
    <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Deny, then change your password and tell security</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""


MALWARE_CONTENT = """
<section>
  <h2>Malware &amp; Ransomware</h2>
  <p>Malware is any software built to harm or exploit a system. This module covers
  the main families &mdash; <strong>viruses &amp; worms</strong>,
  <strong>trojans</strong>, <strong>spyware/keyloggers</strong>, and
  <strong>ransomware</strong> &mdash; and how to avoid and contain them.</p>
</section>

<section>
  <h3>1. Common malware families</h3>
  <table class="table">
    <thead><tr><th>Type</th><th>How it spreads</th><th>Goal</th></tr></thead>
    <tbody>
      <tr><td>Virus / Worm</td><td>Infected files; self-propagation</td><td>Spread &amp; damage</td></tr>
      <tr><td>Trojan</td><td>Disguised as legit software</td><td>Backdoor access</td></tr>
      <tr><td>Spyware / Keylogger</td><td>Bundled downloads, phishing</td><td>Steal data &amp; keystrokes</td></tr>
      <tr><td>Ransomware</td><td>Phishing, RDP, exploits</td><td>Encrypt &amp; extort</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>2. Ransomware</h3>
  <p>Ransomware encrypts your files and demands payment. The best defense is
  prevention plus <strong>tested, offline backups</strong> so you can restore
  without paying. Paying funds crime and never guarantees recovery.</p>
  <ul>
    <li>Patch promptly and disable macros from the internet.</li>
    <li>Keep 3-2-1 backups (3 copies, 2 media, 1 offline).</li>
    <li>Isolate an infected machine from the network immediately.</li>
  </ul>
</section>

<section>
  <h3>3. Infection vectors to watch</h3>
  <p>Most malware arrives through phishing attachments, malicious links, pirated
  software, and unknown USB drives. When in doubt, do not open it &mdash; report it.</p>
</section>

<section class="exercise" data-exercise="scenario">
  <h3>Scenario: How should you respond?</h3>
  <p><em>A file you opened just popped up: &ldquo;Your files are encrypted. Pay 0.5
  BTC to recover them.&rdquo;</em></p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="unsafe">Pay quickly before the deadline</button>
    <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Disconnect from the network and call security/IT now</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""


NETWORK_WEB_CONTENT = """
<section>
  <h2>Network &amp; Web Attacks</h2>
  <p>Beyond code and people, attackers target the wire and the web app itself. This
  module covers <strong>Man-in-the-Middle (MITM)</strong>,
  <strong>Denial of Service (DoS/DDoS)</strong>, <strong>Cross-Site Request
  Forgery (CSRF)</strong>, and <strong>Insecure Direct Object References
  (IDOR)</strong>.</p>
</section>

<section>
  <h3>1. Man-in-the-Middle (MITM)</h3>
  <p>On open Wi-Fi an attacker can sit between you and a site, reading or altering
  traffic. Always use HTTPS and a corporate VPN on untrusted networks; never ignore
  certificate warnings.</p>
</section>

<section>
  <h3>2. Denial of Service (DoS / DDoS)</h3>
  <p>Floods of traffic exhaust a service so real users cannot reach it &mdash; an
  <em>availability</em> attack. Defenses include rate limiting, autoscaling, and
  upstream DDoS protection.</p>
</section>

<section>
  <h3>3. Cross-Site Request Forgery (CSRF)</h3>
  <p>CSRF tricks a logged-in user's browser into submitting an unwanted action. The
  fix is an unguessable anti-CSRF token on every state-changing request &mdash;
  exactly what this platform does on its forms.</p>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>&lt;!-- VULNERABLE: no token --&gt;
&lt;form method="post" action="/transfer"&gt;
  &lt;input name="amount" value="1000"&gt;
&lt;/form&gt;</code></pre>
    <pre class="code-block secure"><code>&lt;!-- SECURE: anti-CSRF token --&gt;
&lt;form method="post" action="/transfer"&gt;
  &lt;input type="hidden" name="csrf_token" value="..."&gt;
  &lt;input name="amount" value="1000"&gt;
&lt;/form&gt;</code></pre>
  </div>
</section>

<section>
  <h3>4. Insecure Direct Object Reference (IDOR)</h3>
  <p>If <code>/invoice/123</code> lets you read someone else's invoice by changing
  the number, that is IDOR. Always enforce an ownership/authorization check on the
  server, not just hide the link.</p>
</section>

<section class="exercise" data-exercise="code-review">
  <h3>Quick check: Is this route secure or vulnerable?</h3>
  <pre class="code-block"><code>@app.get("/invoice/&lt;id&gt;")
def invoice(id):
    return Invoice.query.get(id)   # returns any invoice by id</code></pre>
  <p>Click your answer:</p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="secure">Secure</button>
    <button type="button" class="btn btn-secondary" data-answer="vulnerable" data-correct="true">Vulnerable</button>
  </div>
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
    ("Which practice best prevents stored XSS in user-generated content?",
     "Storing input in uppercase", "Context-aware output encoding/escaping",
     "Using a faster database", "Allowing all HTML tags", "B",
     "Encoding data for the context where it is rendered stops the browser from "
     "executing injected markup or script."),
    ("An ORM like SQLAlchemy helps prevent SQL injection because it:",
     "Encrypts the whole database", "Parameterizes queries by default",
     "Disables the network", "Caches every query", "B",
     "ORMs bind parameters separately from the SQL text, so user data is never "
     "parsed as part of the query."),
    ("What is the safest way to handle secrets like API keys in code?",
     "Hard-code them for convenience", "Commit them to the repo",
     "Load them from environment variables / a secrets manager",
     "Email them to the team", "C",
     "Secrets should live outside source control, injected via environment "
     "variables or a dedicated secrets manager."),
    ("'Defense in depth' means:",
     "Relying on one strong firewall", "Layering multiple independent controls",
     "Only encrypting passwords", "Hiding the source code", "B",
     "Multiple overlapping controls ensure that if one fails, others still "
     "protect the system."),
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
    ("'Smishing' refers to social engineering carried out over:",
     "SMS text messages", "Smoke signals", "Shared printers", "Slack only", "A",
     "Smishing is phishing via SMS; vishing is via voice calls. Treat unexpected "
     "links and requests in texts with the same caution as email."),
    ("A caller claims to be your bank and asks you to read back a code 'to verify "
     "your identity'. You should:",
     "Read the code to prove who you are", "Refuse and hang up; banks never ask "
     "for one-time codes", "Give it only if they sound official", "Text it instead",
     "B",
     "One-time codes authenticate YOU; anyone asking you to share one is trying "
     "to take over your account."),
    ("Tailgating in physical security means:",
     "Driving too close", "Following an authorized person through a secure door",
     "Spamming an inbox", "Reusing a password", "B",
     "Tailgating is following someone into a restricted area without badging in; "
     "always ensure doors close behind you."),
    ("The strongest reason to report a phishing email you spotted is:",
     "To get a reward", "So security can warn others and block the campaign",
     "To delete it faster", "It is required by law everywhere", "B",
     "Reporting lets the security team contain the campaign and protect colleagues "
     "who may also have received it."),
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
    ("Information Disclosure in STRIDE violates which property?",
     "Availability", "Confidentiality", "Integrity", "Authentication", "B",
     "Information Disclosure exposes data to those not authorized to see it, "
     "breaking confidentiality."),
    ("Repudiation threats are best countered by:",
     "Faster servers", "Secure audit logging and signatures",
     "Bigger passwords", "More RAM", "B",
     "Tamper-evident logs and digital signatures let you prove who did what, "
     "defeating repudiation."),
    ("A 'trust boundary' in a data-flow diagram is where:",
     "Two servers share a cable", "Data crosses between different privilege levels",
     "The CPU meets the GPU", "Logs are rotated", "B",
     "Trust boundaries mark where data moves between components of differing trust, "
     "the places most worth scrutinizing for threats."),
    ("After identifying and rating threats, the next step is to:",
     "Ignore low-cost ones", "Define and track mitigations for prioritized threats",
     "Delete the model", "Publish them publicly", "B",
     "Threat modeling drives action: each significant threat should get an owned, "
     "tracked mitigation."),
]

PASSWORD_ATTACKS_QUIZ = [
    ("Password spraying differs from brute force because it:",
     "Tries many passwords on one account",
     "Tries one common password across many accounts",
     "Only targets admins", "Requires the password already", "B",
     "Spraying uses a few common passwords against many accounts to avoid "
     "triggering per-account lockouts."),
    ("Credential stuffing succeeds mainly because people:",
     "Use long passwords", "Reuse the same password across sites",
     "Enable MFA", "Use password managers", "B",
     "Reused passwords let attackers replay credentials leaked from one breach "
     "against your other accounts."),
    ("The single most effective add-on defense against stolen passwords is:",
     "A longer username", "Multi-factor authentication (MFA)",
     "Changing passwords daily", "A custom font", "B",
     "MFA means a stolen password alone is not enough to log in."),
    ("'MFA fatigue' attacks rely on the victim:",
     "Forgetting their password", "Approving a push prompt they did not initiate",
     "Using a hardware key", "Disabling notifications", "B",
     "Attackers spam approval prompts hoping you tap Approve; deny prompts you "
     "did not start and change your password."),
    ("Why is a password manager recommended?",
     "It makes passwords shorter", "It generates and stores unique strong passwords",
     "It disables MFA", "It shares passwords by email", "B",
     "A manager lets every account have a unique, strong password without you "
     "memorizing them."),
    ("A good account-protection control on login servers is:",
     "Unlimited attempts", "Rate limiting and lockout after repeated failures",
     "Logging passwords in plain text", "Disabling HTTPS", "B",
     "Throttling and lockouts blunt automated guessing attacks like brute force "
     "and spraying."),
    ("The most phishing-resistant form of MFA is:",
     "SMS one-time codes", "Email codes",
     "A FIDO2/WebAuthn hardware security key", "Security questions", "C",
     "Hardware security keys bind the login to the real site's origin, so they "
     "cannot be relayed to a phishing page like SMS or app codes."),
    ("Storing user passwords safely on a server means:",
     "Encrypting them reversibly", "Saving them in plain text",
     "Hashing them with a slow salted algorithm (e.g. bcrypt/argon2)",
     "Emailing them to the user", "C",
     "Passwords should be one-way hashed with a slow, salted algorithm so a "
     "database leak does not reveal them."),
    ("'Passwordless' login with passkeys improves security mainly because:",
     "Passkeys are shorter", "There is no shared secret to phish or reuse",
     "They never expire", "They disable MFA", "B",
     "Passkeys use public-key cryptography, so there is no reusable secret for an "
     "attacker to steal, phish, or replay."),
    ("After a confirmed credential breach, the FIRST priority is to:",
     "Buy new laptops", "Reset affected passwords and revoke active sessions/tokens",
     "Email all customers a coupon", "Ignore it if no money was lost", "B",
     "Containment starts by invalidating the compromised credentials and sessions "
     "so the attacker loses access."),
]

MALWARE_QUIZ = [
    ("Ransomware's primary goal is to:",
     "Speed up your PC", "Encrypt your files and demand payment",
     "Update your software", "Improve backups", "B",
     "Ransomware encrypts data and extorts the victim for a decryption key."),
    ("The best protection that lets you recover from ransomware without paying is:",
     "Antivirus alone", "Tested offline backups",
     "A faster CPU", "Paying quickly", "B",
     "Reliable offline (3-2-1) backups let you restore data instead of paying a "
     "ransom."),
    ("A trojan is malware that:",
     "Self-replicates across networks", "Disguises itself as legitimate software",
     "Only affects servers", "Cannot be removed", "B",
     "A trojan tricks the user into running it by masquerading as something "
     "trustworthy."),
    ("If you suspect your machine is infected, you should first:",
     "Keep working", "Disconnect it from the network and report it",
     "Email the file to colleagues", "Pay any ransom", "B",
     "Isolating the device limits spread; then let security/IT investigate."),
    ("Which is a common malware infection vector?",
     "Reading plain-text email", "Opening a malicious attachment or link",
     "Locking your screen", "Using a password manager", "B",
     "Phishing attachments and links are among the most common ways malware gets "
     "in."),
    ("A keylogger is a type of:",
     "Backup tool", "Spyware that records keystrokes",
     "Firewall", "Password manager", "B",
     "Keyloggers secretly capture what you type, including passwords, and send it "
     "to an attacker."),
    ("'Double extortion' ransomware adds which extra threat?",
     "Slower encryption", "Leaking stolen data publicly if the ransom is unpaid",
     "Free decryption", "Better backups", "B",
     "Double-extortion gangs steal data before encrypting and threaten to publish "
     "it, pressuring victims even when they have backups."),
    ("Macro malware most commonly arrives via:",
     "A firmware update", "Office documents with malicious macros",
     "A wired keyboard", "A monitor cable", "B",
     "Attackers embed malicious macros in documents and lure users to 'Enable "
     "Content'; disable macros from the internet by default."),
    ("The safest response to a suspicious email attachment is to:",
     "Open it to check", "Forward it to friends",
     "Not open it and report it to security", "Rename the file extension", "C",
     "Unexpected attachments are a top malware vector; verify out-of-band and let "
     "security analyze it."),
    ("Endpoint Detection and Response (EDR) primarily helps by:",
     "Speeding up the CPU", "Detecting and responding to malicious behavior on devices",
     "Encrypting the monitor", "Blocking all email", "B",
     "EDR monitors endpoint behavior to detect, investigate, and contain threats "
     "that signature-only antivirus may miss."),
]

NETWORK_WEB_QUIZ = [
    ("A Man-in-the-Middle attack is most likely on:",
     "A wired corporate LAN with TLS", "Open public Wi-Fi without a VPN",
     "An offline laptop", "A printed document", "B",
     "Untrusted open networks let an attacker intercept traffic; HTTPS and a VPN "
     "mitigate this."),
    ("A DoS/DDoS attack primarily harms which security property?",
     "Confidentiality", "Integrity", "Availability", "Non-repudiation", "C",
     "Denial of service floods a system so legitimate users cannot reach it, "
     "harming availability."),
    ("CSRF attacks are prevented by:",
     "Hiding the form", "Anti-CSRF tokens on state-changing requests",
     "Longer passwords", "Disabling cookies entirely", "B",
     "An unguessable per-session token ensures requests genuinely came from your "
     "app, not an attacker's page."),
    ("Changing /invoice/123 to /invoice/124 and seeing someone else's data is:",
     "XSS", "IDOR (broken object-level authorization)", "A DoS", "Spoofing", "B",
     "IDOR occurs when the server fails to check that the user owns the requested "
     "object."),
    ("The correct fix for IDOR is to:",
     "Use random-looking IDs only", "Enforce a server-side ownership/authorization "
     "check", "Hide the URL", "Cache the response", "B",
     "Obscurity is not enough; the server must verify the requester is authorized "
     "for that specific object."),
    ("Ignoring a browser certificate warning on public Wi-Fi can enable:",
     "Faster browsing", "A Man-in-the-Middle interception",
     "Better battery life", "Stronger encryption", "B",
     "Certificate warnings often signal interception; never click through them on "
     "untrusted networks."),
    ("Server-Side Request Forgery (SSRF) lets an attacker:",
     "Speed up the server", "Make the server send requests to unintended internal targets",
     "Encrypt the database", "Improve caching", "B",
     "SSRF abuses a server's ability to fetch URLs, reaching internal services or "
     "cloud metadata the attacker could not access directly."),
    ("Security headers like Content-Security-Policy primarily help mitigate:",
     "Disk failures", "Cross-site scripting (XSS)",
     "Slow networks", "Weak passwords", "B",
     "CSP restricts where scripts and resources may load from, reducing the impact "
     "of injected/XSS content."),
    ("HTTP Strict Transport Security (HSTS) protects users by:",
     "Compressing pages", "Forcing browsers to use HTTPS for the site",
     "Blocking cookies", "Disabling JavaScript", "B",
     "HSTS tells browsers to only connect over HTTPS, preventing downgrade and "
     "SSL-stripping man-in-the-middle attacks."),
    ("A WAF (Web Application Firewall) is best described as a control that:",
     "Backs up the database", "Filters and blocks malicious HTTP traffic to an app",
     "Encrypts the disk", "Manages passwords", "B",
     "A WAF inspects incoming web requests and blocks common application-layer "
     "attacks such as injection and XSS attempts."),
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
    m4 = TrainingModule(
        title='Password & Authentication Attacks',
        description='Defend against brute force, credential stuffing, password '
                    'spraying, and MFA fatigue with MFA and password managers.',
        content=PASSWORD_ATTACKS_CONTENT,
        category='Identity & Access', is_active=True, order=4,
    )
    m5 = TrainingModule(
        title='Malware & Ransomware',
        description='Recognize viruses, trojans, spyware, and ransomware, their '
                    'infection vectors, and how to contain and recover.',
        content=MALWARE_CONTENT,
        category='Endpoint Security', is_active=True, order=5,
    )
    m6 = TrainingModule(
        title='Network & Web Attacks',
        description='Understand MITM, DoS/DDoS, CSRF, and IDOR, and the controls '
                    'that stop them.',
        content=NETWORK_WEB_CONTENT,
        category='Network Security', is_active=True, order=6,
    )
    db.session.add_all([m1, m2, m3, m4, m5, m6])
    db.session.commit()

    _add_questions(m1, SECURE_CODING_QUIZ)
    _add_questions(m2, SOCIAL_ENGINEERING_QUIZ)
    _add_questions(m3, THREAT_MODELING_QUIZ)
    _add_questions(m4, PASSWORD_ATTACKS_QUIZ)
    _add_questions(m5, MALWARE_QUIZ)
    _add_questions(m6, NETWORK_WEB_QUIZ)
    db.session.commit()

    # Top up each existing module to 30 questions with the extra question banks.
    existing_by_title = {m.title: m for m in (m1, m2, m3, m4, m5, m6)}
    for title, extra in EXTRA_QUESTIONS.items():
        _add_questions(existing_by_title[title], extra)
    db.session.commit()

    # --- 15 "top attack" modules (orders 7-21) from seed_data ---
    new_modules = []
    for spec in NEW_ATTACK_MODULES:
        nm = TrainingModule(
            title=spec['title'], description=spec['description'],
            content=spec['content'], category=spec['category'],
            is_active=True, order=spec['order'],
        )
        db.session.add(nm)
        new_modules.append((nm, spec['questions']))
    db.session.commit()

    for nm, questions in new_modules:
        _add_questions(nm, questions)
    db.session.commit()

    modules = [m1, m2, m3, m4, m5, m6] + [nm for nm, _ in new_modules]

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
    c5 = PhishingCampaign(
        title='Shared Document Notification',
        subject='A document was shared with you: "Q3 Budget (Final).xlsx"',
        sender_name='DocuShare', sender_email='no-reply@docu-share-files.com',
        body='<p>Hello,</p><p>A colleague shared a document with you. '
             '<a href="http://docu-share-files.com/view?id=8842">Click here to '
             'view it</a>. You may need to sign in with your email password to '
             'access the file.</p><p>DocuShare</p>',
        red_flags='Asks you to sign in with your email password on a third-party '
                  'site (credential harvesting)\n'
                  'Look-alike external domain (docu-share-files.com)\n'
                  'Unexpected shared file from no specific person\n'
                  'Link points off your corporate domain',
        difficulty='medium', is_phishing=True, created_by=trainer.id,
    )
    c6 = PhishingCampaign(
        title='IT Maintenance Window',
        subject='Scheduled maintenance this weekend (no action needed)',
        sender_name='IT Operations', sender_email='itops@cyberaware.local',
        body='<p>Hi all,</p><p>We will perform routine maintenance on internal '
             'systems this Saturday 22:00-23:00. Some services may briefly restart. '
             'No action is required and you do not need to log in or click '
             'anything.</p><p>&mdash; IT Operations</p>',
        red_flags='', difficulty='easy', is_phishing=False, created_by=trainer.id,
    )
    db.session.add_all([c1, c2, c3, c4, c5, c6])
    db.session.commit()

    campaigns = [c1, c2, c3, c4, c5, c6]

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
    respond(emp1, c5, 'phishing')      # correct
    respond(emp2, c1, 'legitimate')    # incorrect (it was phishing)
    respond(emp2, c2, 'phishing')      # correct
    respond(emp3, c3, 'phishing')      # incorrect (it was legitimate)
    respond(emp3, c6, 'legitimate')    # correct
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

    print('Seed complete: 5 users, %d modules, %d questions, %d campaigns.'
          % (TrainingModule.query.count(), QuizQuestion.query.count(),
             PhishingCampaign.query.count()))


if __name__ == '__main__':
    seed()
