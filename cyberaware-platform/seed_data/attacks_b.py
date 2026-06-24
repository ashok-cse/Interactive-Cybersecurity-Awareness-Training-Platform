"""Training modules 12-16: supply chain, zero-day, credential theft, cloud, BEC.

Authored defensive/educational content. Exports MODULES for the integrator to
wire into seed.py. See seed_data/CONTRACT for the dict + 7-tuple format.
"""

SUPPLY_CHAIN_CONTENT = """
<section>
  <h2>Supply Chain Attacks</h2>
  <p>A supply chain attack compromises an organisation indirectly, by tampering
  with a trusted third party - a software vendor, an open-source dependency, a
  build pipeline, or a managed service provider. Because the malicious code or
  access arrives through a channel the victim already trusts, these attacks
  bypass many traditional perimeter defences.</p>

  <h3>How the attack works</h3>
  <p>Instead of breaking through your front door, the attacker poisons something
  you willingly invite inside. Common vectors include:</p>
  <ul>
    <li><strong>Compromised software updates:</strong> Attackers breach a vendor
    and inject a backdoor into a signed update that customers install
    automatically (for example, the SolarWinds Orion compromise in 2020).</li>
    <li><strong>Malicious open-source packages:</strong> Typosquatting,
    dependency confusion, or a hijacked maintainer account ships malware to every
    project that pulls the dependency (for example, the event-stream npm
    incident).</li>
    <li><strong>Build/CI pipeline compromise:</strong> Tampering with build
    servers, signing keys, or container base images so the artifact is poisoned
    before it ever reaches a customer.</li>
    <li><strong>Hardware and firmware implants:</strong> Malicious components or
    firmware introduced during manufacturing or shipping.</li>
    <li><strong>Managed/MSP access abuse:</strong> Attackers compromise a service
    provider and pivot into all of its customers (for example, the Kaseya VSA
    ransomware incident).</li>
  </ul>

  <h3>Real-world red flags</h3>
  <ul>
    <li>A dependency name that is a near-miss of a popular package
    (<em>reqeusts</em> instead of <em>requests</em>).</li>
    <li>An internal package name that suddenly resolves from the public registry
    at a higher version number (dependency confusion).</li>
    <li>A signed update that triggers unexpected outbound network connections to
    unfamiliar domains.</li>
    <li>A maintainer account that adds a new co-maintainer and immediately
    publishes a minified, obfuscated release.</li>
    <li>Build artifacts whose hash does not match a reproducible build.</li>
  </ul>

  <h3>Defenses</h3>
  <ul>
    <li>Maintain a Software Bill of Materials (SBOM) so you know exactly what is
    in every release.</li>
    <li>Pin dependencies to specific versions and verify integrity with lock
    files and cryptographic hashes.</li>
    <li>Configure scoped/private registries and explicit source priority to
    prevent dependency-confusion substitution.</li>
    <li>Verify code signatures and use reproducible builds where possible.</li>
    <li>Apply least privilege to CI/CD: short-lived credentials, isolated
    runners, and protected signing keys (ideally in an HSM).</li>
    <li>Continuously monitor vendor advisories and software composition analysis
    (SCA) findings.</li>
  </ul>

  <h3>Dependency configuration: risky vs. safer</h3>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code># requirements.txt - no integrity, floating versions
requests&gt;=2.0
internal-utils        # may resolve from PUBLIC registry (dependency confusion)</code></pre>
    <pre class="code-block secure"><code># requirements.txt - pinned + hash-verified
requests==2.32.3 --hash=sha256:abc123...
# install internal pkgs only from the trusted index:
#   pip install --index-url https://pkgs.internal/simple internal-utils==1.4.2</code></pre>
  </div>

  <table class="table">
    <thead>
      <tr><th>Vector</th><th>Example</th><th>Primary defense</th></tr>
    </thead>
    <tbody>
      <tr><td>Update poisoning</td><td>SolarWinds Orion</td><td>Signature + build integrity verification</td></tr>
      <tr><td>Malicious package</td><td>event-stream</td><td>SCA, pinning, maintainer review</td></tr>
      <tr><td>Dependency confusion</td><td>Internal name on public registry</td><td>Scoped private registries</td></tr>
      <tr><td>MSP compromise</td><td>Kaseya VSA</td><td>Least privilege, segmentation, MFA</td></tr>
    </tbody>
  </table>

  <section class="exercise" data-exercise="threat">
    <h3>Which of these are supply chain attack vectors? Select all that apply.</h3>
    <div class="exercise-options">
      <label><input type="checkbox" data-answer="dependency-confusion" data-correct="true"> Publishing a higher-version public package with an internal name</label>
      <label><input type="checkbox" data-answer="signed-update" data-correct="true"> Injecting a backdoor into a vendor's signed software update</label>
      <label><input type="checkbox" data-answer="brute-force"> Guessing a user's password by brute force at the login page</label>
      <label><input type="checkbox" data-answer="typosquat" data-correct="true"> Uploading a malicious package named like a popular one</label>
    </div>
    <button type="button" class="btn btn-primary" data-action="check">Check</button>
    <p class="exercise-feedback" hidden></p>
  </section>
</section>
"""

