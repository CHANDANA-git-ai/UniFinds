const CACHE_NAME = 'unifinds-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/css/style.min.css',
  '/js/app.min.js'
];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  // Network-first for API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(fetch(event.request).catch(()=>caches.match(event.request)));
    return;
  }
  // Cache-first for static assets
  event.respondWith(caches.match(event.request).then(resp=>resp||fetch(event.request).then(fetchResp=>{return caches.open(CACHE_NAME).then(cache=>{cache.put(event.request, fetchResp.clone());return fetchResp;});})));
});
