'use strict';
const $=s=>document.querySelector(s), app=$('#app');
const LOB=['Super!','Stark!','Genau so!','Richtig, weiter so!','Sauber gelöst!'];
const ST='lernapp-v1';
let DATA, store=JSON.parse(localStorage.getItem(ST)||'{}'); store.stats=store.stats||{}; store.mode=store.mode||'sek';
const save=()=>{try{localStorage.setItem(ST,JSON.stringify(store))}catch(e){}};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let backFn=null; $('#back').onclick=()=>backFn&&backFn();
function head(t,b,color){$('#title').textContent=t;$('#back').hidden=!b;backFn=b;document.documentElement.style.setProperty('--c',color||'#1fa37a');window.scrollTo(0,0)}

function home(){head('Lernapp',null,'#3b5bdb');
 app.innerHTML=`<div class="card"><h2 style="margin:0 0 6px">Hallo!</h2><p class="hint" style="margin:0">Übe für deine Tests. Wähle ein Fach und ein Thema.</p></div>
 <h3>Fächer</h3>${DATA.subjects.map((s,i)=>`<button class="card tile" data-i="${i}"><img src="${s.icon}" alt=""><span><b>${esc(s.name)}</b><small>${s.topics.length} Thema</small></span></button>`).join('')}
 <p class="hint">Dein Fortschritt wird nur auf diesem Gerät gespeichert, ohne Login. Auf dem iPhone kann er verloren gehen (z.B. wenn Safari Daten löscht).</p>`;
 app.querySelectorAll('.tile').forEach(b=>b.onclick=()=>topics(DATA.subjects[b.dataset.i]));}

function topics(s){head(s.name,home,s.color);
 app.innerHTML=s.topics.map((t,i)=>{const qs=t.questions,d=qs.filter(q=>(store.stats[q.id]||{}).r>0).length;
  return `<button class="card tile" data-i="${i}"><img src="${s.icon}" alt=""><span><b>${esc(t.name)}</b><small>${qs.length} Fragen · ${d} schon richtig</small></span></button>`}).join('');
 app.querySelectorAll('.tile').forEach(b=>b.onclick=()=>setup(s,s.topics[b.dataset.i]));}

const MODES={real:['Real (G)',q=>q.level==='G'],sek:['Sek (G+E)',()=>true],alle:['Alle',()=>true]};
function setup(s,t){head(t.name,()=>topics(s),s.color);
 const draw=()=>{const n=t.questions.filter(MODES[store.mode][1]).length;
 app.innerHTML=`<div class="card"><b>Niveau</b><div class="seg" style="margin-top:10px">${Object.keys(MODES).map(k=>`<button data-k="${k}" class="${k===store.mode?'on':''}">${MODES[k][0]}</button>`).join('')}</div>
 <p class="hint">Real: nur Grundanforderungen (G). Sek: G und erweiterte Anforderungen (E). ${n} Fragen.</p>
 <button class="btn" id="go">Übung starten</button><button class="btn sec" id="rs">Fortschritt zurücksetzen</button></div>
 <div class="card"><b>Lernziele</b><table>${Object.entries(t.goals).map(([k,v])=>`<tr><td><span class="tag">${k}</span>${esc(v)}</td></tr>`).join('')}</table></div>`;
 app.querySelectorAll('.seg button').forEach(b=>b.onclick=()=>{store.mode=b.dataset.k;save();draw()});
 $('#go').onclick=()=>quiz(s,t);
 $('#rs').onclick=()=>{if(confirm('Fortschritt für dieses Thema löschen?')){t.questions.forEach(q=>delete store.stats[q.id]);save();draw()}};};draw();}

