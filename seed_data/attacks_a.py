"""CyberAware training content: attack-focused modules (set A).

Defines MODULES: a list of 5 module dicts (orders 7-11) following the
content/quiz contract. Educational and defensive content only.
"""

# ---------------------------------------------------------------------------
# Module 7 - Phishing & Spear Phishing
# ---------------------------------------------------------------------------

PHISHING_CONTENT = """
<section>
  <h2>Phishing &amp; Spear Phishing</h2>
  <p>Phishing is a social-engineering attack that uses fraudulent messages to
  trick people into revealing credentials, sending money, or installing malware.
  It remains the single most common entry point for breaches. This module
  explains how phishing works, how to spot the red flags, and how to respond.</p>
</section>

<section>
  <h3>1. How phishing works</h3>
  <p>Attackers impersonate a trusted brand, colleague, or authority and create a
  reason to act quickly. The message drives the victim to a fake login page, a
  malicious attachment, or a request to wire funds or buy gift cards. Because the
  message exploits trust and urgency, it often bypasses technical controls.</p>
  <ul>
    <li><strong>Bulk phishing</strong> blasts the same lure to thousands of people.</li>
    <li><strong>Spear phishing</strong> is researched and tailored to one person
    or team, referencing real names, projects, or vendors.</li>
    <li><strong>Whaling</strong> targets executives and other high-value roles.</li>
    <li><strong>Smishing</strong> and <strong>vishing</strong> use SMS and voice
    calls instead of email.</li>
  </ul>
</section>

<section>
  <h3>2. Real-world red flags</h3>
  <ul>
    <li>Urgency or threats ("your account will be closed in 24 hours").</li>
    <li>A mismatch between the display name and the real sending domain.</li>
    <li>Links whose hover target differs from the visible text, or look-alike
    domains (rn for m, paypa1, micros0ft).</li>
    <li>Unexpected attachments, especially .htm, .iso, .zip, or macro documents.</li>
    <li>Requests to bypass normal process: secrecy, gift cards, or wire changes.</li>
    <li>Generic greetings, odd grammar, or a reply-to that differs from the sender.</li>
  </ul>
</section>

<section>
  <h3>3. Anatomy of a spear-phishing lure</h3>
  <table class="table">
    <thead><tr><th>Element</th><th>What the attacker does</th><th>Defender check</th></tr></thead>
    <tbody>
      <tr><td>Sender</td><td>Spoofs or look-alikes a known contact</td><td>Inspect full address and domain</td></tr>
      <tr><td>Pretext</td><td>References a real project or invoice</td><td>Verify via a second channel</td></tr>
      <tr><td>Payload</td><td>Fake portal or malicious file</td><td>Never enter creds from a link</td></tr>
      <tr><td>Urgency</td><td>Deadline or authority pressure</td><td>Slow down; escalate if unsure</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>4. Spotting a spoofed link</h3>
  <p>The visible text can say anything; what matters is the real destination and
  domain. Compare the apparent brand to the actual registrable domain.</p>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>Visible: https://secure-bank.com/login
Real:    https://secure-bank.com.verify-id&lt;dot&gt;ru/login
(the true domain is verify-id.ru, not the bank)</code></pre>
    <pre class="code-block secure"><code>Visible: https://www.yourbank.com
Real:    https://www.yourbank.com/login
(registrable domain matches the brand you expect)</code></pre>
  </div>
</section>

<section>
  <h3>5. Defenses</h3>
  <ul>
    <li>Enable phishing-resistant MFA (FIDO2/passkeys) so stolen passwords alone fail.</li>
    <li>Deploy SPF, DKIM, and DMARC to reduce domain spoofing.</li>
    <li>Verify money or credential requests out-of-band using known contacts.</li>
    <li>Report suspicious mail with the report button; do not just delete it.</li>
    <li>Use a password manager: it will not autofill on look-alike domains.</li>
  </ul>
</section>

<section class="exercise" data-exercise="scenario">
  <h3>Scenario: How should you respond?</h3>
  <p><em>You get an email that looks like it is from your CEO asking you to buy
  five $200 gift cards and send the codes, marked urgent and confidential.</em></p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="unsafe">Buy the cards quietly to avoid disappointing the CEO</button>
    <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Verify the request through a known phone number or in person before acting</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""

PHISHING_QUESTIONS = [
    ("What is phishing?",
     "A method to encrypt email in transit", "A fraudulent message that tricks people into revealing data or money",
     "A type of firewall rule", "A backup strategy", "B",
     "Phishing uses deceptive messages impersonating trusted parties to steal credentials, money, or deliver malware."),
    ("How does spear phishing differ from ordinary bulk phishing?",
     "It is sent only by SMS", "It targets a specific person with tailored, researched details",
     "It never contains links", "It only targets banks", "B",
     "Spear phishing is customized to an individual or team using real names and context, making it more convincing."),
    ("Which term describes phishing aimed specifically at high-level executives?",
     "Smishing", "Vishing", "Whaling", "Pharming", "C",
     "Whaling targets executives and other high-value individuals who can authorize large transfers or access."),
    ("'Smishing' refers to phishing delivered via:",
     "SMS text messages", "Voice phone calls", "QR codes only", "Printed letters", "A",
     "Smishing is phishing conducted through SMS or other text messaging."),
    ("'Vishing' is phishing conducted over:",
     "Email attachments", "Voice phone calls", "Wi-Fi networks", "Social media posts", "B",
     "Vishing uses voice calls, often spoofing caller ID, to pressure victims into revealing information."),
    ("Which of these is a classic red flag of a phishing email?",
     "A digitally signed message from a known colleague", "An artificial sense of urgency or threat",
     "A plain-text newsletter you subscribed to", "An internal calendar invite", "B",
     "Urgency and threats pressure victims to act before they think, a hallmark of phishing."),
    ("You hover over a link and the destination domain does not match the brand shown. You should:",
     "Click it to investigate", "Forward it to friends", "Not click and report the message", "Reply asking if it is real", "C",
     "A mismatched destination is a strong phishing indicator; do not click and report it through proper channels."),
    ("Which authentication method best resists phishing even if your password is stolen?",
     "SMS one-time codes", "Security questions", "FIDO2 / passkeys (phishing-resistant MFA)", "A longer password", "C",
     "FIDO2/passkeys are bound to the legitimate site origin, so they do not work on attacker look-alike pages."),
    ("What is the safest action when an email asks you to log in via a provided link?",
     "Enter your credentials quickly", "Navigate to the site yourself using a known URL or bookmark",
     "Reply with your username only", "Disable your antivirus first", "B",
     "Typing the known address or using a bookmark avoids attacker-controlled look-alike login pages."),
    ("Look-alike domains such as 'paypa1.com' or 'micros0ft.com' are used to:",
     "Improve email deliverability", "Trick users into trusting a fake site", "Speed up DNS", "Encrypt traffic", "B",
     "Homoglyph and typosquatted domains mimic real brands to deceive victims into trusting fraudulent pages."),
    ("Which email authentication standards help reduce domain spoofing?",
     "TLS, SSH, and IPSec", "SPF, DKIM, and DMARC", "RAID, NAS, and SAN", "HTTP, FTP, and SMTP", "B",
     "SPF, DKIM, and DMARC let receiving servers verify that mail genuinely comes from the claimed domain."),
    ("A 'business email compromise' gift-card request from your boss should first be:",
     "Acted on immediately and secretly", "Ignored entirely with no follow-up",
     "Verified out-of-band via a known phone number", "Paid from petty cash", "C",
     "Out-of-band verification using a trusted contact defeats impersonation and BEC fraud."),
    ("Why are unexpected attachments like .iso, .zip, or macro documents risky?",
     "They are always too large to open", "They can carry malware that runs when opened",
     "They cannot be scanned", "They expire quickly", "B",
     "These file types are common malware delivery vehicles, often using scripts or macros to execute code."),
    ("Pharming differs from phishing because it:",
     "Always uses phone calls", "Redirects victims via DNS or host-file tampering rather than a lure link",
     "Targets only printers", "Requires physical access", "B",
     "Pharming poisons DNS or hosts files so users are silently sent to fake sites even with correct URLs."),
    ("A password manager helps against phishing because it:",
     "Types passwords faster", "Will not autofill credentials on a look-alike domain",
     "Encrypts the network", "Blocks all email", "B",
     "Password managers match the stored site's exact domain and refuse to autofill on fraudulent look-alikes."),
    ("Which greeting is more consistent with a phishing email?",
     "Hi Priya, about the Q3 audit you raised", "Dear Valued Customer",
     "Hi team, see Friday's notes", "Hello Sam, lunch at noon?", "B",
     "Generic greetings like 'Dear Valued Customer' suggest a mass, impersonal phishing campaign."),
    ("The best response to a suspected phishing email at work is to:",
     "Delete it silently", "Click links to confirm it is fake", "Use the report-phishing button so security can act", "Mark it as spam only", "C",
     "Reporting alerts the security team to investigate, warn others, and block the campaign."),
    ("Why do attackers create a sense of urgency in phishing messages?",
     "To comply with regulations", "To reduce the victim's critical thinking and prompt fast action",
     "To improve grammar", "To pass spam filters", "B",
     "Urgency triggers emotional, reflexive responses, lowering the chance the target verifies the request."),
    ("Clone phishing typically involves:",
     "Cloning a server", "Copying a legitimate prior email and swapping in a malicious link or attachment",
     "Duplicating a hard drive", "Spoofing only the subject line", "B",
     "Clone phishing replicates a real, expected message but replaces content with malicious payloads."),
    ("What does DMARC add on top of SPF and DKIM?",
     "Encryption of message bodies", "A policy telling receivers what to do with failing mail and where to send reports",
     "Faster delivery", "Automatic translation", "B",
     "DMARC defines handling policy (none/quarantine/reject) for messages failing alignment and enables reporting."),
    ("A QR code in an email leading to a login page (quishing) is risky because:",
     "QR codes cannot contain URLs", "It can hide a malicious URL and bypass link scanners",
     "It only works on paper", "It encrypts your phone", "B",
     "Quishing hides the destination in an image, evading URL filters and pushing the user to a fake site."),
    ("If you accidentally entered your password on a phishing site, you should first:",
     "Wait to see if anything happens", "Change the password and report it immediately",
     "Reboot the computer only", "Email the attacker", "B",
     "Promptly changing the password and reporting limits the window an attacker can use the stolen credentials."),
    ("Why is verifying via a 'second channel' effective against phishing?",
     "It is faster", "The attacker usually does not control the other channel", "It encrypts the request", "It is required by law", "B",
     "Confirming through an independent, trusted channel exposes impersonation the attacker cannot replicate."),
    ("Which is a sign a 'sender' address may be spoofed?",
     "It uses your company domain exactly", "The reply-to differs from the from address and points elsewhere",
     "It has a digital signature", "It arrived during business hours", "B",
     "A mismatched reply-to that routes responses to an unrelated address is a common spoofing trick."),
    ("Credential-harvesting phishing pages are designed to:",
     "Speed up your login", "Capture the username and password you type", "Update your software", "Test your network", "B",
     "Fake login portals exist solely to record the credentials victims enter."),
    ("Security awareness phishing simulations are used to:",
     "Punish employees publicly", "Train and measure staff resilience to real phishing",
     "Collect customer data", "Replace MFA", "B",
     "Simulations safely build recognition skills and provide metrics to guide further training."),
    ("Which practice most reduces the damage if phishing steals one password?",
     "Reusing passwords for convenience", "Using unique passwords per site plus MFA",
     "Writing passwords on sticky notes", "Sharing logins with the team", "B",
     "Unique passwords plus MFA contain the blast radius so one stolen credential cannot unlock everything."),
    ("An email from 'IT Support' asks for your password to 'fix your mailbox.' You should:",
     "Provide it to avoid downtime", "Refuse; legitimate IT never needs your password",
     "Send a hint instead", "Give a temporary one", "B",
     "Legitimate IT can reset or access systems administratively and will never ask for your password."),
    ("Why is hovering over a link before clicking recommended?",
     "It loads the page faster", "It reveals the true destination URL without visiting it",
     "It encrypts the link", "It reports the sender", "B",
     "Hovering shows the real target so you can spot mismatches before any navigation occurs."),
    ("The strongest overall posture against phishing combines:",
     "Only spam filters", "Only employee training", "Layered controls: training, MFA, email authentication, and reporting", "Only antivirus", "C",
     "No single control stops phishing; layered technical and human defenses together provide resilience."),
]


# ---------------------------------------------------------------------------
# Module 8 - Ransomware
# ---------------------------------------------------------------------------

RANSOMWARE_CONTENT = """
<section>
  <h2>Ransomware</h2>
  <p>Ransomware is malware that encrypts files or whole systems and demands
  payment for a decryption key. Modern campaigns add data theft and extortion,
  threatening to publish stolen data if the victim refuses to pay. This module
  covers how ransomware spreads, what to watch for, and how to prepare.</p>
