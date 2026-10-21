const CACHE = "techpcinfo-v1";
const PRECACHE = ["/","/index.html","/dashboard.html","/pc-detail.html","/scan.html","/admin.html","/settings.html","/register.html","/css/app.css","/js/app.js","/manifest.json","/assets/icons/icon-192.png","/assets/icons/icon-512.png"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (url.pathname.startsWith("/api/")) { e.respondWith(fetch(e.request)); return; }
  e.respondWith(caches.match(e.request).then((cached) => cached || fetch(e.request).then((res) => { const copy = res.clone(); if (e.request.method === "GET" && res.status === 200) caches.open(CACHE).then((c) => c.put(e.request, copy)); return res; }).catch(() => cached)));
});