SUPPLY_CHAIN_QUESTIONS = [
    (
        "What best defines a supply chain attack?",
        "An attack that compromises a target through a trusted third party such as a vendor or dependency",
        "An attack that floods a network with traffic",
        "An attack that only targets physical warehouses",
        "An attack that exclusively uses stolen credit cards",
        "A",
        "Supply chain attacks reach the victim indirectly through a trusted supplier, dependency, or service provider.",
    ),
    (
        "In the SolarWinds incident, how did the attackers reach victims?",
        "By phishing every customer individually",
        "By injecting a backdoor into a legitimately signed Orion software update",
        "By exploiting an unpatched web server at each customer",
        "By stealing laptops from customer offices",
        "B",
        "Attackers trojanised a signed Orion update so the backdoor was distributed automatically through normal update channels.",
    ),
    (
        "What is dependency confusion?",
        "When two developers pick the same variable name",
        "When a build fails because of conflicting versions",
        "When an attacker publishes a public package with an internal package name at a higher version so it is pulled instead",
        "When a license is incompatible with a project",
        "C",
        "Dependency confusion exploits resolvers that prefer the highest version, letting a public malicious package shadow an internal one.",
    ),
    (
        "What does an SBOM provide?",
        "A list of employees with admin rights",
        "A firewall rule set",
        "A backup schedule",
        "An inventory of the components and dependencies that make up a piece of software",
        "D",
        "A Software Bill of Materials inventories components so teams can quickly find affected software when a vulnerability is disclosed.",
    ),
    (
        "Which practice most directly prevents dependency confusion?",
        "Configuring scoped/private registries with explicit source priority",
        "Using floating version ranges",
        "Disabling lock files",
        "Allowing any registry mirror",
        "A",
        "Scoping internal packages to a private registry and controlling source priority stops public substitutes from being installed.",
    ),
    (
        "Typosquatting in package ecosystems refers to:",
        "Misconfiguring a server's hostname",
        "Registering package names that are common misspellings of popular packages to trick installers",
        "Renaming files to avoid detection",
        "Using uppercase letters in code",
        "B",
        "Typosquatting relies on developers mistyping a package name and installing the malicious lookalike instead.",
    ),
    (
        "Why are software supply chain attacks especially dangerous?",
        "They are easy for antivirus to detect",
        "They only affect one machine",
        "They arrive through trusted, often automated channels, bypassing perimeter defences",
        "They require physical access",
        "C",
        "Because the malicious content rides a trusted update or dependency, traditional perimeter controls often do not flag it.",
    ),
    (
        "A lock file with cryptographic hashes primarily ensures:",
        "Faster compilation",
        "Smaller binary size",
        "Automatic license approval",
        "That the exact, unmodified dependency versions are installed",
        "D",
        "Hash-pinned lock files detect tampering and guarantee the same verified artifact is installed everywhere.",
    ),
    (
        "The Kaseya VSA incident is an example of attackers abusing:",
        "A managed service provider's tooling to reach many downstream customers",
        "A single stolen laptop",
        "A physical firewall failure",
        "A DNS cache only",
        "A",
        "Attackers exploited the MSP/RMM platform to push ransomware to numerous downstream customer environments at once.",
    ),
    (
        "What is a reproducible build?",
        "A build that runs faster each time",
        "A build that produces bit-for-bit identical output from the same source, allowing verification",
        "A build that skips tests",
        "A build that only works on one machine",
        "B",
        "Reproducible builds let independent parties confirm an artifact was built from the claimed source, detecting tampering.",
    ),
    (
        "Storing software signing keys in an HSM helps because it:",
        "Speeds up the network",
        "Eliminates the need for backups",
        "Protects private keys from extraction even if the build server is compromised",
        "Automatically patches code",
        "C",
        "A hardware security module keeps signing keys non-exportable, limiting damage if the build environment is breached.",
    ),
    (
        "Which is a red flag in an open-source dependency?",
        "A clear changelog and signed release",
        "A widely reviewed pull request",
        "Comprehensive unit tests",
        "A maintainer adding a co-maintainer who immediately ships an obfuscated minified release",
        "D",
        "Sudden maintainer changes followed by obfuscated releases are a classic precursor to a poisoned package.",
    ),
    (
        "Software composition analysis (SCA) tools mainly help you:",
        "Identify known-vulnerable and risky dependencies in your project",
        "Write faster algorithms",
        "Design a user interface",
        "Encrypt disk volumes",
        "A",
        "SCA scans your dependency tree against vulnerability databases so you can remediate risky components.",
    ),
    (
        "Least privilege in a CI/CD pipeline means:",
        "Giving every job full admin to be safe",
        "Granting each job only the minimal, short-lived credentials it needs",
        "Sharing one long-lived token across all jobs",
        "Disabling all authentication",
        "B",
        "Minimal, short-lived, scoped credentials limit what an attacker can do if a pipeline step is compromised.",
    ),
    (
        "A firmware implant introduced during manufacturing is an example of a:",
        "Network flooding attack",
        "Cross-site scripting attack",
        "Hardware supply chain attack",
        "Password spray",
        "C",
        "Tampering with components or firmware before delivery is a hardware-level supply chain compromise.",
    ),
    (
        "Why pin dependencies to specific versions?",
        "To always get the newest features automatically",
        "To reduce code readability",
        "To bypass code review",
        "To prevent an unexpected or malicious newer version from being pulled silently",
        "D",
        "Version pinning makes installs deterministic and blocks silent upgrades that could introduce malicious code.",
    ),
    (
        "Verifying a vendor update's digital signature confirms:",
        "The update genuinely came from the vendor and was not altered in transit",
        "The update is bug-free",
        "The update is faster",
        "The update is free",
        "A",
        "Signature verification proves authenticity and integrity, though it does not guarantee the vendor itself was not compromised.",
    ),
    (
        "The event-stream npm incident occurred because:",
        "A firewall was misconfigured",
        "A maintainer handed control to a malicious actor who added a backdoored dependency",
        "A database was left public",
        "A laptop was stolen",
        "B",
        "Ownership of a popular package was transferred to a bad actor who slipped in malicious code targeting a downstream wallet app.",
    ),
    (
        "Which monitoring practice best catches a poisoned update post-install?",
        "Ignoring outbound traffic",
        "Disabling logging",
        "Watching for unexpected outbound connections to unfamiliar domains",
        "Trusting all signed binaries forever",
        "C",
        "Beaconing to unknown infrastructure is a strong indicator a trusted binary has been backdoored.",
    ),
    (
        "A vendor risk assessment should evaluate a supplier's:",
        "Office decor only",
        "Marketing budget",
        "Stock price exclusively",
        "Security practices, patching cadence, and breach history",
        "D",
        "Assessing a vendor's actual security posture helps you judge the risk of integrating their software or services.",
    ),
    (
        "Why segment networks that connect to third-party/MSP tooling?",
        "To limit lateral movement if the third party is compromised",
        "To make the network slower",
        "To avoid using passwords",
        "To increase trust automatically",
        "A",
        "Segmentation contains a third-party compromise so it cannot spread freely across your environment.",
    ),
    (
        "Container base image risk is best reduced by:",
        "Using random untrusted images",
        "Pulling minimal, pinned, scanned images from trusted registries",
        "Never updating images",
        "Disabling image scanning",
        "B",
        "Trusted, minimal, pinned, and scanned base images shrink the attack surface and reduce inherited vulnerabilities.",
    ),
    (
        "Which statement about signed updates is most accurate?",
        "A valid signature guarantees the vendor was never breached",
        "Signatures are unnecessary if you trust the vendor",
        "Signatures verify origin and integrity but cannot prove the vendor's build was not compromised",
        "Signatures make code run faster",
        "C",
        "SolarWinds showed that a valid signature can still wrap malicious code if the build process itself is compromised.",
    ),
    (
        "Continuous monitoring of vendor advisories helps you:",
        "Avoid ever patching",
        "Ignore CVEs",
        "Disable updates",
        "Respond quickly when a dependency or product you use is found vulnerable",
        "D",
        "Tracking advisories lets you act fast on newly disclosed vulnerabilities in your supply chain.",
    ),
    (
        "A scoped npm package like @myorg/utils helps because:",
        "The scope ties the package to your organisation, reducing namespace confusion",
        "It is always faster",
        "It cannot be installed",
        "It disables versioning",
        "A",
        "Scoping reserves a namespace under your control, mitigating typosquatting and dependency confusion.",
    ),
    (
        "If a build server is compromised, the highest-impact risk is:",
        "Slower builds",
        "Malicious code being signed and shipped to all customers as trusted",
        "A misspelled commit message",
        "A larger log file",
        "B",
        "A compromised build server can produce trusted, signed, poisoned artifacts distributed to everyone downstream.",
    ),
    (
        "Which is the best first response when a dependency you use is reported malicious?",
        "Ignore it until the next release",
        "Delete all logs",
        "Identify affected systems via your SBOM, remove/rollback the package, and rotate exposed secrets",
        "Publish the incident publicly before investigating",
        "C",
        "Rapid scoping with an SBOM, removal, and secret rotation contains the impact of a malicious dependency.",
    ),
    (
        "Provenance attestation (for example SLSA) aims to:",
        "Make code prettier",
        "Encrypt user passwords",
        "Replace firewalls",
        "Provide verifiable evidence of how and from what source an artifact was built",
        "D",
        "Build provenance frameworks document the build's origin and process so consumers can verify artifact integrity.",
    ),
    (
        "Why is auto-updating without verification risky in a supply chain context?",
        "A poisoned update can be installed instantly and at scale before anyone notices",
        "It always breaks the UI",
        "It uses too much disk",
        "It improves security automatically",
        "A",
        "Unverified auto-updates turn one vendor compromise into immediate, widespread infection.",
    ),
    (
        "The core principle behind defending the software supply chain is:",
        "Trust everything that is signed forever",
        "Establish and continuously verify trust at every link rather than assuming it",
        "Avoid all third-party software",
        "Only use software older than ten years",
        "B",
        "Defence depends on verifying integrity and provenance at each stage instead of blindly trusting any single link.",
    ),
]

ZERO_DAY_CONTENT = """
<section>
  <h2>Zero-Day Exploits</h2>
  <p>A zero-day vulnerability is a flaw that the software vendor does not yet
  know about (or has not yet patched). A zero-day exploit is attack code that
  abuses such a flaw. The name comes from the fact that defenders have had
  "zero days" to prepare a fix when the exploit appears in the wild.</p>

  <h3>How the attack works</h3>
  <p>Attackers (or researchers) discover an unknown flaw - a memory corruption,
  logic error, or input-handling bug. Because no patch exists, signature-based
  defences may not recognise the exploit. The window between discovery and a
  released, deployed patch is the period of greatest risk.</p>
  <ul>
    <li><strong>Discovery:</strong> through fuzzing, reverse engineering, or
    accidental disclosure.</li>
    <li><strong>Weaponisation:</strong> a reliable exploit is built, sometimes
    chained with other bugs (an "exploit chain").</li>
    <li><strong>Delivery:</strong> via phishing, a malicious document, a watering
    hole site, or direct network exploitation.</li>
    <li><strong>Disclosure:</strong> responsible disclosure gives the vendor time
    to patch; full or zero-day disclosure does not.</li>
  </ul>

  <h3>Key terminology and timeline</h3>
  <table class="table">
    <thead>
      <tr><th>Term</th><th>Meaning</th></tr>
    </thead>
    <tbody>
      <tr><td>Zero-day vulnerability</td><td>An unknown/unpatched flaw</td></tr>
      <tr><td>Zero-day exploit</td><td>Working attack code for that flaw</td></tr>
      <tr><td>N-day</td><td>A known, patched flaw still exploited on unpatched systems</td></tr>
      <tr><td>Window of exposure</td><td>Time from exploitation to patch deployment</td></tr>
      <tr><td>CVE</td><td>A public identifier assigned once the flaw is disclosed</td></tr>
    </tbody>
  </table>

  <h3>Real-world examples</h3>
  <ul>
    <li><strong>Stuxnet</strong> chained multiple Windows zero-days to target
    industrial control systems.</li>
    <li><strong>Log4Shell</strong> (CVE-2021-44228) was exploited rapidly across
    the internet before many organisations could patch.</li>
    <li>Browser and mobile zero-days are frequently used in targeted
    surveillance.</li>
  </ul>

  <h3>Defenses</h3>
  <ul>
    <li><strong>Defense in depth:</strong> assume any single control can fail.</li>
    <li><strong>Rapid patch management:</strong> shrink the window of exposure by
    patching quickly once fixes appear.</li>
    <li><strong>Virtual patching / WAF rules</strong> to block exploitation while
    a real patch is prepared.</li>
    <li><strong>Behavioural / EDR detection</strong> that flags anomalous
    activity rather than relying only on signatures.</li>
    <li><strong>Least privilege and sandboxing</strong> to limit what a successful
    exploit can do.</li>
    <li><strong>Attack surface reduction:</strong> disable unused features and
    services.</li>
    <li><strong>Threat intelligence and bug-bounty programmes</strong> to learn of
    flaws early.</li>
  </ul>

  <h3>Input handling: exploitable vs. hardened</h3>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>char buf[64];
strcpy(buf, user_input);   // no bounds check -&gt; overflow primitive</code></pre>
    <pre class="code-block secure"><code>char buf[64];
strncpy(buf, user_input, sizeof(buf) - 1);
buf[sizeof(buf) - 1] = '\0';   // bounded copy reduces memory-corruption risk</code></pre>
  </div>

  <section class="exercise" data-exercise="scenario">
    <h3>Scenario: A critical zero-day is announced for a public-facing app you run, and no patch exists yet. What is the safest immediate action?</h3>
    <p><em>You operate an internet-facing application and a zero-day with active exploitation is disclosed. The vendor says a patch is days away.</em></p>
    <div class="exercise-options">
      <button type="button" class="btn btn-secondary" data-answer="unsafe">Do nothing and wait for the official patch</button>
      <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Apply mitigations now: virtual patch/WAF rules, restrict exposure, and monitor closely</button>
    </div>
    <p class="exercise-feedback" hidden></p>
  </section>
</section>
"""