</section>

<section>
  <h3>1. How ransomware works</h3>
  <p>A typical attack moves through stages: initial access (phishing, stolen
  credentials, or an exploited vulnerability), establishing persistence, moving
  laterally, stealing data, then deploying the encryptor. Attackers often disable
  backups and security tools first to maximize pressure.</p>
  <ul>
    <li><strong>Encryption</strong> scrambles files; only the attacker's key restores them.</li>
    <li><strong>Double extortion</strong> also threatens to leak stolen data.</li>
    <li><strong>Ransomware-as-a-Service (RaaS)</strong> rents kits to affiliates.</li>
  </ul>
</section>

<section>
  <h3>2. Common entry points and warning signs</h3>
  <ul>
    <li>Phishing emails with malicious attachments or links.</li>
    <li>Exposed or weakly protected remote access (RDP, VPN) and unpatched servers.</li>
    <li>Reused or stolen credentials and missing MFA.</li>
    <li>Warning signs: mass file renames, ransom notes, disabled antivirus, sudden
    spikes in CPU/disk activity, or accounts logging in at odd hours.</li>
  </ul>
</section>

<section>
  <h3>3. Why paying is discouraged</h3>
  <table class="table">
    <thead><tr><th>Concern</th><th>Reality</th></tr></thead>
    <tbody>
      <tr><td>Recovery</td><td>Decryptors may be buggy or incomplete; some data stays lost.</td></tr>
      <tr><td>Repeat attacks</td><td>Paying marks you as willing, inviting return visits.</td></tr>
      <tr><td>Funding crime</td><td>Payment funds further attacks and may breach sanctions.</td></tr>
      <tr><td>Data leak</td><td>Stolen data may be sold or leaked even after payment.</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>4. The 3-2-1 backup rule</h3>
  <p>Reliable, tested backups are the most important ransomware defense. Keep at
  least three copies of data, on two different media, with one copy offline or
  immutable (air-gapped) so the attacker cannot encrypt it.</p>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>Backup target mounted 24/7 with write access
-&gt; ransomware encrypts the backups too</code></pre>
    <pre class="code-block secure"><code>Offline / immutable backups + tested restores
-&gt; clean recovery without paying</code></pre>
  </div>
</section>

<section>
  <h3>5. Defenses</h3>
  <ul>
    <li>Maintain offline, immutable, regularly tested backups.</li>
    <li>Patch promptly and reduce internet-exposed services.</li>
    <li>Enforce MFA and least privilege; segment the network.</li>
    <li>Deploy EDR to detect lateral movement and encryption behavior early.</li>
    <li>Have an incident response plan: isolate, preserve evidence, notify.</li>
  </ul>