function weight(q){const st=store.stats[q.id]||{r:0,w:0};return 1+st.w*2-Math.min(st.r,3)*0.5+Math.random()}
function quiz(s,t){
 const pool=t.questions.filter(MODES[store.mode][1]).sort((a,b)=>weight(b)-weight(a));
 const queue=pool.slice(), res={}, again=new Set(); let done=0, total=pool.length;
 const next=()=>{if(!queue.length)return summary(s,t,res);show(queue.shift())};
 function show(q){head(t.name,()=>setup(s,t),s.color);
  const pct=Math.round(done/total*100);
  let body='';
  if(q.type==='mc')body=q.options.map((o,i)=>`<button class="opt" data-v="${i}">${esc(o)}</button>`).join('');
  if(q.type==='tf')body=`<button class="opt" data-v="true">Richtig</button><button class="opt" data-v="false">Falsch</button>`;
  if(q.type==='num')body=`<div class="num"><input id="n" inputmode="decimal" autocomplete="off" placeholder="Zahl">${q.unit?`<span>${esc(q.unit)}</span>`:''}</div><button class="btn" id="ck">Prüfen</button>`;
  app.innerHTML=`<div class="meta"><span>Frage ${done+1} von ${total}</span><span><span class="tag">LZ ${q.goal}</span><span class="tag">${q.level}</span></span></div>
  <div class="bar"><i style="width:${pct}%"></i></div><div class="card"><div class="q">${esc(q.prompt)}${q.image?`<img src="${q.image}" alt="Abbildung">`:''}</div>${body}<div id="fb"></div></div>`;
  const answer=(ok,el)=>{
   app.querySelectorAll('.opt,#ck,#n').forEach(b=>b.disabled=true);
   if(q.type!=='num'){app.querySelectorAll('.opt').forEach(b=>{if(String(b.dataset.v)===String(q.answer))b.classList.add('ok')});if(!ok&&el)el.classList.add('no')}
   const st=store.stats[q.id]=store.stats[q.id]||{r:0,w:0}; ok?st.r++:st.w++; save();
   const r=res[q.goal]=res[q.goal]||{ok:0,n:0}; if(!again.has(q.id)){r.n++;if(ok)r.ok++;}
   if(ok)done++; else if(!again.has(q.id)){again.add(q.id);queue.splice(Math.min(2,queue.length),0,q)} else {done++;}
   const sol=q.type==='num'?` Lösung: ${String(q.answer)}${q.unit?' '+q.unit:''}.`:'';
   $('#fb').innerHTML=`<div class="fb ${ok?'ok':'no'}"><b>${ok?LOB[Math.floor(Math.random()*LOB.length)]:'Noch nicht ganz.'+(again.has(q.id)&&!ok&&queue.includes(q)?' Die Frage kommt gleich nochmals.':'')}</b>${esc(q.explanation)}${esc(sol)}</div><button class="btn" id="nx">Weiter</button>`;
   $('.bar i').style.width=Math.round(done/total*100)+'%';
   $('#nx').onclick=next; $('#nx').scrollIntoView({behavior:'smooth',block:'nearest'});};
  app.querySelectorAll('.opt').forEach(b=>b.onclick=()=>answer(String(q.answer)===b.dataset.v,b));
  if(q.type==='num'){const f=()=>{const v=parseFloat($('#n').value.replace(/[’' ]/g,'').replace(',','.'));if(isNaN(v)){$('#n').focus();return}answer(Math.abs(v-q.answer)<=(q.tolerance||0)+1e-9)};
   $('#ck').onclick=f;$('#n').onkeydown=e=>{if(e.key==='Enter')f()}}}
 next();}

function summary(s,t,res){head('Auswertung',()=>setup(s,t),s.color);
 let ok=0,n=0;Object.values(res).forEach(r=>{ok+=r.ok;n+=r.n});const p=n?Math.round(ok/n*100):0;
 app.innerHTML=`<div class="card"><div class="big">${ok} / ${n}</div><p style="text-align:center;margin:0">${p>=80?'Sehr gut vorbereitet!':p>=50?'Gut unterwegs. Übe die markierten Lernziele nochmals.':'Dranbleiben! Lies die Skriptseiten nochmals und übe erneut.'}</p></div>
 <div class="card"><b>Übersicht pro Lernziel</b><p class="hint">Gezählt wird der erste Versuch.</p><table>${Object.keys(res).sort((a,b)=>a-b).map(k=>{const r=res[k],f=r.ok===r.n;
 return `<tr><td><span class="tag">${k}</span>${esc(t.goals[k])}</td><td class="r" style="color:${f?'var(--ok)':'var(--no)'}">${f?'✓':'↻'} ${r.ok}/${r.n}</td></tr>`}).join('')}</table></div>
 <button class="btn" id="ag">Nochmals üben</button><button class="btn sec" id="hm">Zur Startseite</button>`;
 $('#ag').onclick=()=>quiz(s,t);$('#hm').onclick=home;}

fetch('questions.json').then(r=>r.json()).then(d=>{DATA=d;home()}).catch(()=>{app.innerHTML='<div class="card">Die Fragen konnten nicht geladen werden.</div>'});
if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js');