ZERO_DAY_QUESTIONS = [
    (
        "What is a zero-day vulnerability?",
        "A flaw unknown to the vendor (or unpatched) and therefore without an available fix",
        "A flaw that has been patched for years",
        "A flaw that only affects old hardware",
        "A flaw that is impossible to exploit",
        "A",
        "Zero-day refers to a vulnerability the vendor has not patched, giving defenders zero days of advance fix.",
    ),
    (
        "Why does the term include the words zero days?",
        "It takes zero days to exploit",
        "Defenders have had zero days to develop and deploy a fix when the exploit appears",
        "It costs zero dollars",
        "It affects zero users",
        "B",
        "The name reflects that no patch is available when the attack emerges, so there has been no time to prepare.",
    ),
    (
        "What distinguishes an N-day from a zero-day?",
        "An N-day has no patch",
        "An N-day cannot be exploited",
        "An N-day is a known, patched flaw still being exploited on unpatched systems",
        "An N-day only affects mobile devices",
        "C",
        "N-day flaws are publicly known and patched, but remain dangerous wherever the patch has not been applied.",
    ),
    (
        "Why can signature-based antivirus miss a fresh zero-day exploit?",
        "Signatures update instantly worldwide",
        "Antivirus ignores all executables",
        "Zero-days are always encrypted",
        "There is no known signature yet for an unknown, never-seen exploit",
        "D",
        "Without prior knowledge of the exploit, signature databases have nothing to match against.",
    ),
    (
        "What is the window of exposure?",
        "The period between exploitation and the deployment of an effective patch",
        "The time a screen stays on",
        "The time to reboot a server",
        "The warranty period of hardware",
        "A",
        "Reducing this window through fast patching and mitigations is central to limiting zero-day damage.",
    ),
    (
        "Virtual patching with a WAF is useful because it:",
        "Permanently fixes the source code",
        "Can block exploitation attempts while a real patch is being prepared",
        "Removes the need to ever patch",
        "Slows the entire internet",
        "B",
        "Virtual patches buy time by filtering malicious input even though the underlying flaw still exists.",
    ),
    (
        "An exploit chain is:",
        "A single trivial bug",
        "A blockchain product",
        "Multiple vulnerabilities combined to achieve a larger goal such as full compromise",
        "A type of password",
        "C",
        "Attackers often chain several flaws (for example, a sandbox escape plus privilege escalation) for greater impact.",
    ),
    (
        "Which incident chained multiple Windows zero-days against industrial systems?",
        "WannaCry only",
        "Heartbleed",
        "POODLE",
        "Stuxnet",
        "D",
        "Stuxnet is a well-known example of an advanced threat using several zero-days to reach ICS targets.",
    ),
    (
        "Log4Shell (CVE-2021-44228) was notable because:",
        "It was widely and rapidly exploited across many systems before patching",
        "It was patched before disclosure with no risk",
        "It only affected printers",
        "It required physical access",
        "A",
        "Log4Shell's ubiquity and ease of exploitation led to a global scramble to patch.",
    ),
    (
        "Responsible (coordinated) disclosure means:",
        "Publishing the exploit immediately with no warning",
        "Privately notifying the vendor and allowing time to patch before public details",
        "Selling the exploit to the highest bidder",
        "Ignoring the flaw",
        "B",
        "Coordinated disclosure gives vendors time to fix the flaw before details that aid attackers are released.",
    ),
    (
        "Defense in depth helps against zero-days because:",
        "One control is always enough",
        "It removes the need for patching",
        "Multiple layered controls mean a single bypassed control does not equal full compromise",
        "It only applies to firewalls",
        "C",
        "Layered defences ensure that even an unknown exploit must defeat several controls to succeed.",
    ),
    (
        "EDR/behavioural detection helps with zero-days by:",
        "Matching only known file hashes",
        "Disabling logging",
        "Blocking all network traffic permanently",
        "Flagging anomalous behaviour that an exploit triggers, even without a signature",
        "D",
        "Behaviour-based detection can catch the actions of a novel exploit (unusual process spawning, injection, etc.).",
    ),
    (
        "How does least privilege limit zero-day impact?",
        "It restricts what a successful exploit can access or do",
        "It makes exploits faster",
        "It removes all user accounts",
        "It guarantees no exploit succeeds",
        "A",
        "If an exploited process has limited rights, the damage an attacker can do is constrained.",
    ),
    (
        "Sandboxing a browser tab or document viewer aims to:",
        "Increase rendering speed only",
        "Contain exploit code so it cannot easily reach the rest of the system",
        "Disable JavaScript permanently",
        "Encrypt the hard drive",
        "B",
        "Sandboxes isolate untrusted content; an attacker must also escape the sandbox to do real harm.",
    ),
    (
        "Attack surface reduction means:",
        "Adding as many features as possible",
        "Opening all firewall ports",
        "Disabling unused services and features so there is less to exploit",
        "Granting admin to everyone",
        "C",
        "Fewer enabled features and services mean fewer potential zero-day entry points.",
    ),
    (
        "A bug bounty programme primarily helps an organisation by:",
        "Selling vulnerabilities on the black market",
        "Hiding all vulnerabilities",
        "Replacing the need for a security team",
        "Encouraging researchers to report flaws responsibly for a reward",
        "D",
        "Bounties incentivise finders to disclose flaws to you rather than to attackers.",
    ),
    (
        "Once a zero-day becomes public and a patch is released, the flaw is often called:",
        "An N-day",
        "A false positive",
        "A honeypot",
        "A canary",
        "A",
        "After disclosure and patching, exploitation of unpatched systems is N-day exploitation.",
    ),
    (
        "Fuzzing is a technique that:",
        "Encrypts network traffic",
        "Feeds malformed or random inputs to software to discover crashes and flaws",
        "Backs up databases",
        "Manages passwords",
        "B",
        "Fuzzers automatically generate unexpected inputs to surface vulnerabilities, often before vendors find them.",
    ),
    (
        "Why is rapid patch management critical even though it does not stop the first zero-day use?",
        "It does nothing useful",
        "It increases the attack surface",
        "It quickly closes the window so the flaw cannot keep being exploited as an N-day",
        "It only matters for printers",
        "C",
        "Fast patching shrinks the time attackers can exploit a now-known flaw across your estate.",
    ),
    (
        "A watering hole attack used to deliver a zero-day involves:",
        "Poisoning a water supply",
        "Spraying passwords",
        "Sending physical mail",
        "Compromising a website the target group frequently visits to serve the exploit",
        "D",
        "Attackers infect a site the victims trust, so visiting it triggers the exploit.",
    ),
    (
        "Which statement about zero-day markets is accurate?",
        "Working zero-day exploits can be highly valuable and traded among offensive actors",
        "Zero-days have no monetary value",
        "Vendors always know about every zero-day",
        "Zero-days only affect open-source software",
        "A",
        "Reliable zero-days for popular targets can command high prices, motivating their secrecy.",
    ),
    (
        "Memory-safety bugs like buffer overflows are common sources of zero-days because:",
        "They never cause crashes",
        "Unbounded operations can corrupt memory and grant attacker control of execution",
        "They only affect text files",
        "They are impossible in any language",
        "B",
        "Out-of-bounds writes can overwrite control data, a frequent primitive for code execution exploits.",
    ),
    (
        "Using a memory-safe language (or bounded operations) helps by:",
        "Guaranteeing zero bugs of any kind",
        "Making code unreadable",
        "Eliminating whole classes of memory-corruption vulnerabilities",
        "Removing the need for testing",
        "C",
        "Memory safety removes common overflow/use-after-free classes that drive many zero-days.",
    ),
    (
        "When a critical zero-day with active exploitation hits a public app with no patch, the best immediate step is:",
        "Wait silently for the patch and change nothing",
        "Publicly post your server details",
        "Disable all logging",
        "Apply available mitigations, reduce exposure, and increase monitoring now",
        "D",
        "Immediate mitigations and tighter monitoring reduce risk during the pre-patch window.",
    ),
    (
        "Threat intelligence feeds help defenders against emerging zero-days by:",
        "Providing early indicators and context about active exploitation",
        "Guaranteeing no attacks occur",
        "Replacing all endpoint security",
        "Slowing patch deployment",
        "A",
        "Timely intel helps teams prioritise mitigations and detect indicators of active campaigns.",
    ),
    (
        "Why is a CVE identifier usually assigned after disclosure?",
        "Because CVEs are secret",
        "A CVE provides a standard public reference once the vulnerability is known and disclosed",
        "Because vendors never track flaws",
        "Because CVEs only apply to hardware",
        "B",
        "CVE IDs standardise references to publicly known vulnerabilities for coordination and tracking.",
    ),
    (
        "Network segmentation aids zero-day resilience because it:",
        "Makes exploits more reliable",
        "Removes the need for patching",
        "Limits how far an attacker can move after exploiting one system",
        "Disables monitoring",
        "C",
        "Segmentation contains a successful exploit, slowing lateral movement to critical assets.",
    ),
    (
        "Which is NOT an effective zero-day mitigation strategy?",
        "Behavioural detection",
        "Least privilege",
        "Virtual patching",
        "Disabling all security logging to save space",
        "D",
        "Disabling logging blinds defenders; the others are legitimate layered mitigations.",
    ),
    (
        "The main reason zero-days are so prized by attackers is that they:",
        "Can bypass defences that rely on prior knowledge of the threat",
        "Are always loud and obvious",
        "Only work after a patch is released",
        "Require the vendor's permission",
        "A",
        "Because no one is yet defending against them specifically, zero-days offer stealthy, reliable access.",
    ),
    (
        "The overarching defensive mindset for zero-days is:",
        "Assume perfect prevention is possible",
        "Assume compromise is possible and build detection, containment, and rapid response",
        "Rely solely on signatures",
        "Never update anything",
        "B",
        "Since you cannot patch what you do not know about, resilience comes from detection and containment, not prevention alone.",
    ),
]