</section>

<section class="exercise" data-exercise="threat">
  <h3>Which of these strengthen ransomware resilience? Select all that apply.</h3>
  <div class="exercise-options">
    <label><input type="checkbox" data-answer="backups" data-correct="true"> Offline, immutable, tested backups</label>
    <label><input type="checkbox" data-answer="mfa" data-correct="true"> Enforcing MFA on remote access</label>
    <label><input type="checkbox" data-answer="payfirst"> Pre-paying attackers as insurance</label>
    <label><input type="checkbox" data-answer="patch" data-correct="true"> Patching internet-facing systems promptly</label>
    <label><input type="checkbox" data-answer="sharedadmin"> Sharing one admin account team-wide</label>
  </div>
  <button type="button" class="btn btn-primary" data-action="check">Check</button>
  <p class="exercise-feedback" hidden></p>
</section>
"""

RANSOMWARE_QUESTIONS = [
    ("What does ransomware primarily do to a victim's data?",
     "Speeds up access to it", "Encrypts or locks it and demands payment to restore access",
     "Compresses it to save space", "Backs it up to the cloud", "B",
     "Ransomware encrypts or locks data and demands a ransom for the decryption key."),
    ("What is 'double extortion' ransomware?",
     "Charging twice the normal ransom", "Encrypting data and also threatening to leak stolen copies",
     "Attacking two companies at once", "Using two encryption keys", "B",
     "Double extortion pairs encryption with the threat to publish exfiltrated data, increasing pressure to pay."),
    ("What is the single most important defense for recovering from ransomware?",
     "Antivirus signatures", "Reliable, offline, tested backups", "A faster internet connection", "Longer passwords", "B",
     "Clean offline backups let an organization restore systems without paying the attacker."),
    ("The '3-2-1' backup rule recommends:",
     "3 passwords, 2 admins, 1 firewall", "3 copies, on 2 media types, with 1 offline/immutable",
     "3 servers in one rack", "3 daily reboots", "B",
     "3-2-1 means three copies on two media with one kept offline or immutable, surviving an attack on production."),
    ("Why is paying the ransom generally discouraged?",
     "It is always cheaper to pay", "It may fund crime, invite repeat attacks, and not guarantee recovery",
     "Decryptors are always perfect", "It is required by law", "B",
     "Payment funds criminals, marks you as a willing target, and provides no guarantee of full, clean recovery."),
    ("'Ransomware-as-a-Service' (RaaS) refers to:",
     "A cloud backup product", "Criminal kits rented to affiliates who carry out attacks",
     "A government recovery service", "An antivirus subscription", "B",
     "RaaS lets developers rent ransomware to affiliates, lowering the skill needed to launch attacks."),
    ("Which is a common initial access vector for ransomware?",
     "Phishing emails and exposed remote access", "Properly patched servers", "Air-gapped backups", "Disabled USB ports", "A",
     "Phishing and weakly protected internet-facing remote access are leading ransomware entry points."),
    ("Network segmentation helps against ransomware by:",
     "Making files load faster", "Limiting how far an infection can spread laterally",
     "Encrypting the internet", "Replacing backups", "B",
     "Segmentation contains an outbreak to part of the network, slowing or stopping lateral spread."),
    ("Why do attackers try to disable or delete backups before encrypting?",
     "To save disk space", "To remove the victim's ability to recover without paying",
     "To improve performance", "To comply with policy", "B",
     "Destroying backups maximizes pressure by eliminating the cheapest recovery option."),
    ("What is a strong sign a ransomware attack is underway?",
     "Mass file renaming with new extensions and ransom notes appearing", "Faster boot times",
     "Lower CPU usage", "Fewer emails", "A",
     "Sudden mass renaming, unfamiliar extensions, and ransom notes are hallmark indicators of active encryption."),
    ("'Immutable' backups are valuable because they:",
     "Can be edited quickly", "Cannot be altered or deleted for a set period, even by admins",
     "Are stored only in RAM", "Compress better", "B",
     "Immutability prevents attackers (or compromised accounts) from encrypting or deleting backup copies."),
    ("Multi-factor authentication reduces ransomware risk mainly by:",
     "Encrypting files", "Stopping attackers who only have a stolen password",
     "Speeding up logins", "Blocking all email", "B",
     "MFA prevents account takeover from stolen credentials, closing a major initial-access path."),
    ("Endpoint Detection and Response (EDR) helps by:",
     "Replacing backups", "Detecting suspicious behavior like lateral movement and mass encryption early",
     "Paying ransoms automatically", "Disabling MFA", "B",
     "EDR spots behavioral indicators of intrusion and encryption, enabling faster containment."),
    ("The first technical step when ransomware is detected on a host is usually to:",
     "Reboot it repeatedly", "Isolate it from the network to stop spread",
     "Pay the ransom", "Delete all logs", "B",
     "Isolating the affected host limits lateral spread while responders investigate."),
    ("Why should logs be preserved during a ransomware incident?",
     "They speed up encryption", "They support investigation, scope, and recovery decisions",
     "They are not useful", "They auto-pay the ransom", "B",
     "Logs help responders understand entry, spread, and data theft, guiding recovery and reporting."),
    ("Keeping a backup mounted with constant write access is risky because:",
     "It is too slow", "Ransomware can encrypt the connected backups too",
     "It uses no power", "It improves security", "B",
     "Always-connected, writable backups can be encrypted alongside production data, defeating recovery."),
    ("'Lateral movement' in a ransomware attack means:",
     "Moving the server physically", "Spreading from the first foothold to other systems",
     "Rotating backups", "Changing file names", "B",
     "Attackers pivot from the initial host to additional systems to maximize impact before encrypting."),
    ("Which practice most reduces internet-exposed ransomware entry points?",
     "Opening RDP to the internet", "Closing or protecting remote services behind VPN/MFA and patching them",
     "Disabling backups", "Sharing admin passwords", "B",
     "Removing or hardening exposed remote services cuts off a primary ransomware access route."),
    ("Least privilege limits ransomware by:",
     "Giving everyone admin rights", "Restricting accounts so a compromise can reach fewer systems and files",
     "Encrypting nothing", "Disabling MFA", "B",
     "When accounts have only needed access, a compromised one can damage and spread far less."),
    ("Testing your backups by performing restores is important because:",
     "It deletes old data", "Untested backups may be incomplete or corrupt when you need them",
     "It speeds up the network", "It is required to pay ransoms", "B",
     "Only verified restores prove backups will actually recover systems during an incident."),
    ("A ransom note demanding cryptocurrency typically indicates:",
     "A hardware failure", "An active ransomware extortion attempt", "A software update", "A backup completion", "B",
     "Cryptocurrency ransom demands are characteristic of ransomware extortion."),
    ("Why is prompt patching a key ransomware defense?",
     "Patches encrypt files", "Many attacks exploit known, unpatched vulnerabilities for access or spread",
     "Patches slow recovery", "Patching is optional", "B",
     "Attackers frequently weaponize known vulnerabilities; timely patching removes those openings."),
    ("Even after paying, organizations may still suffer because:",
     "Decryptors always work perfectly", "Stolen data can still be leaked or sold and decryption may be incomplete",
     "The attack never returns", "Backups are restored automatically", "B",
     "Payment does not guarantee data is deleted or that decryption fully restores all files."),
    ("Which combination best supports ransomware resilience?",
     "Backups, MFA, patching, segmentation, and an IR plan", "Only antivirus",
     "Only a firewall", "Only employee monitoring", "A",
     "Layered controls plus tested backups and a response plan provide the strongest resilience."),
    ("An incident response (IR) plan for ransomware should define:",
     "Only who pays", "Roles, isolation steps, communications, and recovery procedures",
     "Nothing in advance", "Only the ransom amount", "B",
     "A good IR plan pre-defines responsibilities and steps so the team acts quickly and correctly under stress."),
    ("Why is reporting ransomware to authorities encouraged?",
     "It pays the ransom", "It aids investigations, may provide decryptors, and meets legal obligations",
     "It is illegal", "It speeds encryption", "B",
     "Reporting can unlock investigative help, known decryptors, and satisfies regulatory requirements."),
    ("Disabling unneeded macros in office documents helps because:",
     "Macros speed typing", "Malicious macros are a common ransomware delivery mechanism",
     "It improves graphics", "Macros cannot run code", "B",
     "Blocking macros from the internet removes a frequent path used to drop ransomware payloads."),
    ("Application allowlisting reduces ransomware risk by:",
     "Allowing any program to run", "Permitting only approved software to execute",
     "Disabling backups", "Encrypting the network", "B",
     "Allowlisting blocks unapproved executables, stopping many ransomware binaries from running."),
    ("A 'data exfiltration' phase before encryption means attackers:",
     "Improved your backups", "Stole copies of data to enable extortion",
     "Defragmented the disk", "Updated the OS", "B",
     "Exfiltration steals data so attackers can threaten to publish it, enabling double extortion."),
    ("The safest mindset toward ransomware is:",
     "Assume it cannot happen here", "Assume it can happen and prepare layered prevention plus recovery",
     "Rely only on luck", "Pay quickly to avoid trouble", "B",
     "Assuming breach and preparing prevention, detection, and tested recovery gives the best outcome."),
]


# ---------------------------------------------------------------------------
# Module 9 - Malware & Spyware
# ---------------------------------------------------------------------------

MALWARE_CONTENT = """
<section>
  <h2>Malware &amp; Spyware</h2>
  <p>Malware ("malicious software") is any program designed to harm, exploit, or
  spy on a system or user. Spyware is a category that secretly gathers
  information. This module covers the main malware families, how they infect
  devices, the signs of infection, and how to defend against them.</p>
