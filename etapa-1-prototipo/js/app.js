/**
 * TechPCInfo – lógica comum do protótipo (Etapa 1)
 * Detecção de dispositivo móvel para scan QR com câmara.
 */

const API = "/api";

// ---------- Detecção de dispositivo portátil com câmara ----------
function isMobileDevice() {
  const ua = navigator.userAgent || navigator.vendor || "";
  const mobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet/i.test(ua);
  const touch = navigator.maxTouchPoints > 1;
  const smallScreen = Math.min(window.screen.width, window.screen.height) < 768;
  return mobileUA || (touch && smallScreen);
}

function canUseCameraScan() {
  return isMobileDevice() && !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

// ---------- Sessão ----------
function getSession() {
  try {
    return JSON.parse(localStorage.getItem("techpc_session") || "null");
  } catch {
    return null;
  }
}

function setSession(user) {
  localStorage.setItem("techpc_session", JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem("techpc_session");
}

function requireAuth(roles) {
  const s = getSession();
  if (!s || !s.token) {
    window.location.href = "/index.html";
    return null;
  }
  if (roles && roles.length && !roles.includes(s.role)) {
    alert("Não tem permissão para esta página.");
    window.location.href = "/dashboard.html";
    return null;
  }
  return s;
}

// ---------- API helpers ----------
async function apiGet(path) {
  const r = await fetch(API + path);
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).error || r.statusText);
  return r.json();
}

async function apiPost(path, body) {
  const r = await fetch(API + path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}

// ---------- UI helpers ----------
function statusBadge(status) {
  const map = {
    ativo: "bg-emerald-100 text-emerald-800",
    manutencao: "bg-amber-100 text-amber-800",
    inativo: "bg-slate-100 text-slate-600",
  };
  const cls = map[status] || map.inativo;
  return `<span class="px-2 py-0.5 rounded-full text-xs font-medium ${cls}">${status || "—"}</span>`;
}

function escapeHtml(s) {
  if (s == null) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

window.TechPC = {
  isMobileDevice,
  canUseCameraScan,
  getSession,
  setSession,
  clearSession,
  requireAuth,
  apiGet,
  apiPost,
  statusBadge,
  escapeHtml,
};