CREDENTIAL_THEFT_CONTENT = """
<section>
  <h2>Credential Theft and Identity Abuse</h2>
  <p>Stolen credentials are one of the most common entry points in modern
  breaches. Once an attacker holds a valid username and password (or a session
  token), they can often walk straight through the front door as a legitimate
  user - no exploit required.</p>

  <h3>How credentials are stolen</h3>
  <ul>
    <li><strong>Phishing:</strong> fake login pages harvest credentials.</li>
    <li><strong>Infostealer malware:</strong> grabs saved passwords, cookies, and
    session tokens from the browser.</li>
    <li><strong>Database breaches:</strong> attackers dump and crack stored
    password hashes.</li>
    <li><strong>Keyloggers and shoulder surfing.</strong></li>
    <li><strong>Man-in-the-middle</strong> capture on insecure channels.</li>
  </ul>

  <h3>How stolen credentials are abused</h3>
  <ul>
    <li><strong>Credential stuffing:</strong> trying breached username/password
    pairs across many sites, exploiting password reuse.</li>
    <li><strong>Password spraying:</strong> trying a few common passwords against
    many accounts to avoid lockouts.</li>
    <li><strong>Pass-the-hash / pass-the-ticket:</strong> reusing captured
    authentication material without knowing the plaintext password.</li>
    <li><strong>Session hijacking / token theft:</strong> stealing a valid
    session cookie to bypass even MFA.</li>
    <li><strong>MFA fatigue (push bombing):</strong> spamming approval prompts
    until a user taps Approve.</li>
  </ul>

  <h3>Red flags</h3>
  <ul>
    <li>Impossible-travel logins (two countries minutes apart).</li>
    <li>A burst of failed logins across many accounts (spraying).</li>
    <li>Unexpected MFA prompts you did not initiate.</li>
    <li>New OAuth app grants or inbox rules you did not create.</li>
  </ul>

  <h3>Defenses</h3>
  <ul>
    <li><strong>Phishing-resistant MFA</strong> (FIDO2/WebAuthn passkeys) over SMS
    codes.</li>
    <li><strong>Unique passwords + a password manager</strong> to kill reuse.</li>
    <li><strong>Salted, slow password hashing</strong> (bcrypt, scrypt, Argon2)
    server-side.</li>
    <li><strong>Detection:</strong> impossible-travel and anomaly alerts, lockout
    and throttling.</li>
    <li><strong>Least privilege and short session lifetimes;</strong> revoke
    tokens on risk events.</li>
    <li><strong>Number matching</strong> to defeat MFA fatigue.</li>
  </ul>

  <h3>Server-side password storage: weak vs. strong</h3>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code># NEVER: fast/unsalted hash or plaintext
stored = md5(password)          # fast, crackable, no salt</code></pre>
    <pre class="code-block secure"><code># Strong: salted, slow, adaptive KDF
import bcrypt
stored = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # per-user salt + work factor</code></pre>
  </div>

  <table class="table">
    <thead>
      <tr><th>Technique</th><th>What it exploits</th><th>Key defense</th></tr>
    </thead>
    <tbody>
      <tr><td>Credential stuffing</td><td>Password reuse</td><td>Unique passwords, MFA</td></tr>
      <tr><td>Password spraying</td><td>Common passwords</td><td>Strong policy, lockout, MFA</td></tr>
      <tr><td>Token theft</td><td>Stolen session cookie</td><td>Short sessions, token binding</td></tr>
      <tr><td>MFA fatigue</td><td>User approval habits</td><td>Number matching</td></tr>
    </tbody>
  </table>

  <section class="exercise" data-exercise="scenario">
    <h3>Scenario: Your phone buzzes with repeated MFA approval prompts you did not request. What should you do?</h3>
    <p><em>You are not trying to log in anywhere, yet push approval requests keep arriving on your authenticator app.</em></p>
    <div class="exercise-options">
      <button type="button" class="btn btn-secondary" data-answer="unsafe">Tap Approve to make the prompts stop</button>
      <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Deny all prompts, report it, and change your password immediately</button>
    </div>
    <p class="exercise-feedback" hidden></p>
  </section>
</section>
"""