</section>

<section>
  <h3>1. Malware families</h3>
  <ul>
    <li><strong>Virus</strong>: attaches to a file and spreads when that file runs.</li>
    <li><strong>Worm</strong>: self-replicates across networks without user action.</li>
    <li><strong>Trojan</strong>: disguises itself as legitimate software.</li>
    <li><strong>Spyware</strong>: secretly collects data (browsing, files, messages).</li>
    <li><strong>Keylogger</strong>: records keystrokes to steal credentials.</li>
    <li><strong>Rootkit</strong>: hides deep in the system to evade detection.</li>
    <li><strong>Adware</strong>: floods the user with unwanted ads, often bundled.</li>
    <li><strong>Botnet client</strong>: enrolls the device into an attacker network.</li>
  </ul>
</section>

<section>
  <h3>2. How devices get infected</h3>
  <ul>
    <li>Opening malicious email attachments or links.</li>
    <li>Downloading cracked or "free" software and fake updates.</li>
    <li>Drive-by downloads from compromised websites.</li>
    <li>Plugging in untrusted USB drives.</li>
    <li>Installing apps from outside official stores (sideloading).</li>
  </ul>
</section>

<section>
  <h3>3. Signs of infection</h3>
  <table class="table">
    <thead><tr><th>Symptom</th><th>Possible cause</th></tr></thead>
    <tbody>
      <tr><td>Sudden slowness / overheating</td><td>Cryptominer or background malware</td></tr>
      <tr><td>Pop-ups and browser redirects</td><td>Adware or browser hijacker</td></tr>
      <tr><td>Unknown new programs or processes</td><td>Trojan or backdoor</td></tr>
      <tr><td>Disabled antivirus or settings locked</td><td>Rootkit or active malware</td></tr>
      <tr><td>Unexpected data usage</td><td>Spyware exfiltrating data</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>4. Trusted vs. risky installs</h3>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>Source: "free-photoshop-crack&lt;dot&gt;xyz/setup.exe"
Prompt: "Disable antivirus to install"
-&gt; classic trojan / spyware bundle</code></pre>
    <pre class="code-block secure"><code>Source: official vendor site or app store
Signature: valid publisher, checksum verified
-&gt; lower risk, verifiable integrity</code></pre>
  </div>
</section>

<section>
  <h3>5. Defenses</h3>
  <ul>
    <li>Install software only from official, trusted sources and verify signatures.</li>
    <li>Keep the OS, browser, and apps patched; enable automatic updates.</li>
    <li>Run reputable endpoint protection / EDR and keep it enabled.</li>
    <li>Use least-privilege accounts so malware cannot easily gain admin rights.</li>
    <li>Do not plug in unknown USB devices; disable autorun.</li>
    <li>Back up data so you can recover from a destructive infection.</li>
  </ul>
</section>

<section class="exercise" data-exercise="code-review">
  <h3>Quick check: secure or risky behavior?</h3>
  <pre class="code-block"><code>A pop-up says your PC is infected and tells you to
call a number and install "PCFixerPro" from a link.</code></pre>
  <p>Click your answer:</p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="secure">Secure</button>
    <button type="button" class="btn btn-secondary" data-answer="vulnerable" data-correct="true">Vulnerable</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""

