/* ==========================================================================
   PRANAV'S RAMEN & CODE — MAIN CONTROLLER (script.js)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  runLoadingScreen();
  initModals();
  initAudioToggle();
});

/* --------------------------------------------------------------------------
   1. LOADING SCREEN — fake progress bar, then START button
   -------------------------------------------------------------------------- */
function runLoadingScreen() {
  const progressEl = document.getElementById('progressPercentage');
  const startBtn   = document.getElementById('startBtn');
  const cooking    = document.getElementById('cooking');

  let pct = 0;
  const interval = setInterval(() => {
    pct += Math.floor(Math.random() * 12) + 4;
    if (pct >= 100) {
      pct = 100;
      clearInterval(interval);
      if (progressEl) progressEl.textContent = '100';
      // Show START button
      if (startBtn) startBtn.style.display = 'block';
    } else {
      if (progressEl) progressEl.textContent = pct;
    }
  }, 120);

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      // 1. Hide loading screen
      if (cooking) cooking.classList.add('loaded');

      // 2. Init Three.js scene (loads GLTF in background)
      if (window.initThreeScene) window.initThreeScene();

      // 3. Trigger camera fly-in after a short delay
      setTimeout(() => {
        if (window.startCameraEntry) window.startCameraEntry();
      }, 300);
    });
  }
}

/* --------------------------------------------------------------------------
   2. RETRO MODAL SYSTEM
   -------------------------------------------------------------------------- */
function initModals() {
  const overlay  = document.getElementById('modalOverlay');
  const closeBtn = document.getElementById('modalCloseBtn');

  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal();
    });
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
}

window.openModal = function(key) {
  const overlay  = document.getElementById('modalOverlay');
  const windowEl = document.getElementById('modalWindow');
  const titleEl  = document.getElementById('modalTitle');
  const bodyEl   = document.getElementById('modalBody');
  if (!overlay || !windowEl || !bodyEl) return;

  const data = modalData[key] || modalData.projects;
  windowEl.className = `modal-window ${data.themeClass}`;
  titleEl.textContent = data.title;
  bodyEl.innerHTML = data.content;
  overlay.classList.add('active');
};

function closeModal() {
  const overlay = document.getElementById('modalOverlay');
  if (overlay) overlay.classList.remove('active');
  if (window.resetCameraToDefault) window.resetCameraToDefault();
}

/* --------------------------------------------------------------------------
   MODAL CONTENT TEMPLATES
   -------------------------------------------------------------------------- */
