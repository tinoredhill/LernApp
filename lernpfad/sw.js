const C='lernpfad-v11';
const F=['./','index.html','style.css','app.js','questions.json','config.json','icons/fach-ma.svg','icons/fach-rzg.svg','manifest.webmanifest','icons/fach-nt.svg','icons/icon-192.png','icons/icon-512.png','icons/apple-touch-icon.png','icons/icon-maskable-512.png','icons/app-icon.svg','icons/favicon-32.png','favicon.ico','img/frottee-leinen.svg','img/rzg/hudf.jpg','img/rzg/sonnensystem_ausschnitt.jpg','img/rzg/bluemarble.jpg','img/rzg/ptolemaeus.jpg','img/rzg/galilei.jpg','img/rzg/tageslaengen.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(F)));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))));self.clients.claim();});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;
 e.respondWith(fetch(e.request).then(r=>{const cl=r.clone();caches.open(C).then(c=>c.put(e.request,cl));return r;}).catch(()=>caches.match(e.request,{ignoreSearch:true})));});