MALWARE_QUESTIONS = [
    ("What does the term 'malware' mean?",
     "Hardware failure", "Any software designed to harm, exploit, or spy on systems",
     "A type of firewall", "A backup format", "B",
     "Malware is a general term for malicious software including viruses, worms, trojans, and spyware."),
    ("What primarily distinguishes a worm from a virus?",
     "A worm self-replicates across networks without needing a host file or user action", "A worm is hardware",
     "A worm cannot spread", "A worm only affects printers", "A",
     "Worms self-propagate over networks automatically, whereas viruses attach to files and need execution."),
    ("A Trojan is dangerous because it:",
     "Announces itself loudly", "Disguises itself as legitimate software to trick users into running it",
     "Cannot run code", "Only displays ads", "B",
     "Trojans masquerade as useful programs so victims install them, then carry out hidden malicious actions."),
    ("Spyware is software that:",
     "Speeds up the computer", "Secretly collects information about the user or system",
     "Encrypts backups", "Blocks all ads", "B",
     "Spyware covertly gathers data such as browsing habits, files, or messages and sends it to attackers."),
    ("A keylogger steals credentials by:",
     "Recording keystrokes the user types", "Encrypting the keyboard", "Disabling the mouse", "Backing up files", "A",
     "Keyloggers capture typed input, including usernames and passwords."),
    ("A rootkit is especially dangerous because it:",
     "Is easy to see", "Hides deep in the system to evade detection and maintain access",
     "Only shows pop-ups", "Improves performance", "B",
     "Rootkits conceal themselves and other malware at a low level, making detection and removal hard."),
    ("Adware most commonly:",
     "Encrypts files for ransom", "Floods the user with unwanted ads and may track behavior",
     "Self-replicates over networks", "Patches the OS", "B",
     "Adware bombards users with ads and often bundles tracking, sometimes arriving with other unwanted software."),
    ("A device enrolled into a 'botnet' is:",
     "Faster and safer", "Remotely controlled by an attacker to perform tasks like DDoS or spam",
     "Disconnected from networks", "Automatically patched", "B",
     "Botnet clients take commands from an attacker, often joining large-scale attacks or spam campaigns."),
    ("Which is a common malware infection vector?",
     "Opening malicious attachments or downloading cracked software", "Reading a printed book",
     "Using a wired keyboard", "Restarting the PC", "A",
     "Malicious attachments, links, and pirated or fake software are frequent infection routes."),
    ("A 'drive-by download' infects a user when they:",
     "Manually compile code", "Merely visit a compromised or malicious website",
     "Print a document", "Charge their phone", "B",
     "Drive-by downloads exploit the browser or plugins to install malware just from visiting a page."),
    ("Why are unknown USB drives a security risk?",
     "They hold too little data", "They can auto-deliver malware when plugged in",
     "They are too slow", "They cannot store files", "B",
     "Untrusted USB devices can carry malware that runs on insertion, especially if autorun is enabled."),
    ("Sideloading apps from outside official stores increases risk because:",
     "Apps load faster", "They bypass store vetting and may contain malware",
     "They are always signed", "They use less battery", "B",
     "Unvetted apps skip store security review, raising the chance of hidden malicious code."),
    ("A reliable way to lower the impact of malware that does run is to:",
     "Use an admin account for everything", "Use least-privilege standard accounts for daily work",
     "Disable backups", "Turn off updates", "B",
     "Running as a standard user limits malware's ability to gain system-wide control."),
    ("Which symptom may indicate a cryptominer infection?",
     "The PC is faster than ever", "Sudden high CPU usage, slowness, and overheating",
     "More free disk space", "Quieter fans", "B",
     "Cryptominers consume CPU/GPU heavily, causing slowdowns, heat, and noisy fans."),
    ("Frequent browser redirects and pop-ups most likely indicate:",
     "A faster connection", "Adware or a browser hijacker", "A new firewall", "Successful patching", "B",
     "Unwanted redirects and pop-ups are classic signs of adware or browser-hijacking malware."),
    ("If antivirus is unexpectedly disabled and settings are locked, you should suspect:",
     "Normal behavior", "Active malware or a rootkit interfering with defenses",
     "A faster system", "A successful backup", "B",
     "Malware often disables security tools to avoid detection and removal."),
    ("Verifying a download's digital signature or checksum helps confirm:",
     "The file is large", "The file is genuine and unmodified",
     "The internet is fast", "The OS is old", "B",
     "Signatures and checksums verify integrity and publisher, reducing the risk of tampered installers."),
    ("A pop-up claiming 'Your PC is infected, call this number' is usually:",
     "Helpful official support", "A scareware/tech-support scam aiming to install malware or steal money",
     "A system update", "A backup notice", "B",
     "Such pop-ups are scareware designed to panic users into installing malware or paying fake support."),
    ("Keeping the OS, browser, and apps patched reduces malware because it:",
     "Adds more ads", "Closes vulnerabilities that malware exploits",
     "Slows the computer", "Deletes files", "B",
     "Patches remove the security holes that drive-by and exploit-based malware rely on."),
    ("A 'backdoor' installed by malware provides:",
     "Faster boot times", "Persistent unauthorized remote access for the attacker",
     "Automatic patching", "Better graphics", "B",
     "Backdoors let attackers return to and control the system whenever they wish."),
    ("Why is downloading 'cracked' paid software risky?",
     "It is always safe", "Cracks frequently bundle trojans, spyware, or miners",
     "It is faster", "It is signed by vendors", "B",
     "Pirated software is a common malware carrier, often hiding trojans or spyware in the crack."),
    ("Endpoint protection / antivirus primarily helps by:",
     "Encrypting the network", "Detecting, blocking, and removing known and suspicious malicious code",
     "Replacing backups", "Disabling MFA", "B",
     "Endpoint protection identifies and stops malware through signatures and behavioral detection."),
    ("Disabling autorun on removable media helps because it:",
     "Speeds up the USB", "Prevents malware from launching automatically on insertion",
     "Adds storage", "Encrypts the drive", "B",
     "Without autorun, malware on a USB cannot execute simply by plugging the device in."),
    ("Fileless malware is harder to detect because it:",
     "Writes large files to disk", "Runs in memory using legitimate system tools, leaving little on disk",
     "Is always visible", "Cannot persist", "B",
     "Fileless malware abuses trusted tools and memory, leaving few traditional artifacts for scanners."),
    ("A good first action if you suspect a work device is infected is to:",
     "Keep using it normally", "Disconnect it from the network and report to IT/security",
     "Plug in more USBs", "Disable backups", "B",
     "Disconnecting limits spread and data theft while professionals investigate and remediate."),
    ("Why are regular backups part of malware defense?",
     "They prevent all infections", "They let you recover data after destructive or persistent infections",
     "They speed downloads", "They block ads", "B",
     "Backups enable recovery when malware corrupts, encrypts, or forces a clean rebuild."),
    ("A 'polymorphic' virus evades detection by:",
     "Staying identical every copy", "Changing its code/signature with each infection",
     "Refusing to spread", "Showing pop-ups", "B",
     "Polymorphic malware mutates its code so simple signature matching fails to catch every variant."),
    ("Which behavior most reduces spyware risk on a phone?",
     "Granting every app all permissions", "Installing apps only from official stores and reviewing permissions",
     "Jailbreaking the device", "Disabling updates", "B",
     "Official stores and careful permission review limit spyware that abuses access to data and sensors."),
    ("A command-and-control (C2) channel is used by malware to:",
     "Update the BIOS", "Receive instructions from and send data to the attacker",
     "Defragment disks", "Improve graphics", "B",
     "C2 lets attackers control infected hosts and exfiltrate stolen information."),
    ("The strongest everyday malware defense combines:",
     "Only one antivirus scan a year", "Trusted sources, patching, least privilege, endpoint protection, and backups",
     "Only a firewall", "Only strong passwords", "B",
     "Layered habits and controls together prevent, detect, and recover from malware far better than any one measure."),
]


# ---------------------------------------------------------------------------
# Module 10 - DDoS Attacks
# ---------------------------------------------------------------------------