CREDENTIAL_THEFT_QUESTIONS = [
    (
        "What is credential stuffing?",
        "Automatically trying breached username/password pairs across many sites to exploit reuse",
        "Cracking a single hash offline",
        "Guessing one account with random strings",
        "Stuffing extra characters into a password field",
        "A",
        "Credential stuffing replays leaked credential pairs on other services, succeeding wherever users reused passwords.",
    ),
    (
        "How does password spraying avoid account lockouts?",
        "It tries thousands of passwords on one account",
        "It tries a few common passwords across many accounts",
        "It never authenticates",
        "It only runs at night",
        "B",
        "Spraying uses a small set of common passwords against many accounts, staying under per-account lockout thresholds.",
    ),
    (
        "Why is password reuse dangerous?",
        "It makes passwords too long",
        "It speeds up logins",
        "One breached site exposes every other site that shares that password",
        "It improves entropy",
        "C",
        "Reuse turns a single breach into access across all accounts sharing the credential, the core of credential stuffing.",
    ),
    (
        "Which is considered phishing-resistant MFA?",
        "SMS one-time codes",
        "Email codes",
        "Security questions",
        "FIDO2/WebAuthn passkeys",
        "D",
        "FIDO2/WebAuthn binds authentication to the legitimate site origin, resisting phishing and replay.",
    ),
    (
        "What is an infostealer?",
        "Malware that harvests saved passwords, cookies, and session tokens",
        "A firewall feature",
        "A password manager",
        "A backup tool",
        "A",
        "Infostealers exfiltrate stored credentials and session data, fueling account takeover and token theft.",
    ),
    (
        "MFA fatigue (push bombing) works by:",
        "Cracking a hash",
        "Spamming approval prompts until the user finally taps Approve",
        "Disabling the network",
        "Guessing the username",
        "B",
        "Attackers with a valid password flood the user with prompts hoping one is approved out of annoyance or habit.",
    ),
    (
        "Number matching defends against MFA fatigue because it:",
        "Sends more prompts",
        "Removes MFA entirely",
        "Requires the user to enter a number shown on the login screen, so blind approval fails",
        "Uses SMS only",
        "C",
        "The user must read and type a code from the genuine login attempt, defeating blind push approvals.",
    ),
    (
        "Session/token theft can bypass MFA because:",
        "It guesses the password",
        "MFA tokens never expire",
        "It disables the firewall",
        "A stolen valid session cookie is already an authenticated session, needing no re-auth",
        "D",
        "If the attacker replays a live session token, the system treats them as the already-authenticated user.",
    ),
    (
        "Pass-the-hash attacks reuse:",
        "Captured password hash material to authenticate without knowing the plaintext",
        "A plaintext password typed manually",
        "A CAPTCHA answer",
        "A printed QR code",
        "A",
        "Pass-the-hash leverages the stored/captured hash directly against systems that accept it for authentication.",
    ),
    (
        "Why store passwords with bcrypt, scrypt, or Argon2 instead of MD5?",
        "They are faster to compute",
        "They are slow and salted, making large-scale cracking far harder",
        "They are reversible",
        "They need no salt",
        "B",
        "Adaptive, salted KDFs deliberately slow brute force and defeat precomputed rainbow tables.",
    ),
    (
        "A salt in password hashing primarily prevents:",
        "Network sniffing",
        "MFA prompts",
        "Identical passwords producing identical hashes and rainbow-table reuse",
        "DNS spoofing",
        "C",
        "Per-user salts ensure equal passwords hash differently, blocking precomputed table attacks.",
    ),
    (
        "Impossible-travel detection flags:",
        "A user logging in twice from the same office",
        "A slow password",
        "A long username",
        "Logins from distant locations within a timeframe no real travel allows",
        "D",
        "Geographically impossible login sequences strongly suggest stolen credentials in use.",
    ),
    (
        "Which is the strongest action against password reuse for users?",
        "Using a password manager to generate unique passwords per site",
        "Writing one password on a sticky note for all sites",
        "Adding 1 to the same password each time",
        "Sharing passwords with colleagues",
        "A",
        "A password manager makes unique, strong credentials per site practical, eliminating reuse.",
    ),
    (
        "Short session lifetimes help by:",
        "Annoying users only",
        "Reducing the value and lifespan of a stolen session token",
        "Removing the need for passwords",
        "Disabling MFA",
        "B",
        "If sessions expire quickly, a stolen token becomes useless sooner, limiting attacker dwell time.",
    ),
    (
        "A keylogger steals credentials by:",
        "Encrypting the disk",
        "Blocking network ports",
        "Recording keystrokes including typed passwords",
        "Rotating session tokens",
        "C",
        "Keyloggers capture typed input such as passwords before any masking or encryption.",
    ),
    (
        "Account lockout and throttling primarily mitigate:",
        "Phishing emails",
        "Physical theft",
        "Cable failures",
        "Online brute-force and spraying attempts",
        "D",
        "Limiting attempts slows and blocks high-volume guessing attacks against login endpoints.",
    ),
    (
        "A malicious OAuth app grant is dangerous because it can:",
        "Provide persistent access to data/mailboxes even after a password change",
        "Only change wallpaper",
        "Speed up the browser",
        "Disable the keyboard",
        "A",
        "OAuth consent grants persist independently of the password, so attackers use them for durable access.",
    ),
    (
        "Why prefer passkeys over SMS codes?",
        "SMS is encrypted end to end always",
        "Passkeys resist phishing and SIM-swap/interception that affect SMS codes",
        "SMS cannot be intercepted",
        "Passkeys require no device",
        "B",
        "SMS codes are phishable and vulnerable to SIM swapping, while passkeys are bound to the legitimate origin.",
    ),
    (
        "Credential theft often needs no software exploit because:",
        "Exploits are always required",
        "All systems block valid logins",
        "A valid login lets the attacker enter as a legitimate user",
        "Passwords cannot be stolen",
        "C",
        "With working credentials, the attacker authenticates normally, avoiding noisy exploitation.",
    ),
    (
        "Which log pattern most suggests password spraying?",
        "One failed login then success",
        "No logins at all",
        "Many successful logins from one user",
        "A few failed attempts spread across many different accounts",
        "D",
        "Low-and-slow failures across many accounts are the signature of spraying designed to dodge lockouts.",
    ),
    (
        "Token binding (for example to a device/TLS) helps because it:",
        "Ties a session token to a specific client so a stolen token is harder to replay elsewhere",
        "Makes tokens last forever",
        "Removes the need for HTTPS",
        "Shares tokens across users",
        "A",
        "Binding a token to its origin/device limits an attacker's ability to reuse a stolen cookie.",
    ),
    (
        "What should you do if you receive MFA prompts you did not initiate?",
        "Approve them to stop the noise",
        "Deny them, report it, and change your password since someone likely has it",
        "Ignore them entirely",
        "Forward the codes to the requester",
        "B",
        "Unrequested prompts mean an attacker already has your password; deny, report, and rotate credentials.",
    ),
    (
        "Rate limiting login attempts protects against:",
        "Slow disk reads",
        "DNS caching",
        "High-speed automated guessing such as stuffing and brute force",
        "Code signing",
        "C",
        "Throttling requests blunts automated credential attacks that rely on many attempts.",
    ),
    (
        "Why never store passwords in plaintext?",
        "It uses too much disk",
        "It is slower to log in",
        "It improves security",
        "A single database breach immediately exposes every user's actual password",
        "D",
        "Plaintext storage means any breach hands attackers usable credentials, often reused elsewhere.",
    ),
    (
        "Adaptive (work-factor) hashing is valuable because:",
        "The cost can be increased as hardware improves, keeping cracking expensive",
        "It gets faster over time",
        "It removes salts",
        "It reverses the hash",
        "A",
        "Tunable work factors let defenders keep pace with faster cracking hardware over the years.",
    ),
    (
        "Disabling a departed employee's accounts promptly helps prevent:",
        "Faster networks",
        "Orphaned-credential abuse and unauthorized access after offboarding",
        "Better hashing",
        "More phishing",
        "B",
        "Stale, active accounts are prime targets; timely deprovisioning closes that gap.",
    ),
    (
        "Which best describes the principle of least privilege for identities?",
        "Give everyone admin to be efficient",
        "Disable all accounts",
        "Grant each identity only the access it needs, limiting damage from a compromise",
        "Use one shared admin account",
        "C",
        "Least privilege shrinks the blast radius when any single credential is stolen.",
    ),
    (
        "Monitoring for new inbox forwarding rules helps detect:",
        "Disk fragmentation",
        "Slow CPUs",
        "Expired certificates",
        "Account takeover where attackers quietly exfiltrate or hide email",
        "D",
        "Attackers commonly add hidden forwarding/rules after taking over a mailbox; alerting catches this.",
    ),
    (
        "A breach of a hashed password database is far less harmful when hashes are:",
        "Salted and produced by a slow adaptive KDF",
        "Fast and unsalted",
        "Stored as MD5",
        "Reversible",
        "A",
        "Slow, salted hashes dramatically raise the cost of cracking, buying time and protecting most users.",
    ),
    (
        "The core lesson of credential theft defence is:",
        "Passwords alone are sufficient",
        "Combine unique credentials, phishing-resistant MFA, strong server-side hashing, and anomaly detection",
        "Reuse strong passwords everywhere",
        "Disable MFA to reduce friction",
        "B",
        "Layered identity defences address theft, reuse, and abuse together rather than relying on any single control.",
    ),
]

