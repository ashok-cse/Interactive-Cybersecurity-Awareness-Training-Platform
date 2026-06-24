/**
 * CyberAware Platform — charts.js
 *
 * Reads JSON from <script id="chart-data" type="application/json"> and
 * renders four Chart.js charts into their respective canvas elements.
 *
 * Canvas IDs (must match exactly — per CONTRACT.md):
 *   completionChart  — bar,      completion.labels / completion.values (%)
 *   avgScoreChart    — bar,      avg_scores.labels / avg_scores.values
 *   passFailChart    — doughnut, pass_fail.passed / pass_fail.failed
 *   phishingChart    — doughnut, phishing.correct / phishing.incorrect / phishing.pending
 *
 * Chart.js is loaded via CDN in base.html before this script runs.
 * Everything is guarded so missing canvases or missing data keys are silently skipped.
 */

(function () {
  "use strict";

  /* ── Palette ─────────────────────────────────────────────── */
  var COLORS = {
    teal:       "rgba( 14, 165, 233, 0.80)",
    tealBorder: "rgba( 14, 165, 233, 1.00)",
    indigo:     "rgba( 99, 102, 241, 0.80)",
    indigoBorder: "rgba( 99, 102, 241, 1.00)",
    success:    "rgba( 34, 197,  94, 0.85)",
    successBorder: "rgba( 34, 197,  94, 1.00)",
    danger:     "rgba(239,  68,  68, 0.85)",
    dangerBorder:  "rgba(239,  68,  68, 1.00)",
    warning:    "rgba(245, 158,  11, 0.85)",
    warningBorder: "rgba(245, 158,  11, 1.00)",
    muted:      "rgba(148, 163, 184, 0.70)",
    mutedBorder:   "rgba(148, 163, 184, 1.00)"
  };

  /* ── Shared default options ──────────────────────────────── */
  var defaultFontColor = "#1e293b";

  var barDefaults = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {}
      }
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: defaultFontColor, font: { size: 11 } }
      },
      y: {
        beginAtZero: true,
        grid: { color: "rgba(0,0,0,.06)" },
        ticks: { color: defaultFontColor, font: { size: 11 } }
      }
    }
  };

  var doughnutDefaults = {
    responsive: true,
    maintainAspectRatio: true,
    cutout: "60%",
    plugins: {
      legend: {
        position: "bottom",
        labels: { color: defaultFontColor, font: { size: 12 }, padding: 16 }
      }
    }
  };

  /* ── Helper: get canvas context safely ──────────────────── */
  function getCtx(id) {
    var el = document.getElementById(id);
    if (!el || el.tagName.toLowerCase() !== "canvas") return null;
    return el.getContext("2d");
  }

  /* ── Helper: deep-merge options (shallow for nested objs) ── */
  function mergeOptions(base, overrides) {
    var merged = JSON.parse(JSON.stringify(base));
    if (!overrides) return merged;
    // Simple top-level + one-level deep merge
    Object.keys(overrides).forEach(function (k) {
      if (
        overrides[k] !== null &&
        typeof overrides[k] === "object" &&
        !Array.isArray(overrides[k]) &&
        typeof merged[k] === "object" &&
        merged[k] !== null
      ) {
        merged[k] = mergeOptions(merged[k], overrides[k]);
      } else {
        merged[k] = overrides[k];
      }
    });
    return merged;
  }

  /* ── 1. Completion Rate bar chart ────────────────────────── */
  function renderCompletionChart(data) {
    var ctx = getCtx("completionChart");
    if (!ctx) return;

    var completion = data.completion;
    if (!completion || !Array.isArray(completion.labels) || !Array.isArray(completion.values)) return;

    var opts = mergeOptions(barDefaults, {
      scales: {
        y: {
          max: 100,
          ticks: {
            callback: function (v) { return v + "%"; }
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (ctx) { return ctx.parsed.y + "% complete"; }
          }
        },
        title: {
          display: false
        }
      }
    });

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: completion.labels,
        datasets: [{
          label: "Completion %",
          data: completion.values,
          backgroundColor: COLORS.teal,
          borderColor: COLORS.tealBorder,
          borderWidth: 1,
          borderRadius: 4
        }]
      },
      options: opts
    });
  }

  /* ── 2. Average Scores bar chart ─────────────────────────── */
  function renderAvgScoreChart(data) {
    var ctx = getCtx("avgScoreChart");
    if (!ctx) return;

    var avgScores = data.avg_scores;
    if (!avgScores || !Array.isArray(avgScores.labels) || !Array.isArray(avgScores.values)) return;

    var opts = mergeOptions(barDefaults, {
      scales: {
        y: {
          max: 100,
          ticks: {
            callback: function (v) { return v; }
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (ctx) { return "Avg score: " + ctx.parsed.y; }
          }
        }
      }
    });

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: avgScores.labels,
        datasets: [{
          label: "Average Score",
          data: avgScores.values,
          backgroundColor: COLORS.indigo,
          borderColor: COLORS.indigoBorder,
          borderWidth: 1,
          borderRadius: 4
        }]
      },
      options: opts
    });
  }

  /* ── 3. Pass / Fail doughnut chart ───────────────────────── */
  function renderPassFailChart(data) {
    var ctx = getCtx("passFailChart");
    if (!ctx) return;

    var pf = data.pass_fail;
    if (!pf || pf.passed === undefined || pf.failed === undefined) return;

    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Passed", "Failed"],
        datasets: [{
          data: [pf.passed, pf.failed],
          backgroundColor: [COLORS.success, COLORS.danger],
          borderColor: [COLORS.successBorder, COLORS.dangerBorder],
          borderWidth: 1
        }]
      },
      options: mergeOptions(doughnutDefaults, {
        plugins: {
          tooltip: {
            callbacks: {
              label: function (ctx) {
                var total = ctx.dataset.data.reduce(function (a, b) { return a + b; }, 0);
                var pct   = total > 0 ? Math.round(ctx.parsed / total * 100) : 0;
                return ctx.label + ": " + ctx.parsed + " (" + pct + "%)";
              }
            }
          }
        }
      })
    });
  }

  /* ── 4. Phishing awareness doughnut chart ────────────────── */
  function renderPhishingChart(data) {
    var ctx = getCtx("phishingChart");
    if (!ctx) return;

    var ph = data.phishing;
    if (!ph || ph.correct === undefined || ph.incorrect === undefined || ph.pending === undefined) return;

    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Correctly identified", "Incorrectly identified", "Pending"],
        datasets: [{
          data: [ph.correct, ph.incorrect, ph.pending],
          backgroundColor: [COLORS.success, COLORS.danger, COLORS.muted],
          borderColor: [COLORS.successBorder, COLORS.dangerBorder, COLORS.mutedBorder],
          borderWidth: 1
        }]
      },
      options: mergeOptions(doughnutDefaults, {
        plugins: {
          tooltip: {
            callbacks: {
              label: function (ctx) {
                var total = ctx.dataset.data.reduce(function (a, b) { return a + b; }, 0);
                var pct   = total > 0 ? Math.round(ctx.parsed / total * 100) : 0;
                return ctx.label + ": " + ctx.parsed + " (" + pct + "%)";
              }
            }
          }
        }
      })
    });
  }

  /* ── Bootstrap ───────────────────────────────────────────── */
  document.addEventListener("DOMContentLoaded", function () {
    // Guard: Chart.js must be loaded
    if (typeof Chart === "undefined") {
      console.warn("charts.js: Chart.js not found — charts will not render.");
      return;
    }

    // Guard: data element must exist
    var dataEl = document.getElementById("chart-data");
    if (!dataEl) return; // Not on the analytics page — silent exit

    var chartData;
    try {
      chartData = JSON.parse(dataEl.textContent);
    } catch (e) {
      console.error("charts.js: Failed to parse #chart-data JSON.", e);
      return;
    }

    if (!chartData || typeof chartData !== "object") return;

    // Render each chart independently so one failure doesn't block others
    try { renderCompletionChart(chartData); } catch (e) { console.error("completionChart error:", e); }
    try { renderAvgScoreChart(chartData);   } catch (e) { console.error("avgScoreChart error:", e); }
    try { renderPassFailChart(chartData);   } catch (e) { console.error("passFailChart error:", e); }
    try { renderPhishingChart(chartData);   } catch (e) { console.error("phishingChart error:", e); }
  });

})();