DDOS_CONTENT = """
<section>
  <h2>DDoS Attacks</h2>
  <p>A Distributed Denial-of-Service (DDoS) attack floods a target with traffic
  or requests from many sources at once, exhausting its capacity so legitimate
  users cannot get through. Unlike a breach, the goal is disruption rather than
  data theft. This module explains the attack types and how to stay resilient.</p>
</section>

<section>
  <h3>1. DoS vs. DDoS</h3>
  <p>A Denial-of-Service (DoS) attack comes from a single source; a Distributed
  Denial-of-Service (DDoS) attack uses many sources at once, often a botnet of
  compromised devices, making it far harder to block and far larger in scale.</p>
</section>

<section>
  <h3>2. Categories of DDoS</h3>
  <table class="table">
    <thead><tr><th>Category</th><th>What it targets</th><th>Examples</th></tr></thead>
    <tbody>
      <tr><td>Volumetric</td><td>Bandwidth / pipe capacity</td><td>UDP/DNS/NTP amplification floods</td></tr>
      <tr><td>Protocol</td><td>Connection-state resources</td><td>SYN flood, fragmented packets</td></tr>
      <tr><td>Application-layer</td><td>App/server processing (Layer 7)</td><td>HTTP GET/POST floods</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>3. Amplification and reflection</h3>
  <p>Attackers abuse services that return a large response to a small request
  (amplification) and spoof the victim's address as the source (reflection), so
  the responses bombard the victim. Open DNS, NTP, and memcached servers have
  been abused this way to multiply attack volume.</p>
</section>

<section>
  <h3>4. Warning signs and impact</h3>
  <ul>
    <li>Sudden, unexplained spikes in traffic from many IPs or regions.</li>
    <li>A specific service slowing or timing out while infrastructure looks healthy.</li>
    <li>Traffic patterns that repeat or target one URL or endpoint.</li>
    <li>Impact: downtime, lost revenue, reputational harm, and sometimes a
    smokescreen to distract responders from another intrusion.</li>
  </ul>
</section>

<section>
  <h3>5. Defenses</h3>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>Single origin server, no rate limits,
no upstream scrubbing -&gt; easily overwhelmed</code></pre>
    <pre class="code-block secure"><code>CDN + DDoS scrubbing, rate limiting,
autoscaling, and an upstream provider plan</code></pre>
  </div>
  <ul>
    <li>Use a CDN and a DDoS-mitigation/scrubbing service to absorb volume.</li>
    <li>Apply rate limiting, WAF rules, and traffic anomaly detection.</li>
    <li>Over-provision and autoscale critical capacity.</li>
    <li>Disable or secure services that can be abused for amplification.</li>
    <li>Prepare a response runbook with your ISP/upstream provider in advance.</li>
  </ul>
</section>

<section class="exercise" data-exercise="scenario">
  <h3>Scenario: How should you respond?</h3>
  <p><em>Your public website suddenly becomes unreachable under a massive traffic
  flood from thousands of IPs around the world.</em></p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="unsafe">Email each source IP owner and wait for replies before acting</button>
    <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Activate your DDoS mitigation/CDN plan and engage your upstream provider</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""

DDOS_QUESTIONS = [
    ("What is the primary goal of a DDoS attack?",
     "To steal database records", "To make a service unavailable by overwhelming it",
     "To encrypt files for ransom", "To phish credentials", "B",
     "DDoS aims to exhaust a target's resources so legitimate users cannot access the service."),
    ("How does a DDoS differ from a DoS attack?",
     "DDoS uses many distributed sources, while DoS comes from a single source", "DDoS is always smaller",
     "DDoS targets only printers", "There is no difference", "A",
     "DDoS leverages many sources (often a botnet), making it larger and harder to block than single-source DoS."),
    ("A 'botnet' in the context of DDoS is:",
     "A backup network", "A network of compromised devices controlled to send attack traffic",
     "A firewall cluster", "A DNS server", "B",
     "Botnets are collections of infected devices that attackers command to flood a target simultaneously."),
    ("Volumetric DDoS attacks primarily aim to exhaust:",
     "CPU cache", "Network bandwidth / link capacity", "Disk space", "Printer queues", "B",
     "Volumetric attacks saturate the target's bandwidth so legitimate packets cannot get through."),
    ("A SYN flood is an example of which DDoS category?",
     "Application-layer", "Protocol/state-exhaustion attack", "Physical attack", "Volumetric only", "B",
     "SYN floods abuse the TCP handshake to exhaust connection-state resources, a protocol-layer attack."),
    ("An HTTP GET/POST flood targeting a web app is which type?",
     "Application-layer (Layer 7) attack", "Volumetric only", "Physical layer", "Link layer", "A",
     "Layer 7 floods send seemingly legitimate requests to exhaust application/server processing capacity."),
    ("What is DNS amplification?",
     "Compressing DNS records", "Sending small spoofed queries that trigger large responses to the victim",
     "Encrypting DNS", "Caching DNS faster", "B",
     "Amplification abuses services that return large replies to small requests, multiplying attack volume at the victim."),
    ("'Reflection' in DDoS means attackers:",
     "Bounce light off servers", "Spoof the victim's IP so responses are sent to the victim",
     "Mirror disks", "Reflect emails", "B",
     "Reflection forges the victim's address as the source so third-party servers flood the victim with replies."),
    ("Why are open/misconfigured DNS, NTP, or memcached servers a concern?",
     "They speed up the internet", "They can be abused as amplifiers in reflection attacks",
     "They block DDoS", "They store backups", "B",
     "Such open services return large responses and are exploited to amplify reflected DDoS traffic."),
    ("A Content Delivery Network (CDN) helps mitigate DDoS by:",
     "Encrypting files", "Distributing and absorbing traffic across many edge servers",
     "Deleting logs", "Slowing legitimate users", "B",
     "CDNs spread load across global edge nodes, absorbing and filtering attack traffic before it reaches the origin."),
    ("Rate limiting defends against DDoS by:",
     "Allowing unlimited requests", "Capping how many requests a source can make in a time window",
     "Encrypting traffic", "Disabling the server", "B",
     "Rate limiting throttles abusive sources, reducing the load floods can place on a service."),
    ("A DDoS 'scrubbing center' is used to:",
     "Clean hardware physically", "Filter malicious traffic upstream and pass clean traffic to the target",
     "Store backups", "Encrypt DNS", "B",
     "Scrubbing services inspect traffic and remove attack packets, forwarding only legitimate traffic."),
    ("Autoscaling helps absorb DDoS by:",
     "Reducing capacity", "Adding compute/bandwidth automatically as demand spikes",
     "Disabling the site", "Blocking all users", "B",
     "Autoscaling expands resources during surges, helping maintain availability under load (within limits)."),
    ("Why might attackers use a DDoS as a 'smokescreen'?",
     "To improve performance", "To distract responders while another intrusion occurs",
     "To back up data", "To patch systems", "B",
     "DDoS can divert security teams' attention from a concurrent breach or data theft."),
    ("A sudden traffic spike from many global IPs hitting one URL suggests:",
     "Normal usage", "A possible application-layer DDoS", "A backup job", "A patch rollout", "B",
     "Coordinated traffic from many sources focused on one endpoint is a classic Layer 7 DDoS signature."),
    ("A Web Application Firewall (WAF) helps against Layer 7 DDoS by:",
     "Encrypting disks", "Filtering malicious or abusive HTTP requests based on rules",
     "Replacing backups", "Disabling DNS", "B",
     "A WAF inspects HTTP traffic and can block patterns associated with application-layer floods."),
    ("Why is blocking a single source IP often ineffective against DDoS?",
     "IPs cannot be blocked", "Attacks come from thousands of distributed and spoofed sources",
     "Blocking is illegal", "It deletes data", "B",
     "Because DDoS uses many (often spoofed) sources, blocking one IP barely reduces the flood."),
    ("Engaging your ISP or upstream provider during a DDoS helps because they:",
     "Can pay the attacker", "Can filter or absorb attack traffic before it reaches your network",
     "Store your passwords", "Encrypt your files", "B",
     "Upstream providers have greater capacity and tooling to filter floods closer to the source."),
    ("Anycast routing aids DDoS resilience by:",
     "Routing all traffic to one server", "Distributing requests across many geographically dispersed nodes",
     "Disabling the network", "Encrypting packets", "B",
     "Anycast spreads incoming traffic across multiple sites, diluting the impact of a flood."),
    ("Over-provisioning bandwidth helps by:",
     "Guaranteeing immunity", "Providing headroom to absorb smaller floods without outage",
     "Encrypting traffic", "Removing all attacks", "B",
     "Extra capacity buys time and resilience against moderate volumetric attacks, though not unlimited ones."),
    ("A DDoS attack most directly threatens which security property?",
     "Confidentiality", "Integrity", "Availability", "Non-repudiation", "C",
     "Denial-of-service attacks target availability by making systems or data inaccessible."),
    ("Which is a sound preparation before a DDoS occurs?",
     "Wait until attacked to plan", "Have a tested response runbook and mitigation provider arranged in advance",
     "Disable all monitoring", "Remove backups", "B",
     "Pre-arranged mitigation and a rehearsed runbook enable a fast, effective response when attacks hit."),
    ("Traffic anomaly detection supports DDoS defense by:",
     "Encrypting payloads", "Alerting on unusual spikes or patterns so mitigation can start quickly",
     "Deleting logs", "Slowing the site", "B",
     "Early detection of abnormal traffic lets defenders trigger mitigations before the service is overwhelmed."),
    ("A 'low and slow' application-layer attack works by:",
     "Sending massive bandwidth", "Holding connections open with slow requests to exhaust server resources",
     "Encrypting data", "Spoofing DNS only", "B",
     "Low-and-slow attacks tie up server connections with drawn-out requests, exhausting capacity at low volume."),
    ("Why should unused or unnecessary internet-facing services be disabled?",
     "They improve speed", "They can be abused for amplification or add attack surface",
     "They block DDoS", "They store backups", "B",
     "Reducing exposed services limits both direct targets and amplification opportunities for attackers."),
    ("Geo-blocking or filtering can help when:",
     "All users are global and equal", "Attack traffic concentrates in regions you do not serve",
     "Never", "Only for email", "B",
     "If a service serves limited regions, filtering traffic from irrelevant regions can cut some attack volume."),
    ("DDoS-for-hire 'booter/stresser' services are:",
     "Legitimate testing tools that are always legal", "Illegal services that launch attacks for a fee",
     "Backup utilities", "Antivirus products", "B",
     "Booter/stresser services sell illegal DDoS capabilities; using them against others is a crime."),
    ("Which combination best improves DDoS resilience?",
     "CDN/scrubbing, rate limiting, autoscaling, WAF, and a response plan", "Only a single firewall",
     "Only stronger passwords", "Only antivirus", "A",
     "Layered network and application defenses plus planning give the strongest availability protection."),
    ("During an active DDoS, a sound first step is to:",
     "Shut down all logging", "Activate your mitigation/CDN plan and notify your provider",
     "Pay a ransom", "Email each attacker", "B",
     "Triggering pre-arranged mitigation and engaging the provider is the fastest path to restoring availability."),
    ("The fundamental challenge of DDoS defense is:",
     "It steals data invisibly", "Distinguishing and absorbing huge volumes of attack traffic vs. legitimate users",
     "It only affects email", "It cannot be mitigated at all", "B",
     "Effective defense must separate malicious floods from real users at scale, which is why layered mitigation matters."),
]


# ---------------------------------------------------------------------------
# Module 11 - Man-in-the-Middle (MitM) Attacks
# ---------------------------------------------------------------------------

MITM_CONTENT = """
<section>
  <h2>Man-in-the-Middle (MitM) Attacks</h2>
  <p>In a Man-in-the-Middle attack, an attacker secretly positions themselves
  between two parties to intercept, read, or alter the communication while both
  sides believe they are talking directly. This module covers common MitM
  techniques and the encryption and verification habits that defeat them.</p>