CLOUD_MISCONFIG_CONTENT = """
<section>
  <h2>Cloud Misconfigurations</h2>
  <p>Cloud platforms are secure by design but configurable by default. Most cloud
  breaches are not caused by the provider being hacked - they stem from customer
  misconfigurations: a storage bucket left public, an overly permissive IAM role,
  a management port open to the world. Under the shared responsibility model, the
  provider secures the cloud, but you secure what you put in it.</p>

  <h3>Common misconfigurations</h3>
  <ul>
    <li><strong>Public storage buckets:</strong> object storage set to public
    read/write, exposing sensitive data.</li>
    <li><strong>Overly permissive IAM:</strong> wildcard policies granting more
    access than needed; long-lived access keys.</li>
    <li><strong>Open security groups:</strong> ports such as SSH (22), RDP (3389),
    or databases exposed to 0.0.0.0/0.</li>
    <li><strong>Disabled logging:</strong> no audit trail (for example, cloud
    audit logs turned off).</li>
    <li><strong>Unencrypted data</strong> at rest or in transit.</li>
    <li><strong>Hardcoded secrets</strong> in code, images, or environment
    variables exposed publicly.</li>
    <li><strong>Public access to management interfaces and metadata services</strong>
    (SSRF to the instance metadata endpoint can steal credentials).</li>
  </ul>

  <h3>The shared responsibility model</h3>
  <table class="table">
    <thead>
      <tr><th>Provider secures</th><th>Customer secures</th></tr>
    </thead>
    <tbody>
      <tr><td>Physical data centres</td><td>Identity and access management</td></tr>
      <tr><td>Host hypervisor</td><td>Data classification and encryption config</td></tr>
      <tr><td>Core network hardware</td><td>Network/security group rules</td></tr>
      <tr><td>Managed service availability</td><td>Bucket/object permissions and app config</td></tr>
    </tbody>
  </table>

  <h3>Red flags</h3>
  <ul>
    <li>A bucket policy containing a principal of <em>*</em> with no conditions.</li>
    <li>IAM policies using <em>Action: *</em> and <em>Resource: *</em>.</li>
    <li>Security groups allowing 0.0.0.0/0 to admin ports.</li>
    <li>Access keys committed to a public repository.</li>
  </ul>

  <h3>Defenses</h3>
  <ul>
    <li><strong>Least privilege IAM:</strong> scope actions and resources; prefer
    short-lived roles over static keys.</li>
    <li><strong>Block public access</strong> at the account/bucket level by
    default; enable Public Access Block.</li>
    <li><strong>Encrypt</strong> data at rest and in transit.</li>
    <li><strong>Enable and centralise logging</strong> (audit logs) and alert on
    drift.</li>
    <li><strong>Use CSPM</strong> (Cloud Security Posture Management) to detect
    misconfigurations continuously.</li>
    <li><strong>Infrastructure as code with policy-as-code</strong> guardrails to
    prevent insecure deployments.</li>
    <li><strong>Secrets management</strong> instead of hardcoding; rotate
    regularly.</li>
  </ul>

  <h3>IAM policy: over-permissive vs. least privilege</h3>
  <div class="code-compare">
    <pre class="code-block vulnerable"><code>{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}</code></pre>
    <pre class="code-block secure"><code>{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::reports-bucket/quarterly/*"
}</code></pre>
  </div>

  <section class="exercise" data-exercise="code-review">
    <h3>Quick check: secure or vulnerable?</h3>
    <pre class="code-block"><code>{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::customer-pii/*"
}</code></pre>
    <p>Click your answer:</p>
    <div class="exercise-options">
      <button type="button" class="btn btn-secondary" data-answer="secure">Secure</button>
      <button type="button" class="btn btn-secondary" data-answer="vulnerable" data-correct="true">Vulnerable</button>
    </div>
    <p class="exercise-feedback" hidden></p>
  </section>
</section>
"""

CLOUD_MISCONFIG_QUESTIONS = [
    (
        "Under the cloud shared responsibility model, who secures data classification and access configuration?",
        "The customer",
        "The cloud provider alone",
        "No one",
        "The internet service provider",
        "A",
        "Providers secure the underlying cloud; customers are responsible for how they configure access and protect their data.",
    ),
    (
        "Which is the most common root cause of cloud data exposures?",
        "Providers being hacked directly",
        "Customer misconfigurations such as public buckets and over-permissive IAM",
        "Physical theft of data centres",
        "Lightning strikes",
        "B",
        "The large majority of cloud incidents stem from customer-side misconfiguration, not provider compromise.",
    ),
    (
        "An IAM policy with Action: * and Resource: * is:",
        "Least privilege",
        "Required by all clouds",
        "Over-permissive and risky, granting far more than needed",
        "Encrypted by default",
        "C",
        "Wildcard action and resource grants violate least privilege and dramatically increase blast radius.",
    ),
    (
        "A storage bucket policy with Principal: * and no conditions typically means:",
        "Only you can access it",
        "It is encrypted",
        "It is offline",
        "Anyone on the internet may access the objects",
        "D",
        "A wildcard principal with no condition exposes the bucket publicly, a frequent source of leaks.",
    ),
    (
        "Opening port 3389 (RDP) to 0.0.0.0/0 is dangerous because it:",
        "Exposes remote desktop to the entire internet for attack",
        "Improves performance",
        "Encrypts the connection",
        "Disables logging",
        "A",
        "Exposing admin ports to the world invites brute force and exploitation; restrict to known sources or a VPN.",
    ),
    (
        "The principle of least privilege in IAM means:",
        "Grant all permissions to simplify work",
        "Grant only the specific actions and resources an identity needs",
        "Use one shared root account",
        "Disable IAM entirely",
        "B",
        "Scoping permissions tightly limits what a compromised identity can do.",
    ),
    (
        "Why prefer short-lived roles over long-lived access keys?",
        "Long-lived keys never leak",
        "Roles are slower",
        "Short-lived credentials reduce the window of misuse if exposed",
        "Keys are encrypted and roles are not",
        "C",
        "Temporary credentials expire quickly, shrinking the value of a leaked secret.",
    ),
    (
        "CSPM tools primarily help by:",
        "Writing application code",
        "Replacing the cloud provider",
        "Encrypting user passwords",
        "Continuously detecting cloud misconfigurations and policy drift",
        "D",
        "Cloud Security Posture Management continuously scans configs against best practices and flags risks.",
    ),
    (
        "Hardcoding cloud access keys in a public repository is risky because:",
        "Bots scrape public repos for keys within minutes and abuse them",
        "It speeds up deployment",
        "Keys cannot be used by others",
        "It encrypts the repo",
        "A",
        "Leaked keys in public repos are rapidly harvested and used, often for crypto-mining or data theft.",
    ),
    (
        "Enabling block public access at the account level:",
        "Makes all buckets public",
        "Prevents buckets from being made public even by mistaken policies",
        "Deletes all data",
        "Disables encryption",
        "B",
        "Account-wide public access blocks act as a guardrail against accidental public exposure.",
    ),
    (
        "An SSRF attack against the instance metadata service can:",
        "Only change the hostname",
        "Speed up the instance",
        "Trick a server into fetching and leaking instance credentials",
        "Encrypt the disk",
        "C",
        "If an app is vulnerable to SSRF, attackers may reach the metadata endpoint and steal role credentials.",
    ),
    (
        "Using IMDSv2 (session-based metadata) helps because it:",
        "Removes metadata entirely",
        "Disables IAM",
        "Makes keys permanent",
        "Requires a token, mitigating many SSRF-based credential thefts",
        "D",
        "Token-based metadata access raises the bar against simple SSRF retrieval of credentials.",
    ),
    (
        "Disabling cloud audit logging is dangerous because:",
        "It removes the trail needed to detect and investigate incidents",
        "It saves money with no downside",
        "It speeds up the network",
        "It encrypts data",
        "A",
        "Without audit logs, malicious activity is far harder to detect or reconstruct.",
    ),
    (
        "Encryption at rest protects data primarily when:",
        "The network is fast",
        "Underlying storage media or snapshots are accessed without authorization",
        "Users log in",
        "Logs are disabled",
        "B",
        "At-rest encryption guards against exposure if storage, backups, or snapshots are accessed improperly.",
    ),
    (
        "Infrastructure as code with policy-as-code guardrails helps by:",
        "Allowing any configuration",
        "Removing version control",
        "Blocking insecure configurations before they are deployed",
        "Disabling reviews",
        "C",
        "Policy-as-code enforces security rules automatically in the deployment pipeline, preventing drift and mistakes.",
    ),
    (
        "A least-privilege S3 policy should scope:",
        "Action to * and Resource to *",
        "Principal to * publicly",
        "Nothing at all",
        "Specific actions to specific resource ARNs",
        "D",
        "Granting only needed actions on specific resources follows least privilege and limits exposure.",
    ),
    (
        "Which finding is a clear misconfiguration red flag?",
        "A security group allowing 0.0.0.0/0 to a database port",
        "A database port open only to an internal app subnet",
        "Encryption enabled at rest",
        "Audit logging turned on",
        "A",
        "Exposing a database directly to the entire internet is a serious, common misconfiguration.",
    ),
    (
        "Secrets management services (vaults) are preferred over env vars in images because they:",
        "Are slower",
        "Centralise, encrypt, and rotate secrets without baking them into artifacts",
        "Make secrets public",
        "Remove the need for IAM",
        "B",
        "Dedicated secret stores keep credentials out of images/code and enable rotation and access control.",
    ),
    (
        "Why centralise logs from multiple accounts?",
        "To delete them faster",
        "To make them public",
        "To enable consistent monitoring, correlation, and tamper resistance",
        "To disable alerts",
        "C",
        "Central, protected logging supports detection and investigation across an entire cloud estate.",
    ),
    (
        "A public bucket holding customer PII is best described as:",
        "Secure by default",
        "A performance optimization",
        "Encrypted automatically",
        "A high-severity exposure requiring immediate remediation",
        "D",
        "Publicly readable PII is a critical data exposure that must be locked down right away.",
    ),
    (
        "Configuration drift refers to:",
        "Live resources diverging from the intended secure baseline over time",
        "Faster deployments",
        "Encrypting backups",
        "Rotating keys",
        "A",
        "Drift detection catches changes that move resources away from approved, secure configurations.",
    ),
    (
        "MFA on the cloud root/owner account is important because:",
        "It slows logins for fun",
        "Root has unrestricted control, so its compromise is catastrophic",
        "Root cannot do much",
        "It disables billing",
        "B",
        "The root account can do anything; protecting it with strong MFA is a critical control.",
    ),
    (
        "Why avoid using the root account for daily tasks?",
        "It is faster",
        "Root has no permissions",
        "Daily use increases exposure of an all-powerful credential; use scoped IAM identities instead",
        "It is required by policy",
        "C",
        "Reserving root for rare, critical tasks and using least-privilege identities daily limits risk.",
    ),
    (
        "Encrypting data in transit primarily defends against:",
        "Disk failure",
        "Public buckets",
        "IAM drift",
        "Interception/eavesdropping on the network",
        "D",
        "TLS/encryption in transit prevents attackers from reading or tampering with data on the wire.",
    ),
    (
        "A wildcard IAM trust policy that any account can assume is risky because:",
        "Untrusted external accounts could assume the role and gain access",
        "It is encrypted",
        "It limits access",
        "It improves logging",
        "A",
        "Overly broad trust relationships can let unintended principals assume privileged roles.",
    ),
    (
        "Tagging and inventory of cloud resources help security by:",
        "Hiding resources",
        "Providing visibility so misconfigured or forgotten assets can be found and fixed",
        "Disabling encryption",
        "Removing IAM",
        "B",
        "You cannot secure what you cannot see; inventory and tagging surface risky or orphaned resources.",
    ),
    (
        "Which best reduces the impact of a leaked long-lived key?",
        "Never rotating it",
        "Posting it publicly",
        "Automated detection plus prompt rotation/revocation and least-privilege scoping",
        "Granting it admin",
        "C",
        "Detecting, revoking, and tightly scoping keys limits the damage from a leak.",
    ),
    (
        "Public access block, least-privilege IAM, encryption, and logging together represent:",
        "An overreaction",
        "A single point of failure",
        "Unnecessary complexity",
        "A layered, defense-in-depth approach to cloud configuration",
        "D",
        "Combining guardrails across identity, data, network, and visibility provides resilient cloud security.",
    ),
    (
        "Why is least privilege especially important for service/automation accounts?",
        "They often hold standing access and run unattended, so over-permissioning is high risk",
        "They never get compromised",
        "They cannot be scoped",
        "They require admin",
        "A",
        "Automation identities run continuously; excessive permissions make them valuable, high-impact targets.",
    ),
    (
        "The central takeaway about cloud misconfigurations is:",
        "The provider is responsible for all your settings",
        "Secure configuration is the customer's job and the leading cause of cloud breaches when neglected",
        "Cloud cannot be secured",
        "Encryption alone solves everything",
        "B",
        "Most cloud breaches trace to customer misconfiguration, so disciplined, least-privilege configuration is essential.",
    ),
]