const modalData = {
  projects: {
    title: 'projects',
    themeClass: 'theme-projects',
    content: `
      <div class="modal-card">
        <img src="trading_bot.png" alt="TradingBOT" class="modal-card-img">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-pink);margin-bottom:.5rem;">TradingBOT</h3>
        <p style="font-size:.88rem;color:var(--text-muted);margin-bottom:.75rem;">Real-time algorithmic trading engine for Indian equities with 2-second scalping scheduler and 18-feature XGBoost signal model.</p>
        <div><span class="modal-tag">Python</span><span class="modal-tag">XGBoost</span><span class="modal-tag">Flask</span><span class="modal-tag">yfinance</span></div>
      </div>
      <div class="modal-card">
        <img src="invoice_iq.png" alt="InvoiceIQ" class="modal-card-img">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-pink);margin-bottom:.5rem;">InvoiceIQ</h3>
        <p style="font-size:.88rem;color:var(--text-muted);margin-bottom:.75rem;">AI invoice parsing & GST fraud detection reaching 96%+ accuracy via Gemini + Claude APIs, &lt;150ms inference.</p>
        <div><span class="modal-tag">Next.js</span><span class="modal-tag">TypeScript</span><span class="modal-tag">Gemini API</span><span class="modal-tag">Supabase</span></div>
      </div>
      <div class="modal-card">
        <img src="scam_shield.png" alt="ScamShield" class="modal-card-img">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-pink);margin-bottom:.5rem;">ScamShield</h3>
        <p style="font-size:.88rem;color:var(--text-muted);margin-bottom:.75rem;">On-device Android scam call detector with TFLite ML, zero audio retention, mid-call real-time risk alerts.</p>
        <div><span class="modal-tag">Kotlin</span><span class="modal-tag">Jetpack Compose</span><span class="modal-tag">TFLite</span></div>
      </div>
      <div class="modal-card">
        <img src="fraud_detector.png" alt="Fraud Detector" class="modal-card-img">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-pink);margin-bottom:.5rem;">Graph Fraud-Detector</h3>
        <p style="font-size:.88rem;color:var(--text-muted);margin-bottom:.75rem;">Real-time graph anomaly engine using NetworkX + SHAP explainable AI, case reports via Gemini API.</p>
        <div><span class="modal-tag">Python</span><span class="modal-tag">FastAPI</span><span class="modal-tag">NetworkX</span><span class="modal-tag">SHAP</span></div>
      </div>
      <div class="modal-card">
        <img src="civic_pulse.png" alt="CivicPulse" class="modal-card-img">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-pink);margin-bottom:.5rem;">CivicPulse</h3>
        <p style="font-size:.88rem;color:var(--text-muted);margin-bottom:.75rem;">Hyperlocal civic issue reporting with Gemini Vision for auto-classification and before/after photo verification.</p>
        <div><span class="modal-tag">Next.js</span><span class="modal-tag">Gemini Vision</span><span class="modal-tag">Leaflet</span></div>
      </div>`
  },
  education: {
    title: 'education',
    themeClass: 'theme-education',
    content: `
      <div class="modal-card">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-purple);margin-bottom:.4rem;">IIT Guwahati</h3>
        <p style="color:var(--accent-cyan);font-weight:600;margin-bottom:.5rem;">B.Sc. (Hons.) Data Science &amp; AI</p>
        <p style="font-size:.88rem;color:var(--text-muted);">Expected 2029 | CGPA: 8.50 / 10 (Sem 2) &amp; 7.50 / 10 (Sem 1)</p>
      </div>
      <div class="modal-card">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-purple);margin-bottom:.4rem;">GTBIT</h3>
        <p style="color:var(--accent-cyan);font-weight:600;margin-bottom:.5rem;">B.Tech Information Technology</p>
        <p style="font-size:.88rem;color:var(--text-muted);">Expected 2029 | CGPA: 8.76 / 10 | New Delhi, India</p>
        <p style="font-size:.85rem;color:var(--text-muted);margin-top:.5rem;">IEEE GTBIT Student Branch Member — IEEE Day 2025, TARANG 2.0, HackTivate</p>
      </div>`
  },
  aboutme: {
    title: 'about me',
    themeClass: 'theme-aboutme',
    content: `
      <div class="modal-card">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-cyan);margin-bottom:.5rem;">Hi, I'm Pranav Khera!</h3>
        <p style="font-size:.9rem;color:var(--text-muted);margin-bottom:.85rem;">
          Dual-degree undergraduate at <strong>IIT Guwahati</strong> (B.Sc. Data Science &amp; AI) and <strong>GTBIT</strong> (B.Tech IT).
          I build end-to-end ML systems — graph-based fraud engines, algorithmic trading bots, and privacy-first on-device Android ML.
        </p>
        <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1rem;">
          <span class="modal-tag">35+ LeetCode DSA</span>
          <span class="modal-tag">CTF DTU Participant</span>
          <span class="modal-tag">IEEE GTBIT Member</span>
        </div>
        <div style="display:flex;gap:.75rem;flex-wrap:wrap;">
          <a href="mailto:pranavkhera47@gmail.com" class="modal-tag" style="background:var(--accent-cyan);color:#000;text-decoration:none;font-weight:700;">✉ Email Me</a>
          <a href="https://github.com/Pranav2-4-7" target="_blank" class="modal-tag" style="text-decoration:none;">⌘ GitHub</a>
        </div>
      </div>`
  },
  credits: {
    title: 'credits',
    themeClass: 'theme-credits',
    content: `
      <div class="modal-card">
        <h3 style="font-family:var(--font-pixel);font-size:.9rem;color:var(--accent-yellow);margin-bottom:.5rem;">Credits</h3>
        <p style="font-size:.88rem;color:var(--text-muted);line-height:1.7;">
          • 3D Scene concept &amp; model by <strong>Jesse Zhou</strong> (jesse-zhou.com)<br>
          • Original GitHub repo: <strong>enderh3art/Ramen-Shop</strong><br>
          • Powered by <strong>Three.js</strong>, GSAP, OrbitControls<br>
          • Customised for <strong>Pranav Khera</strong> — Data Science &amp; AI Portfolio
        </p>
        <p style="margin-top:1rem;font-size:.85rem;color:var(--accent-cyan);">pranavkhera47@gmail.com | +91 9643734558</p>
      </div>`
  }
};

/* --------------------------------------------------------------------------
   3. AUDIO TOGGLE
   -------------------------------------------------------------------------- */
function initAudioToggle() {
  const btn = document.getElementById('audioToggleBtn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    btn.classList.toggle('muted');
    const muted = btn.classList.contains('muted');
    btn.innerHTML = muted
      ? '<i class="fa-solid fa-volume-xmark"></i>'
      : '<i class="fa-solid fa-volume-high"></i>';
  });
}