</section>

<section>
  <h3>1. How MitM works</h3>
  <p>The attacker relays messages between victim and server. If the channel is
  unencrypted or improperly validated, the attacker can read credentials, inject
  content, or hijack sessions. The goal is interception or tampering without
  either side noticing.</p>
</section>

<section>
  <h3>2. Common MitM techniques</h3>
  <ul>
    <li><strong>Evil twin / rogue Wi-Fi</strong>: a fake hotspot that mimics a real one.</li>
    <li><strong>ARP spoofing</strong>: poisons local network mappings to reroute traffic.</li>
    <li><strong>DNS spoofing</strong>: returns false DNS answers to redirect victims.</li>
    <li><strong>SSL stripping</strong>: downgrades HTTPS to HTTP to read traffic.</li>
    <li><strong>Session hijacking</strong>: steals session cookies/tokens to impersonate a user.</li>
    <li><strong>HTTPS interception with a fake certificate</strong> the victim is tricked into trusting.</li>
  </ul>
</section>

<section>
  <h3>3. Red flags</h3>
  <ul>
    <li>Browser certificate warnings you did not expect, or a missing padlock.</li>
    <li>A login page served over HTTP instead of HTTPS.</li>
    <li>Open public Wi-Fi with a generic or duplicated network name.</li>
    <li>Unexpected redirects, or a site that suddenly asks to re-enter credentials.</li>
  </ul>
</section>

<section>
  <h3>4. HTTP vs. HTTPS on untrusted networks</h3>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>http://login.example.com  (no TLS)
-&gt; credentials travel in cleartext;
   a MitM on the Wi-Fi can read them</code></pre>
    <pre class="code-block secure"><code>https://login.example.com (valid cert, HSTS)
-&gt; traffic is encrypted and authenticated;
   tampering breaks the TLS session</code></pre>
  </div>
</section>

<section>
  <h3>5. Defenses</h3>
  <ul>
    <li>Insist on HTTPS/TLS everywhere; heed certificate warnings.</li>
    <li>Enable HSTS so browsers refuse to downgrade to HTTP.</li>
    <li>Use a trusted VPN on public or untrusted Wi-Fi.</li>
    <li>Prefer phishing-resistant MFA and short-lived, protected session tokens.</li>
    <li>Use certificate pinning for sensitive apps where appropriate.</li>
    <li>Avoid sensitive logins on unknown networks; verify the network name.</li>
  </ul>
</section>

<section class="exercise" data-exercise="threat">
  <h3>Which actions reduce Man-in-the-Middle risk? Select all that apply.</h3>
  <div class="exercise-options">
    <label><input type="checkbox" data-answer="https" data-correct="true"> Only logging in over verified HTTPS</label>
    <label><input type="checkbox" data-answer="vpn" data-correct="true"> Using a trusted VPN on public Wi-Fi</label>
    <label><input type="checkbox" data-answer="ignorecert"> Clicking through certificate warnings to save time</label>
    <label><input type="checkbox" data-answer="hsts" data-correct="true"> Relying on HSTS to prevent HTTP downgrades</label>
    <label><input type="checkbox" data-answer="anywifi"> Joining any open Wi-Fi with a familiar-looking name</label>
  </div>
  <button type="button" class="btn btn-primary" data-action="check">Check</button>
  <p class="exercise-feedback" hidden></p>