BEC_CONTENT = """
<section>
  <h2>Social Engineering and Business Email Compromise (BEC)</h2>
  <p>Social engineering attacks the human, not the machine. Business Email
  Compromise (BEC) is a high-impact form of social engineering where attackers
  impersonate a trusted party - a CEO, a vendor, an attorney - to trick
  employees into wiring money or sharing sensitive data. BEC rarely uses malware,
  which makes it hard to catch with technical filters alone.</p>

  <h3>How BEC works</h3>
  <ul>
    <li><strong>Reconnaissance:</strong> attackers study the organisation,
    leadership, and vendors using public sources and social media.</li>
    <li><strong>Impersonation:</strong> via spoofed display names, lookalike
    domains (rn vs m), or a genuinely compromised account.</li>
    <li><strong>Pretext and urgency:</strong> a believable story plus time
    pressure ("the deal closes today, wire it now").</li>
    <li><strong>The ask:</strong> a wire transfer, a change of vendor bank
    details, gift cards, or payroll redirection.</li>
  </ul>

  <h3>Common BEC scenarios</h3>
  <ul>
    <li><strong>CEO fraud:</strong> a fake executive demands an urgent
    confidential payment.</li>
    <li><strong>Vendor/invoice fraud:</strong> an attacker emails updated banking
    details for an outstanding invoice.</li>
    <li><strong>Payroll diversion:</strong> a fake employee asks HR to change
    direct-deposit details.</li>
    <li><strong>Account compromise:</strong> a real, hijacked mailbox sends the
    fraudulent request from inside.</li>
  </ul>

  <h3>Psychological levers and red flags</h3>
  <ul>
    <li><strong>Authority:</strong> pressure from a senior figure.</li>
    <li><strong>Urgency and secrecy:</strong> "do not tell anyone, do it now".</li>
    <li><strong>Plausibility:</strong> correct names, branding, and timing.</li>
    <li><strong>Red flags:</strong> reply-to differs from sender; lookalike
    domain; first-time payee; change of bank details by email; refusal to take a
    phone call.</li>
  </ul>

  <h3>Defenses</h3>
  <ul>
    <li><strong>Out-of-band verification:</strong> confirm payment/bank-change
    requests via a known phone number, never the contact in the email.</li>
    <li><strong>Dual authorization</strong> for wire transfers above a threshold.</li>
    <li><strong>Email authentication:</strong> SPF, DKIM, and DMARC to reduce
    spoofing.</li>
    <li><strong>Banner external emails</strong> and flag lookalike domains.</li>
    <li><strong>Security awareness training</strong> and simulated phishing.</li>
    <li><strong>Vendor master data controls:</strong> verify bank-detail changes
    through an established process.</li>
  </ul>

  <table class="table">
    <thead>
      <tr><th>Scenario</th><th>Lure</th><th>Best defense</th></tr>
    </thead>
    <tbody>
      <tr><td>CEO fraud</td><td>Authority + urgency</td><td>Out-of-band verification</td></tr>
      <tr><td>Invoice fraud</td><td>Bank-detail change</td><td>Verified vendor change process</td></tr>
      <tr><td>Payroll diversion</td><td>Deposit change request</td><td>Identity verification + callback</td></tr>
      <tr><td>Spoofed domain</td><td>Lookalike sender</td><td>DMARC + external banner</td></tr>
    </tbody>
  </table>

  <section class="exercise" data-exercise="scenario">
    <h3>Scenario: An urgent email from your CEO asks you to wire funds to a new account before end of day and keep it confidential. What is the safe response?</h3>
    <p><em>The message uses the CEO's name, sounds urgent, and discourages you from discussing it with anyone.</em></p>
    <div class="exercise-options">
      <button type="button" class="btn btn-secondary" data-answer="unsafe">Wire the funds immediately to avoid disappointing the CEO</button>
      <button type="button" class="btn btn-secondary" data-answer="safe" data-correct="true">Verify out-of-band via a known phone number and follow dual-authorization before any transfer</button>
    </div>
    <p class="exercise-feedback" hidden></p>
  </section>
</section>
"""

