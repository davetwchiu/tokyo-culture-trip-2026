---
---
const CACHE = "tokyo-culture-trip-{{ site.time | date: '%s' }}";
const CORE = [
  "{{ '/assets/style.css' | relative_url }}",
  {% for cached_page in site.pages %}{% if cached_page.offline == true %}
  "{{ cached_page.url | relative_url }}",
  {% endif %}{% endfor %}
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(CORE)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(
    keys.filter(key => key.startsWith("tokyo-culture-trip-") && key !== CACHE).map(key => caches.delete(key))
  )));
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  if (event.request.method !== "GET" || new URL(event.request.url).origin !== self.location.origin) return;
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request).catch(() => {
    if (event.request.mode === "navigate") return caches.match("{{ '/offline/' | relative_url }}");
    return Response.error();
  })));
});