</section>
"""

MITM_QUESTIONS = [
    ("What is a Man-in-the-Middle (MitM) attack?",
     "A physical theft of a server", "An attacker secretly intercepting or altering communication between two parties",
     "A type of backup", "A password rotation policy", "B",
     "In MitM, the attacker sits between two parties to read or modify traffic while both believe they talk directly."),
    ("Which security property is most directly violated when a MitM reads private traffic?",
     "Availability", "Confidentiality", "Redundancy", "Scalability", "B",
     "Intercepting and reading communications breaks confidentiality."),
    ("An 'evil twin' attack involves:",
     "A duplicated hard drive", "A rogue Wi-Fi access point mimicking a legitimate one to lure victims",
     "A cloned email", "A second admin account", "B",
     "Evil twin hotspots impersonate trusted networks so victims connect and route traffic through the attacker."),
    ("ARP spoofing enables MitM on a local network by:",
     "Encrypting all traffic", "Poisoning address mappings so traffic is rerouted through the attacker",
     "Disabling Wi-Fi", "Backing up data", "B",
     "ARP spoofing associates the attacker's MAC with another host's IP, redirecting local traffic through them."),
    ("DNS spoofing supports MitM by:",
     "Speeding up name resolution", "Returning false DNS answers that send victims to attacker-controlled sites",
     "Encrypting DNS", "Blocking ads", "B",
     "By returning forged DNS responses, attackers steer victims to malicious servers while addresses look normal."),
    ("SSL stripping works by:",
     "Strengthening encryption", "Downgrading an HTTPS connection to unencrypted HTTP so traffic can be read",
     "Adding a second certificate", "Blocking cookies", "B",
     "SSL stripping forces the victim onto HTTP, removing TLS so the attacker can read and modify traffic."),
    ("Why is HTTPS important on public Wi-Fi?",
     "It loads pages faster", "It encrypts and authenticates traffic so a local MitM cannot read or tamper with it",
     "It blocks ads", "It saves battery", "B",
     "TLS in HTTPS protects confidentiality and integrity, defeating passive interception and tampering."),
    ("A browser certificate warning on a login page should be treated as:",
     "A harmless glitch to click through", "A possible sign of interception that you should not bypass",
     "A speed improvement", "A backup prompt", "B",
     "Certificate warnings can indicate a MitM with a fake certificate; never click through on sensitive sites."),
    ("HSTS (HTTP Strict Transport Security) helps prevent MitM by:",
     "Allowing HTTP downgrades", "Forcing browsers to use HTTPS and refuse insecure connections to the site",
     "Disabling cookies", "Encrypting disks", "B",
     "HSTS instructs browsers to only connect over HTTPS, blocking SSL-stripping downgrade attempts."),
    ("Session hijacking in a MitM context means the attacker:",
     "Resets your password", "Steals a session cookie/token to impersonate the logged-in user",
     "Encrypts the session", "Backs up the session", "B",
     "Capturing a valid session token lets the attacker act as the authenticated user without the password."),
    ("Using a trusted VPN on public Wi-Fi helps because it:",
     "Makes Wi-Fi faster", "Encrypts your traffic end-to-end to the VPN, shielding it from local interception",
     "Disables HTTPS", "Removes the need for passwords", "B",
     "A VPN tunnel encrypts traffic across the untrusted local network, thwarting on-path eavesdroppers."),
    ("Certificate pinning protects sensitive apps by:",
     "Accepting any certificate", "Trusting only a specific known certificate/key, rejecting fraudulent ones",
     "Disabling TLS", "Storing passwords", "B",
     "Pinning ensures the app only accepts an expected certificate, blocking attacker-presented fake certs."),
    ("Which is a red flag of a possible MitM on Wi-Fi?",
     "A login page served over HTTP instead of HTTPS", "A valid padlock and correct domain",
     "An expected certificate", "A known, secured network", "A",
     "A sensitive page downgraded to HTTP suggests interception or stripping and should not be trusted."),
    ("Why is connecting to any open Wi-Fi with a familiar name risky?",
     "It is always safe", "It could be an evil-twin hotspot run by an attacker",
     "It is faster", "It uses less data", "B",
     "Attackers name rogue hotspots to mimic trusted networks, luring victims into a MitM position."),
    ("Phishing-resistant MFA (like passkeys) helps against MitM because:",
     "It shares passwords", "It binds authentication to the legitimate site, so relayed logins fail",
     "It disables HTTPS", "It stores cookies forever", "B",
     "Origin-bound authenticators do not produce valid responses for an attacker-controlled relay site."),
    ("End-to-end encryption (E2EE) in messaging defeats MitM by:",
     "Letting the server read messages", "Ensuring only the endpoints can decrypt the messages",
     "Disabling keys", "Sending plaintext", "B",
     "With E2EE, only the communicating endpoints hold keys, so an intermediary cannot read the content."),
    ("Verifying a website's domain and valid certificate before logging in helps:",
     "Speed up the page", "Confirm you are talking to the real server and not a MitM",
     "Disable cookies", "Save battery", "B",
     "Checking the domain and certificate validity reduces the chance of submitting data to an impostor."),
    ("Why are short-lived, securely-flagged session tokens safer?",
     "They never expire", "They limit the window and exposure if a token is intercepted",
     "They disable HTTPS", "They store passwords in plaintext", "B",
     "Short lifetimes and secure/HttpOnly flags reduce the value and accessibility of stolen tokens."),
    ("A MitM that alters data in transit threatens which property?",
     "Integrity", "Only availability", "Only redundancy", "Scalability", "A",
     "Tampering with messages in transit violates the integrity of the communication."),
    ("Email transport between servers can be protected from interception using:",
     "Plain SMTP only", "Opportunistic or enforced TLS (such as MTA-STS)",
     "Disabling encryption", "Open relays", "B",
     "TLS for mail transport (and policies like MTA-STS) protects messages from on-path interception."),
    ("Public key cryptography helps prevent MitM by:",
     "Sharing secret keys openly", "Letting parties verify identity and establish keys an interceptor cannot forge",
     "Disabling certificates", "Sending passwords in the clear", "B",
     "Public-key methods enable authentication and secure key exchange that resist on-path tampering."),
    ("A captive portal that asks for your bank login is suspicious because:",
     "Portals always need bank logins", "Legitimate Wi-Fi portals never require banking credentials, hinting at a MitM/phishing setup",
     "It speeds up login", "It is required by law", "B",
     "Genuine captive portals do not need banking credentials; such a request signals a malicious hotspot."),
    ("If your browser unexpectedly shows 'Not Secure' on a known HTTPS site, you should:",
     "Enter your password anyway", "Stop and verify the connection/network before entering sensitive data",
     "Disable the warning permanently", "Email the password", "B",
     "An unexpected insecure indicator can signal interception; verify before transmitting anything sensitive."),
    ("DNS over HTTPS (DoH) or DNSSEC helps against DNS-based MitM by:",
     "Sending DNS in plaintext", "Protecting the integrity/confidentiality of DNS responses",
     "Disabling DNS", "Slowing resolution only", "B",
     "Encrypting and/or authenticating DNS makes it harder to forge or read DNS answers in transit."),
    ("Mutual TLS (mTLS) strengthens defenses by:",
     "Authenticating only the client", "Authenticating both the client and the server to each other",
     "Disabling encryption", "Removing certificates", "B",
     "mTLS verifies both endpoints' certificates, making it much harder for an interceptor to impersonate either side."),
    ("Why should you avoid sensitive logins on unknown networks?",
     "They are always fast", "An attacker controlling the network could intercept or manipulate the traffic",
     "It saves data", "It is required for HTTPS", "B",
     "On an attacker-controlled network, MitM techniques put any sensitive data you transmit at risk."),
    ("A 'downgrade attack' attempts to:",
     "Upgrade your encryption", "Force a connection to use weaker or no encryption that can be broken",
     "Improve performance", "Add MFA", "B",
     "Downgrade attacks push parties to weaker protocols/ciphers, making interception feasible; modern TLS resists this."),
    ("Checking for the padlock alone is insufficient because:",
     "Padlocks guarantee a site is honest", "A phishing site can also have HTTPS; you must also verify the correct domain",
     "Padlocks are fake always", "HTTPS is unrelated to MitM", "B",
     "HTTPS only proves encryption to that domain; attackers can obtain certs for look-alike domains, so verify the name too."),
    ("Which combination best defends against MitM?",
     "HTTPS/TLS everywhere, HSTS, VPN on untrusted Wi-Fi, certificate validation, and phishing-resistant MFA",
     "Only a strong password", "Only antivirus", "Only a firewall", "A",
     "Layered encryption, transport hardening, verification, and strong authentication together defeat MitM techniques."),
    ("The core defensive idea against MitM is to ensure communications are:",
     "Fast and unencrypted", "Encrypted and authenticated end-to-end so interception or tampering fails",
     "Logged only", "Sent over HTTP", "B",
     "Strong encryption plus identity verification ensures an interceptor can neither read nor alter the traffic undetected."),
]


# ---------------------------------------------------------------------------
# Module list
# ---------------------------------------------------------------------------

MODULES = [
    {
        "title": "Phishing & Spear Phishing",
        "description": "Recognize and resist deceptive messages that steal credentials, money, or deliver malware, from bulk phishing to targeted spear phishing.",
        "category": "Human Risk",
        "order": 7,
        "content": PHISHING_CONTENT,
        "questions": PHISHING_QUESTIONS,
    },
    {
        "title": "Ransomware",
        "description": "Understand how ransomware encrypts and extorts victims, and how backups, MFA, patching, and response planning build resilience.",
        "category": "Endpoint Security",
        "order": 8,
        "content": RANSOMWARE_CONTENT,
        "questions": RANSOMWARE_QUESTIONS,
    },
    {
        "title": "Malware & Spyware",
        "description": "Learn the major malware families, common infection vectors, signs of compromise, and layered defenses for endpoints.",
        "category": "Endpoint Security",
        "order": 9,
        "content": MALWARE_CONTENT,
        "questions": MALWARE_QUESTIONS,
    },
    {
        "title": "DDoS Attacks",
        "description": "Explore how distributed denial-of-service attacks overwhelm services and how CDNs, scrubbing, rate limiting, and planning preserve availability.",
        "category": "Network Security",
        "order": 10,
        "content": DDOS_CONTENT,
        "questions": DDOS_QUESTIONS,
    },
    {
        "title": "Man-in-the-Middle (MitM) Attacks",
        "description": "See how attackers intercept and alter traffic, and how encryption, certificate validation, HSTS, and VPNs keep communications safe.",
        "category": "Network Security",
        "order": 11,
        "content": MITM_CONTENT,
        "questions": MITM_QUESTIONS,
    },
]