BEC_QUESTIONS = [
    (
        "What is Business Email Compromise (BEC)?",
        "A scam where attackers impersonate trusted parties to trick staff into payments or data disclosure",
        "A virus that encrypts email servers",
        "A type of spam filter",
        "A backup failure",
        "A",
        "BEC uses impersonation and social engineering, usually to redirect payments, often without any malware.",
    ),
    (
        "Why is BEC hard to stop with technical filters alone?",
        "It always contains malware",
        "It often uses plain text and legitimate-looking email with no malicious attachment",
        "It only targets servers",
        "It is encrypted end to end",
        "B",
        "Because BEC relies on words and trust rather than payloads, signature/AV filters frequently miss it.",
    ),
    (
        "The single most effective defence against payment-redirection BEC is:",
        "Replying to the email to confirm",
        "Approving faster to save time",
        "Out-of-band verification using a known, trusted phone number",
        "Disabling SPF",
        "C",
        "Verifying through an independent, pre-known channel defeats impersonation since the attacker does not control it.",
    ),
    (
        "CEO fraud typically relies on the psychological lever of:",
        "Boredom",
        "Generosity",
        "Curiosity about cats",
        "Authority combined with urgency",
        "D",
        "Impersonating a senior leader pressures employees to comply quickly without questioning.",
    ),
    (
        "A lookalike domain attack uses:",
        "A confusingly similar domain such as rn substituted for m",
        "The exact legitimate domain",
        "No domain at all",
        "Only numeric domains",
        "A",
        "Visually similar domains trick recipients into trusting a spoofed sender.",
    ),
    (
        "Invoice/vendor fraud most often involves:",
        "A free software download",
        "A request to change the vendor's bank account details",
        "A password reset",
        "A network scan",
        "B",
        "Attackers send updated banking details so future or outstanding payments go to them.",
    ),
    (
        "Dual authorization for wire transfers means:",
        "One person can approve anything",
        "No approval is needed",
        "Two authorized people must independently approve a transfer above a threshold",
        "The bank approves automatically",
        "C",
        "Requiring two approvers makes a single tricked employee insufficient to release funds.",
    ),
    (
        "DMARC, working with SPF and DKIM, helps by:",
        "Encrypting attachments",
        "Speeding up email delivery",
        "Blocking all external email",
        "Reducing domain spoofing and instructing receivers how to handle failures",
        "D",
        "DMARC builds on SPF/DKIM to authenticate senders and curb spoofing of your domain.",
    ),
    (
        "Payroll diversion fraud targets:",
        "HR/payroll, requesting a change to an employee's direct-deposit details",
        "The firewall",
        "The DNS server",
        "The printer queue",
        "A",
        "Attackers impersonate employees to redirect salary payments to attacker-controlled accounts.",
    ),
    (
        "Which is a strong BEC red flag?",
        "A long-standing vendor with unchanged details",
        "A first-time payee plus an urgent request to change bank details by email",
        "An internal memo with no money involved",
        "A routine newsletter",
        "B",
        "New payees and email-only bank changes under time pressure are classic BEC indicators.",
    ),
    (
        "Why do attackers often add secrecy (do not tell anyone) to BEC requests?",
        "To be polite",
        "To improve email formatting",
        "To prevent the target from verifying with colleagues who might spot the fraud",
        "To comply with regulations",
        "C",
        "Discouraging discussion blocks the very verification that would expose the scam.",
    ),
    (
        "Reconnaissance in BEC commonly uses:",
        "Only random guessing",
        "Physical break-ins",
        "Nothing at all",
        "Public sources and social media to learn names, roles, and vendor relationships",
        "D",
        "Open-source intelligence lets attackers craft convincing, well-targeted pretexts.",
    ),
    (
        "An external email banner helps by:",
        "Reminding recipients that a message claiming to be internal actually came from outside",
        "Blocking internal mail",
        "Encrypting the message",
        "Deleting attachments",
        "A",
        "Banners cue caution when an apparent internal sender is really external, a hallmark of spoofing.",
    ),
    (
        "If a real vendor mailbox is compromised, the fraudulent request:",
        "Will always fail SPF",
        "Comes from a legitimate address, so out-of-band verification is even more important",
        "Is harmless",
        "Cannot ask for money",
        "B",
        "Account compromise means email authentication passes, so independent verification is the key safeguard.",
    ),
    (
        "Gift card scams are a BEC variant where attackers ask victims to:",
        "Install antivirus",
        "Reset their router",
        "Buy gift cards and send the codes urgently",
        "Update a spreadsheet",
        "C",
        "Requests to buy and send gift card codes under urgency are a common, low-tech BEC fraud.",
    ),
    (
        "Pretexting refers to:",
        "Encrypting an email",
        "A password policy",
        "A type of firewall",
        "Creating a fabricated but believable scenario to manipulate the target",
        "D",
        "A convincing backstory (the pretext) makes the malicious request feel legitimate.",
    ),
    (
        "Why verify bank-detail changes through an established vendor process?",
        "It ensures changes are confirmed via controlled channels, not just an email claim",
        "It is slower for no reason",
        "It removes the need for invoices",
        "It disables payments entirely",
        "A",
        "Formal change controls with verification prevent attackers from quietly rerouting payments.",
    ),
    (
        "Spoofing the display name (but not the address) exploits the fact that:",
        "Addresses are always visible",
        "Many email clients show only the friendly name, hiding the real address",
        "Display names are encrypted",
        "Names cannot be faked",
        "B",
        "Recipients often trust the displayed name without checking the underlying address.",
    ),
    (
        "Simulated phishing exercises help organisations by:",
        "Punishing employees",
        "Sending real malware",
        "Safely training staff to recognise and report social-engineering attempts",
        "Replacing email filters",
        "C",
        "Practice with realistic, safe simulations builds recognition and reporting habits.",
    ),
    (
        "The best response to an urgent confidential CEO wire request is to:",
        "Wire immediately to avoid delay",
        "Reply-all asking for confirmation",
        "Forward it to the attacker",
        "Verify via a known phone number and follow dual authorization before acting",
        "D",
        "Independent verification plus dual control stops impersonation-driven payment fraud.",
    ),
    (
        "A reply-to address that differs from the visible sender is suspicious because:",
        "Replies may be silently routed to the attacker instead of the real person",
        "It always indicates encryption",
        "It speeds up replies",
        "It is required by DMARC",
        "A",
        "Mismatched reply-to fields let attackers intercept responses, a common BEC trick.",
    ),
    (
        "Why is urgency such an effective social-engineering lever?",
        "It relaxes the victim",
        "It pressures targets to act before they think critically or verify",
        "It improves accuracy",
        "It has no effect",
        "B",
        "Time pressure short-circuits careful verification, exactly what attackers want.",
    ),
    (
        "Which control most directly limits damage if one employee is fooled by BEC?",
        "Faster email",
        "Disabling MFA",
        "Dual authorization and out-of-band verification for payments",
        "Bigger mailboxes",
        "C",
        "Process controls ensure a single deceived person cannot unilaterally release funds.",
    ),
    (
        "Whaling is a form of phishing that:",
        "Targets random consumers",
        "Only uses SMS",
        "Targets printers",
        "Specifically targets high-value executives",
        "D",
        "Whaling focuses on senior leaders whose authority and access make them lucrative targets.",
    ),
    (
        "Vishing in a BEC context is:",
        "Voice-based social engineering, for example a phone call impersonating an executive",
        "A type of VPN",
        "A spam filter",
        "A backup method",
        "A",
        "Attackers may call to add pressure or legitimacy, sometimes using cloned or deepfaked voices.",
    ),
    (
        "A genuinely effective response when a request feels off is to:",
        "Comply quietly",
        "Pause, independently verify, and report it through the proper channel",
        "Delete it and tell no one",
        "Approve it to be safe",
        "B",
        "Slowing down to verify and report breaks the attacker's reliance on speed and silence.",
    ),
    (
        "Why are publicly posted out-of-office and org-chart details useful to BEC attackers?",
        "They are never useful",
        "They encrypt mail",
        "They reveal who is away and who reports to whom, improving impersonation timing and targeting",
        "They block spoofing",
        "C",
        "Knowing absences and reporting lines helps attackers pick believable senders and moments.",
    ),
    (
        "Which statement about BEC financial impact is accurate?",
        "It is negligible",
        "It only affects individuals",
        "It never involves wire transfers",
        "BEC is among the costliest cybercrime categories by reported losses",
        "D",
        "BEC consistently ranks among the highest-loss cybercrime categories due to large fraudulent transfers.",
    ),
    (
        "Confirming a payment request by calling the number printed in the suspicious email is:",
        "Unsafe, because the attacker may have supplied a number they control",
        "A reliable verification method",
        "Required by DMARC",
        "The only valid option",
        "A",
        "Verification must use a known, independent contact, not details provided within the suspect message.",
    ),
    (
        "The core principle for defeating social engineering and BEC is:",
        "Trust urgent authority unconditionally",
        "Verify independently, slow down, and use process controls rather than reacting to pressure",
        "Rely only on spam filters",
        "Keep all requests secret",
        "B",
        "Independent verification, deliberate process, and a healthy skepticism toward urgency defeat human-targeted fraud.",
    ),
]

MODULES = [
    {
        "title": "Supply Chain Attacks",
        "description": "How attackers compromise organisations through trusted vendors, dependencies, and build pipelines, and how to defend the software and hardware supply chain.",
        "category": "Third-Party Risk",
        "order": 12,
        "content": SUPPLY_CHAIN_CONTENT,
        "questions": SUPPLY_CHAIN_QUESTIONS,
    },
    {
        "title": "Zero-Day Exploits",
        "description": "Understanding unknown, unpatched vulnerabilities, how exploits are discovered and weaponised, and layered defences that limit their impact.",
        "category": "Vulnerability Management",
        "order": 13,
        "content": ZERO_DAY_CONTENT,
        "questions": ZERO_DAY_QUESTIONS,
    },
    {
        "title": "Credential Theft & Identity Abuse",
        "description": "How credentials are stolen and abused through stuffing, spraying, token theft, and MFA fatigue, and the identity controls that stop them.",
        "category": "Identity & Access",
        "order": 14,
        "content": CREDENTIAL_THEFT_CONTENT,
        "questions": CREDENTIAL_THEFT_QUESTIONS,
    },
    {
        "title": "Cloud Misconfigurations",
        "description": "The most common cloud security mistakes - public buckets, over-permissive IAM, open ports - and how the shared responsibility model and guardrails prevent them.",
        "category": "Cloud Security",
        "order": 15,
        "content": CLOUD_MISCONFIG_CONTENT,
        "questions": CLOUD_MISCONFIG_QUESTIONS,
    },
    {
        "title": "Social Engineering & Business Email Compromise (BEC)",
        "description": "How attackers manipulate people and impersonate trusted parties to redirect payments and data, and the verification and process controls that defeat them.",
        "category": "Human Risk",
        "order": 16,
        "content": BEC_CONTENT,
        "questions": BEC_QUESTIONS,
    },
]
