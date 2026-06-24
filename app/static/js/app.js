/**
 * CyberAware Platform — app.js
 *
 * Vanilla JS; runs on DOMContentLoaded.
 * No external dependencies (Chart.js is handled separately in charts.js).
 *
 * Features:
 *  1. Auto-dismiss .alert flash messages after 5 s.
 *  2. Logout confirmation dialog.
 *  3. Mobile sidebar toggle via [data-sidebar-toggle].
 *  4. Interactive exercises:
 *       - [data-exercise="code-review"]   — click an answer button, compare to data-correct.
 *       - [data-exercise="scenario"]      — safe/unsafe choice with inline feedback.
 *       - [data-exercise="threat"]        — STRIDE checkbox check with result reveal.
 */

(function () {
  "use strict";

  /* ── 1. Auto-dismiss flash alerts ─────────────────────────── */
  function initAlerts() {
    var alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (el) {
      setTimeout(function () {
        el.classList.add("fade-out");
        // Remove from DOM after the CSS transition ends
        el.addEventListener("transitionend", function () {
          if (el.parentNode) el.parentNode.removeChild(el);
        });
      }, 5000);
    });
  }

  /* ── 2. Logout confirmation ────────────────────────────────── */
  function initLogoutConfirm() {
    // Handles both [data-confirm-logout] on a form and on a button
    document.querySelectorAll("[data-confirm-logout]").forEach(function (el) {
      el.addEventListener("submit", function (e) {
        if (!window.confirm("Are you sure you want to log out?")) {
          e.preventDefault();
        }
      });
    });
  }

  /* ── 3. Mobile sidebar toggle ──────────────────────────────── */
  function initSidebarToggle() {
    var toggleBtn = document.querySelector("[data-sidebar-toggle]");
    var sidebar   = document.querySelector(".sidebar");
    if (!toggleBtn || !sidebar) return;

    // Create backdrop element if not already present
    var backdrop = document.querySelector(".sidebar-backdrop");
    if (!backdrop) {
      backdrop = document.createElement("div");
      backdrop.className = "sidebar-backdrop";
      document.body.appendChild(backdrop);
    }

    function openSidebar() {
      sidebar.classList.add("open");
      backdrop.classList.add("visible");
      document.body.style.overflow = "hidden";
    }

    function closeSidebar() {
      sidebar.classList.remove("open");
      backdrop.classList.remove("visible");
      document.body.style.overflow = "";
    }

    toggleBtn.addEventListener("click", function () {
      if (sidebar.classList.contains("open")) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });

    backdrop.addEventListener("click", closeSidebar);

    // Close sidebar on nav link click (for SPA-like feel)
    sidebar.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeSidebar);
    });
  }

  /* ── 3b. Light / dark theme toggle ─────────────────────────── */
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem("cyberaware-theme", theme); } catch (e) {}
  }

  function initThemeToggle() {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var current = document.documentElement.getAttribute("data-theme") === "dark"
          ? "dark" : "light";
        applyTheme(current === "dark" ? "light" : "dark");
      });
    });
  }

  /* Resolve the correct answer for a button-based exercise.
     Supports both conventions:
       - [data-correct] on the container (e.g. "secure")
       - [data-correct] (truthy) on the winning [data-answer] button */
  function resolveCorrectAnswer(container, buttons) {
    var fromContainer = (container.getAttribute("data-correct") || "").trim().toLowerCase();
    if (fromContainer) return fromContainer;
    var winner = null;
    buttons.forEach(function (b) {
      if (b.hasAttribute("data-correct")) {
        var v = (b.getAttribute("data-correct") || "").trim().toLowerCase();
        if (v !== "false" && v !== "0" && v !== "no") winner = b;
      }
    });
    return winner ? (winner.getAttribute("data-answer") || "").trim().toLowerCase() : "";
  }

  function showFeedback(feedback, ok, text) {
    if (!feedback) return;
    feedback.removeAttribute("hidden");
    feedback.classList.remove("correct", "incorrect");
    feedback.textContent = text;
    feedback.classList.add(ok ? "correct" : "incorrect");
  }

  /* ── 4a. Code-review exercise ──────────────────────────────── */
  /**
   * Markup contract (from CONTRACT.md):
   *   <div data-exercise="code-review" data-correct="secure">
   *     <button data-answer="secure">Mark as Secure</button>
   *     <button data-answer="vulnerable">Mark as Vulnerable</button>
   *     <div class="exercise-feedback"></div>
   *   </div>
   *
   * Behaviour: click a [data-answer] button → compare its value against
   * the container's [data-correct] value → show feedback; disable all
   * answer buttons so the widget can't be re-answered.
   */
  function initCodeReviewExercises() {
    document.querySelectorAll('[data-exercise="code-review"]').forEach(function (container) {
      var buttons  = container.querySelectorAll("[data-answer]");
      var feedback = container.querySelector(".exercise-feedback");
      var correct  = resolveCorrectAnswer(container, buttons);

      if (!buttons.length) return; // nothing to wire

      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var answer = (btn.getAttribute("data-answer") || "").trim().toLowerCase();
          var isCorrect = (answer === correct);

          showFeedback(feedback, isCorrect, isCorrect
            ? "Correct! Good eye."
            : "Not quite — the correct answer is: " + correct + ".");

          // Visual highlight on the clicked button
          buttons.forEach(function (b) {
            b.disabled = true;
            b.style.opacity = "0.6";
          });
          btn.style.opacity = "1";
          btn.style.outline = isCorrect
            ? "2px solid var(--success)"
            : "2px solid var(--danger)";
        });
      });
    });
  }

  /* ── 4b. Scenario exercise ─────────────────────────────────── */
  /**
   * Markup contract:
   *   <div data-exercise="scenario" data-correct="safe">
   *     <button data-answer="safe">This is safe</button>
   *     <button data-answer="unsafe">This is unsafe</button>
   *     <div class="exercise-feedback"></div>
   *   </div>
   *
   * Behaviour: identical to code-review — compare [data-answer] to
   * [data-correct] and display inline feedback.
   */
  function initScenarioExercises() {
    document.querySelectorAll('[data-exercise="scenario"]').forEach(function (container) {
      var buttons  = container.querySelectorAll("[data-answer]");
      var feedback = container.querySelector(".exercise-feedback");
      var correct  = resolveCorrectAnswer(container, buttons);

      if (!buttons.length) return;

      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var answer    = (btn.getAttribute("data-answer") || "").trim().toLowerCase();
          var isCorrect = (answer === correct);

          showFeedback(feedback, isCorrect, isCorrect
            ? "Correct! You identified the scenario accurately."
            : "Incorrect — this scenario is actually: " + correct + ".");

          buttons.forEach(function (b) {
            b.disabled = true;
            b.style.opacity = "0.6";
          });
          btn.style.opacity = "1";
          btn.style.outline = isCorrect
            ? "2px solid var(--success)"
            : "2px solid var(--danger)";
        });
      });
    });
  }

  /* ── 4c. Threat / STRIDE identification exercise ───────────── */
  /**
   * Markup contract:
   *   <div data-exercise="threat" data-correct="Spoofing,Tampering">
   *     <ul class="stride-list">
   *       <li class="stride-item">
   *         <label><input type="checkbox" value="Spoofing"> Spoofing</label>
   *       </li>
   *       ...
   *     </ul>
   *     <button class="btn btn-primary" data-check>Check Answers</button>
   *     <div class="exercise-feedback"></div>
   *   </div>
   *
   * [data-correct] is a comma-separated list of the correct STRIDE
   * categories (case-insensitive comparison).
   *
   * On check:
   *  - Each stride-item gets a class: correct-pick / wrong-pick / missed-pick.
   *  - correct-pick  = user checked it AND it was correct.
   *  - wrong-pick    = user checked it AND it was wrong.
   *  - missed-pick   = user didn't check it AND it was correct.
   *  - Feedback div shows a summary.
   */
  function initThreatExercises() {
    document.querySelectorAll('[data-exercise="threat"]').forEach(function (container) {
      var correctAttr = container.getAttribute("data-correct") || "";
      var correctSet  = correctAttr.split(",").map(function (s) {
        return s.trim().toLowerCase();
      }).filter(Boolean);

      var checkBtn  = container.querySelector("[data-check], [data-action='check']");
      var feedback  = container.querySelector(".exercise-feedback");
      var checkboxes = container.querySelectorAll('input[type="checkbox"]');

      if (!checkBtn || !checkboxes.length) return;

      // Resolve which boxes are correct: per-checkbox [data-correct] OR
      // container [data-correct] comma list matched on value/data-answer.
      function isAnswerCorrect(cb) {
        if (cb.hasAttribute("data-correct")) {
          var v = (cb.getAttribute("data-correct") || "").trim().toLowerCase();
          return v !== "" && v !== "false" && v !== "0" && v !== "no";
        }
        var key = (cb.value || cb.getAttribute("data-answer") || "").trim().toLowerCase();
        return correctSet.indexOf(key) !== -1;
      }

      // Total number of correct options (for the "perfect" check).
      var totalCorrect = 0;
      checkboxes.forEach(function (cb) { if (isAnswerCorrect(cb)) totalCorrect++; });

      checkBtn.addEventListener("click", function () {
        var correct = 0, wrong = 0, missed = 0;

        checkboxes.forEach(function (cb) {
          var item = cb.closest(".stride-item") || cb.closest("label") || cb.parentElement;
          var isCorrect = isAnswerCorrect(cb);

          if (item) item.classList.remove("correct-pick", "wrong-pick", "missed-pick");

          if (cb.checked && isCorrect) {
            if (item) item.classList.add("correct-pick");
            correct++;
          } else if (cb.checked && !isCorrect) {
            if (item) item.classList.add("wrong-pick");
            wrong++;
          } else if (!cb.checked && isCorrect) {
            if (item) item.classList.add("missed-pick");
            missed++;
          }
        });

        var allRight = (correct === totalCorrect && wrong === 0 && missed === 0);
        if (allRight) {
          showFeedback(feedback, true, "Perfect! You identified all threats correctly.");
        } else {
          var parts = [];
          if (correct > 0) parts.push(correct + " correct");
          if (wrong   > 0) parts.push(wrong   + " wrong");
          if (missed  > 0) parts.push(missed  + " missed");
          showFeedback(feedback, false, "Results: " + parts.join(", ") + ". "
            + (missed > 0 ? "Highlighted items show what you missed." : ""));
        }

        checkBtn.disabled  = true;
        checkBtn.textContent = "Checked";
      });
    });
  }

  /* ── 5. Animated progress bars ─────────────────────────────── */
  /**
   * Finds .progress-bar elements that carry a data-width attribute
   * (set by templates as data-width="70") and animates them to that
   * width on page load. Inline style="width:X%" also works directly
   * without JS, but this provides a smoother entrance animation.
   */
  function initProgressBars() {
    document.querySelectorAll(".progress-bar[data-width]").forEach(function (bar) {
      var target = parseInt(bar.getAttribute("data-width"), 10);
      if (isNaN(target)) return;
      // Start from 0 for the animation
      bar.style.width = "0%";
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          bar.style.width = Math.min(Math.max(target, 0), 100) + "%";
        });
      });
    });
  }

  /* ── Bootstrap all on DOMContentLoaded ────────────────────── */
  document.addEventListener("DOMContentLoaded", function () {
    initAlerts();
    initLogoutConfirm();
    initSidebarToggle();
    initThemeToggle();
    initCodeReviewExercises();
    initScenarioExercises();
    initThreatExercises();
    initProgressBars();
  });

})();
