'use strict';
const $=s=>document.querySelector(s),app=$('#app'),nav=$('#nav');
const ST='lernpfad-v1',LOB=['Super!','Stark!','Genau so!','Richtig, weiter so!','Sauber gelöst!'];
const PACK='<svg class="pki" viewBox="0 0 24 24"><path d="M9 5a3 3 0 0 1 6 0" fill="none" stroke="currentColor" stroke-width="2"/><rect x="5" y="6" width="14" height="15" rx="4" fill="currentColor"/><rect x="8" y="13" width="8" height="5" rx="1.5" fill="#0f1a1c" opacity=".35"/></svg>';
const XP_OK=10,XP_BONUS=5; // Bonus ab der 3. richtigen Antwort in Folge
let DATA,S,T,store=Object.assign({stats:{},xp:0,run:0,best:0,days:[],badges:{},stages:{},mode:'sek'},JSON.parse(localStorage.getItem(ST)||'{}'));
// Migration v9 → v10: gleicher Schlüssel, neue Felder nur ergänzen
store.favs=Array.isArray(store.favs)?store.favs:[];store.pack=Array.isArray(store.pack)?store.pack:[];store.schema=2;
const save=()=>{try{localStorage.setItem(ST,JSON.stringify(store))}catch(e){}};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt=n=>String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'’');
const MODES={real:['Real (G)',q=>q.level==='G'],sek:['Sek (G+E)',()=>true],alle:['Alle',()=>true]};
const BADGES=[
 {id:'etappe',name:'Erste Etappe',txt:'Eine Etappe abgeschlossen',ico:'<path d="M18 46V10" stroke="#06221a" stroke-width="4" stroke-linecap="round"/><path d="M20 12h22l-6 8 6 8H20z" fill="#06221a"/>'},
 {id:'serie10',name:'10 richtig in Folge',txt:'Zehn richtige Antworten nacheinander',ico:'<text x="28" y="38" text-anchor="middle" font-size="22" font-weight="800" fill="#06221a">10</text>'},
 {id:'meister',name:'Thema gemeistert',txt:'Jede Frage eines Themas richtig',ico:'<path d="M8 44l12-20 8 10 6-8 14 18z" fill="#06221a"/><circle cx="40" cy="16" r="5" fill="#06221a"/>'}];
function color(c){document.documentElement.style.setProperty('--c',c)}
function mtn(){return `<svg class="mtn" viewBox="0 0 800 220" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
<g fill="#fffdf2" opacity=".6"><ellipse cx="240" cy="44" rx="30" ry="6"/><circle cx="232" cy="39" r="8"/><circle cx="246" cy="37" r="10"/><ellipse cx="445" cy="58" rx="34" ry="6"/><circle cx="438" cy="52" r="9"/><circle cx="454" cy="50" r="11"/></g>
<g fill="#fbfbef"><circle cx="740" cy="120" r="18"/><circle cx="765" cy="108" r="24"/><circle cx="795" cy="104" r="26"/><rect x="725" y="118" width="80" height="22" rx="10"/><circle cx="655" cy="140" r="12"/><circle cx="672" cy="134" r="15"/><rect x="645" y="138" width="45" height="12" rx="6"/></g>
<path d="M60 160 L150 72 L175 84 L200 70 L300 150Z" fill="#d3d9c4"/><path d="M150 72 L175 84 L160 110 L120 130Z" fill="#c4cdb6"/>
<path d="M210 190 L250 140 L262 146 L285 108 L296 112 L320 73 L334 90 L348 96 L365 108 L376 118 L460 190Z" fill="#86aaa2"/>
<path d="M320 73 L334 90 L348 96 L365 108 L376 118 L460 190 L410 190 L372 140 L350 112 L334 100Z" fill="#f2f5e8"/>
<path d="M320 73 L296 112 L276 150 L312 122 L330 96Z" fill="#a4c3bb"/><path d="M330 96 L312 122 L322 160 L340 120Z" fill="#6e958d"/>
<path d="M285 108 L262 146 L230 190 L268 170 L290 132Z" fill="#5f877f"/><path d="M350 112 L372 140 L356 170 L344 136Z" fill="#7aa098"/><path d="M296 112 L285 108 L280 126Z" fill="#6e958d"/>
<path d="M320 73 L313 88 L320 85 L324 96 L330 88Z M365 108 L356 116 L364 114 L370 122Z M290 140 L312 134 L326 139 L304 143Z M262 160 L276 156 L282 160 L268 163Z" fill="#fff"/>
<path d="M380 190 L500 10 L665 190Z" fill="#8fb1a9"/>
<path d="M500 10 L665 190 L604 190 L548 102 L522 52Z" fill="#f4f6ea"/>
<path d="M500 10 L468 82 L436 152 L492 108Z" fill="#a9c7bf"/><path d="M500 10 L522 52 L506 110 L486 90Z" fill="#698f88"/>
<path d="M470 140 L418 190 L482 190 L512 150Z" fill="#5a827b"/><path d="M522 52 L548 102 L530 150 L512 118Z" fill="#7ca39b"/>
<path d="M500 10 L491 34 L500 30 L503 46 L510 30Z M516 122 L552 114 L568 122 L538 128Z M474 130 L496 124 L508 130 L484 133Z" fill="#fff"/>
<g fill="#fff"><ellipse cx="338" cy="150" rx="22" ry="6"/><circle cx="332" cy="145" r="8"/><circle cx="344" cy="143" r="9"/></g>
<path d="M250 220 L410 140 L560 158 L660 140 L1000 160 V220Z" fill="#dce6bb"/>
<path d="M410 140 L470 220 L330 220Z" fill="#cbdba5"/>
<path d="M-200 220 V176 L150 166 L290 150 L380 196 L320 220Z" fill="#a8c27e"/>
<path d="M290 150 L380 196 L240 220Z" fill="#9ab673"/>
<path d="M400 220 L500 156 L630 178 L740 146 L1000 156 V220Z" fill="#bccf86"/>
<path d="M740 146 L800 220 L660 220Z" fill="#cfd98e"/>
<path d="M270 220 L380 172 L520 186 L580 220Z" fill="#8aab6c"/><path d="M380 172 L440 220 L330 220Z" fill="#7d9f63"/>
<path d="M540 220 L650 170 L780 186 L1000 178 V220Z" fill="#7e9f68"/><path d="M650 170 L710 220 L610 220Z" fill="#6c8f5c"/>
<path d="M-200 220 L100 196 L250 210 L420 194 L560 212 L700 196 L1000 205 V220Z" fill="#2f5a4a"/>
<path d="M-200 221 V214 L200 208 L480 216 L800 206 L1000 210 V221Z" fill="#0f1a1c"/></svg><svg class="fg" viewBox="0 0 200 200" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="fgg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c5446"/><stop offset=".7" stop-color="#1a3330"/><stop offset="1" stop-color="#0f1a1c"/></linearGradient></defs>
<path d="M0 46 L22 58 L60 100 L110 146 L160 180 L200 200 L0 200Z" fill="url(#fgg)"/>
<path d="M0 46 L22 58 L12 96 L20 130 L0 150Z" fill="#1c3a32" opacity=".9"/>
<path d="M22 58 L60 100 L44 112 L38 140 L28 120Z" fill="#3a6656" opacity=".7"/>
<path d="M60 100 L110 146 L80 150 L72 172Z" fill="#163029" opacity=".8"/>
<path d="M0 200 V176 C60 186 140 194 200 200Z" fill="#0f1a1c"/></svg>`}
function setNav(v,show){const o=nav.querySelector('.packnav');if(o)o.remove();nav.hidden=!show;nav.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.v===v))}
nav.querySelectorAll('button').forEach(b=>b.onclick=()=>b.dataset.v==='pfad'?pfad():uebersicht());
function view(h){app.style.animation='none';app.offsetHeight;app.style.animation='';app.innerHTML=h;window.scrollTo(0,0)}
function toast(t){const d=document.createElement('div');d.className='toast';d.textContent=t;document.body.appendChild(d);setTimeout(()=>d.remove(),2200)}
function confetti(){if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;const fx=$('#fx'),cs=['#1fa37a','#f3e6c4','#9ff0cf','#e9d8a8','#5fd3ad'];
 for(let i=0;i<26;i++){const e=document.createElement('i');e.className='cf';e.style.left='50%';e.style.top='45%';e.style.background=cs[i%cs.length];
 e.style.setProperty('--dx',(Math.random()*320-160)+'px');e.style.setProperty('--dy',(Math.random()*-260-40)+'px');fx.appendChild(e);setTimeout(()=>e.remove(),1200)}}

/* Etappen = Lernziele des Themas, gefiltert nach Niveau */
function stages(t){const f=MODES[store.mode][1];return Object.keys(t.goals).map(k=>({lz:k,name:t.goals[k],qs:t.questions.filter(q=>String(q.goal)===k&&f(q))})).filter(s=>s.qs.length)}
const sdone=(t,lz)=>!!(store.stages[t.id]||{})[lz];
function today(){const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}
function dayStreak(){const set=new Set(store.days);let n=0,d=new Date();if(!set.has(today()))d.setDate(d.getDate()-1);
 for(;;){const k=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');if(!set.has(k))break;n++;d.setDate(d.getDate()-1)}return n}
function award(id){if(store.badges[id])return;store.badges[id]=today();save();const b=BADGES.find(x=>x.id===id);setTimeout(()=>{toast('Abzeichen: '+b.name);confetti()},400)}

let CFG={topics:{}};
const prog=t=>{const n=t.questions.length,r=t.questions.filter(q=>(store.stats[q.id]||{}).r>0).length;return {n,r,p:n?r/n:0}};
const STAR='<svg viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.8-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1-4.4-4.3 6.1-.8z"/></svg>';
function home(){color('#1fa37a');setNav('',false);
 view(`<section class="hero"><div class="brand"><i></i>Lernpfad</div><h1>Bereit für die nächste Etappe?</h1><p>Wähle ein Fach und geh deinen Weg Schritt für Schritt.</p>${mtn()}</section>
 <div class="chips"><div class="chip"><b>${fmt(store.xp)}</b><small>XP</small></div><div class="chip"><b>${dayStreak()}</b><small>Tage in Folge</small></div><div class="chip"><b>${Object.keys(store.badges).length}/3</b><small>Abzeichen</small></div></div>
 <h3>Fächer</h3><div class="grid">${DATA.subjects.map((s,i)=>{const ts=s.topics.filter(t=>CFG.topics[t.id]!=='spaeter'),q=ts.reduce((a,t)=>a+t.questions.length,0),r=ts.reduce((a,t)=>a+prog(t).r,0);
  return `<button class="card tile subj" style="--c:${s.color}" data-i="${i}"><img src="${s.icon}" alt=""><span><b>${esc(s.name)}</b>${ts.length?`<small>${ts.length} ${ts.length>1?'Themen':'Thema'}${q?` · ${r}/${q} Fragen geschafft`:''}</small>${q?`<i class="mini"><i style="width:${r/q*100}%"></i></i>`:''}`:'<small class="soon">Bald verfügbar</small>'}</span></button>`}).join('')}</div>
 <p class="hint">Alles bleibt nur auf diesem Gerät, ohne Login und ohne Rangliste. Auf dem iPhone kann der Fortschritt verloren gehen (z.B. wenn Safari Daten löscht).</p>`);
 app.querySelectorAll('.subj').forEach(b=>b.onclick=()=>{S=DATA.subjects[b.dataset.i];themen()})}

function themen(){color(S.color);setNav('',false);store.favs=store.favs||[];
 const vis=S.topics.filter(t=>CFG.topics[t.id]!=='spaeter'),fav=vis.filter(t=>store.favs.includes(t.id)),rest=vis.filter(t=>!store.favs.includes(t.id));
 const akt=rest.filter(t=>(CFG.topics[t.id]||'aktuell')==='aktuell'),rep=rest.filter(t=>CFG.topics[t.id]==='repetition');
 const card=t=>{const g=prog(t),f=store.favs.includes(t.id);return `<div class="card topic" data-id="${t.id}"><button class="topen" data-id="${t.id}"><b>${esc(t.name)}</b>
  ${g.n?`<small>${g.r}/${g.n} Fragen geschafft · ${stages(t).length} Etappen</small><i class="mini"><i style="width:${g.p*100}%"></i></i>`:'<small class="soon">Fragen folgen</small>'}</button>
  <button class="star ${f?'on':''}" data-id="${t.id}" aria-label="${f?'Favorit entfernen':'Als Favorit markieren'}" aria-pressed="${f}">${STAR}</button></div>`};
 view(`<section class="hero"><button class="back" aria-label="Zurück" id="bk">‹</button><div class="brand"><i></i>Lernpfad · ${esc(S.short)}</div><h1>${esc(S.name)}</h1><p>${vis.length?'Wähle ein Thema. Mit dem Stern merkst du dir Favoriten.':'Hier entstehen bald neue Lernpfade.'}</p>${mtn()}</section>
 ${!vis.length?`<div class="card empty"><img src="${S.icon}" alt=""><b>Bald verfügbar</b><p class="hint">Für ${esc(S.name)} gibt es noch keine Themen. Schau später wieder vorbei.</p><button class="btn sec" id="hm">Zu den Fächern</button></div>`:''}
 ${fav.length?`<h3>★ Favoriten</h3>${fav.map(card).join('')}`:''}
 ${akt.length?`<h3>Aktuell</h3>${akt.map(card).join('')}`:''}
 ${rep.length?`<details class="fold"${store.repOpen?' open':''}><summary>Repetition <small>${rep.length} ${rep.length>1?'Themen':'Thema'}</small></summary>${rep.map(card).join('')}</details>`:''}`);
 $('#bk').onclick=home;const hm=$('#hm');if(hm)hm.onclick=home;
 const fd=$('.fold');if(fd)fd.ontoggle=()=>{store.repOpen=fd.open;save()};
 app.querySelectorAll('.star').forEach(b=>b.onclick=()=>{const id=b.dataset.id;store.favs=store.favs.includes(id)?store.favs.filter(x=>x!==id):store.favs.concat(id);save();const y=scrollY;themen();window.scrollTo(0,y)});
 app.querySelectorAll('.topen').forEach(b=>b.onclick=()=>{const t=S.topics.find(x=>x.id===b.dataset.id);if(!t.questions.length)return toast('Fragen folgen bald');T=t;pfad()})}

function pfad(){color(S.color);setNav('pfad',true);
 const st=stages(T),n=st.length,nx=st.findIndex(s=>!sdone(T,s.lz)),H=118,W=340,TOP=90,h=TOP+(n-1)*H+90;
 // Etappe 0 unten, letzte oben; nach oben schmaler und kleiner (Perspektive)
 const pts=st.map((s,i)=>{const t=n>1?i/(n-1):0,amp=(1-t*.55)*120;return {x:W/2+[0,1,0,-1][i%4]*amp,y:h-60-i*H,sc:1-t*.28,t}});
 const goal={x:W/2,y:28};
 let seg='';const all=pts.concat([{x:goal.x,y:goal.y+18,t:1}]);
 for(let i=1;i<all.length;i++){const a=all[i-1],b=all[i],d=`M${a.x} ${a.y} C${a.x} ${a.y-H*.55} ${b.x} ${b.y+H*.55} ${b.x} ${b.y}`,w=14-10*((a.t+b.t)/2),done=i-1<(nx<0?n:nx);
  seg+=`<path d="${d}" fill="none" stroke="#2e464a" stroke-width="${w.toFixed(1)}" stroke-linecap="round"/><path d="${d}" fill="none" stroke="var(--c)" stroke-width="${(w*.4).toFixed(1)}" stroke-dasharray="${done?'none':'2 '+(w*1.1).toFixed(0)}" stroke-linecap="round" opacity="${done?1:.8}"/>`}
 const doneLen=nx<0?n:nx;
 view(`<section class="hero"><button class="back" aria-label="Zurück" id="bk">‹</button><div class="brand"><i></i>Lernpfad · ${esc(S.short)}</div><h1>${esc(T.name)}</h1><p>${doneLen} von ${n} Etappen geschafft</p>${mtn()}</section>
 <div class="card"><div class="seg">${Object.keys(MODES).map(k=>`<button data-k="${k}" class="${k===store.mode?'on':''}">${MODES[k][0]}</button>`).join('')}</div></div>
 <div class="path" style="height:${h}px;max-width:${W}px;margin:0 auto"><svg viewBox="0 0 ${W} ${h}" preserveAspectRatio="none">${seg}
 <g transform="translate(${goal.x} ${goal.y})"><path d="M0 18 V-20" stroke="${nx<0?'var(--c)':'#93a8a4'}" stroke-width="3" stroke-linecap="round"/><path d="M0 -20 L20 -13 L0 -6Z" fill="${nx<0?'var(--c)':'#f3e6c4'}"/><path d="M-8 18 L0 8 L8 18Z" fill="#2e464a"/></g></svg>
 <div class="goal" style="top:${goal.y+24}px">Ziel: Thema gemeistert</div>
 ${st.map((s,i)=>`<button class="stage ${sdone(T,s.lz)?'done':''} ${i===nx?'next':''}" style="left:${pts[i].x/W*100}%;top:${pts[i].y}px;--sc:${pts[i].sc.toFixed(2)}" data-i="${i}"><div class="dot">${sdone(T,s.lz)?'✓':s.lz}</div><span>LZ ${s.lz} · ${s.qs.length} ${s.qs.length>1?'Fragen':'Frage'}</span></button>`).join('')}</div>
 ${nx>=0?'<p class="hint up">↑ Weiter Richtung Gipfel</p>':''}<button class="btn" id="go">${nx<0?'Ganzes Thema wiederholen':'Etappe LZ '+st[nx].lz+' starten'}</button>`);
 const pn=packQs().length;if(pn)nav.insertAdjacentHTML('beforeend',`<span class="packnav" title="Rucksack: Fragen, die in der nächsten Etappe wiederkommen">${PACK}${pn}</span>`);
 $('#bk').onclick=themen;
 app.querySelectorAll('.seg button').forEach(b=>b.onclick=()=>{store.mode=b.dataset.k;save();pfad()});
 app.querySelectorAll('.stage').forEach(b=>b.onclick=()=>quiz([st[b.dataset.i]]));
 $('#go').onclick=()=>quiz(nx<0?st:[st[nx]]);
 const tgt=nx<0?$('.goal'):app.querySelectorAll('.stage')[nx],from=lastStage!=null?app.querySelectorAll('.stage')[st.findIndex(s=>s.lz===lastStage)]:null;lastStage=null;
 const yOf=el=>{const r=el.getBoundingClientRect();return Math.max(0,window.scrollY+r.top+r.height/2-innerHeight/2)};
 window.scrollTo({top:yOf(from||tgt),behavior:'instant'});
 if(from&&from!==tgt&&!matchMedia('(prefers-reduced-motion: reduce)').matches){const y0=window.scrollY,y1=yOf(tgt),D=1300;
  setTimeout(()=>{const t0=performance.now(),ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
   const step=now=>{const t=Math.min(1,(now-t0)/D);window.scrollTo(0,y0+(y1-y0)*ease(t));if(t<1)requestAnimationFrame(step)};requestAnimationFrame(step)},400)}
 else if(from)window.scrollTo({top:yOf(tgt),behavior:'instant'});}

function weight(q){const s=store.stats[q.id]||{r:0,w:0};return s.w*2-Math.min(s.r,3)*.5+Math.random()}

/* ---------- Fragetypen ---------- */
const shuffle=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
function shuffled(a){if(a.length<2)return a.slice();let s;do s=shuffle(a);while(s.every((x,i)=>x===a[i]));return s}
function parseNum(s){s=String(s).trim().replace(/[’'\s]/g,'');if(s.includes(',')&&!s.includes('.'))s=s.replace(',','.');else s=s.replace(/,/g,'');return s===''?NaN:Number(s)}
function fmtNum(n){const [i,d]=String(n).split('.');return i.replace(/\B(?=(\d{3})+(?!\d))/g,'’')+(d?'.'+d:'')}
const norm=s=>String(s).trim().toLowerCase().replace(/[’'\s]/g,'').replace(/\./g,':');
function imgHtml(im){if(!im)return '';const o=typeof im==='string'?{src:im,alt:'Abbildung'}:im;
 return `<figure class="qimg"><img src="${esc(o.src)}" alt="${esc(o.alt||'')}" loading="lazy">${o.credit?`<figcaption>${esc(o.credit)}</figcaption>`:''}</figure>`}
function widget(q){
 if(q.type==='mc'||q.type==='tf'){const opts=q.type==='tf'?[['true','Richtig'],['false','Falsch']]:q.options.map((o,i)=>[String(i),o]);
  return {html:opts.map(([v,t])=>`<button class="opt" data-v="${v}">${esc(t)}</button>`).join(''),bind:ans=>app.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{
   const ok=b.dataset.v===String(q.answer);app.querySelectorAll('.opt').forEach(x=>{if(x.dataset.v===String(q.answer))x.classList.add('ok')});if(!ok)b.classList.add('no');ans(ok,'')})}}
 if(q.type==='num')return {html:`<div class="num"><input id="n" inputmode="decimal" autocomplete="off" placeholder="Zahl, z.B. 2’903.36">${q.unit?`<b>${esc(q.unit)}</b>`:''}</div><button class="btn" id="ck">Prüfen</button>`,
  bind:ans=>{const f=()=>{const v=parseNum($('#n').value);if(isNaN(v))return $('#n').focus();const ok=Math.abs(v-q.answer)<=(q.tolerance||0)+1e-9;$('#n').classList.add(ok?'ok':'no');ans(ok,`Lösung: <b>${fmtNum(q.answer)}${q.unit?' '+esc(q.unit):''}</b>`)};$('#ck').onclick=f;$('#n').onkeydown=e=>{if(e.key==='Enter')f()}}}
 if(q.type==='order'){const pool=shuffled(q.items.map((t,i)=>i));
  return {html:`<p class="hint">Tippe die Einträge in der richtigen Reihenfolge an. Nochmals tippen nimmt einen Eintrag zurück.</p><ol class="ord" id="picked"></ol><div class="pool" id="pool">${pool.map(i=>`<button class="chipbtn" data-i="${i}">${esc(q.items[i])}</button>`).join('')}</div><button class="btn" id="ck" disabled>Prüfen</button>`,
  bind:ans=>{const picked=[];const draw=()=>{$('#picked').innerHTML=picked.map((i,k)=>`<li><button class="chipbtn on" data-k="${k}"><span>${k+1}</span>${esc(q.items[i])}</button></li>`).join('');
    app.querySelectorAll('#pool .chipbtn').forEach(b=>b.hidden=picked.includes(+b.dataset.i));$('#ck').disabled=picked.length<q.items.length;
    app.querySelectorAll('#picked .chipbtn').forEach(b=>b.onclick=()=>{picked.splice(+b.dataset.k,1);draw()})};
   app.querySelectorAll('#pool .chipbtn').forEach(b=>b.onclick=()=>{picked.push(+b.dataset.i);draw()});
   $('#ck').onclick=()=>{const ok=picked.every((v,k)=>v===k);app.querySelectorAll('#picked li').forEach((li,k)=>li.classList.add(picked[k]===k?'ok':'no'));
    ans(ok,'Richtige Reihenfolge:<ol>'+q.items.map(t=>'<li>'+esc(t)+'</li>').join('')+'</ol>')}}}}
 if(q.type==='match'){const rights=shuffled(q.pairs.map(p=>p[1]));
  return {html:`<div class="match">${q.pairs.map((p,i)=>`<label class="mrow"><span>${esc(p[0])}</span><select data-i="${i}"><option value="">– wählen –</option>${rights.map(r=>`<option>${esc(r)}</option>`).join('')}</select></label>`).join('')}</div><button class="btn" id="ck" disabled>Prüfen</button>`,
  bind:ans=>{const ss=[...app.querySelectorAll('.match select')];ss.forEach(s=>s.onchange=()=>{$('#ck').disabled=ss.some(x=>!x.value)});
   $('#ck').onclick=()=>{let ok=true;ss.forEach(s=>{const g=s.value===q.pairs[+s.dataset.i][1];s.parentNode.classList.add(g?'ok':'no');if(!g)ok=false});
    ans(ok,'Richtig ist:<ul>'+q.pairs.map(p=>`<li><b>${esc(p[0])}</b> → ${esc(p[1])}</li>`).join('')+'</ul>')}}}}
 if(q.type==='cloze'){const html=esc(q.text).replace(/\{(\d+)\}/g,(m,k)=>{const g=q.gaps[+k];return g.options?`<select class="gap" data-k="${k}"><option value="">…</option>${g.options.map((o,i)=>`<option value="${i}">${esc(o)}</option>`).join('')}</select>`:`<input class="gap" data-k="${k}" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="…">`});
  return {html:`<p class="cloze">${html}</p><button class="btn" id="ck" disabled>Prüfen</button>`,
  bind:ans=>{const gs=[...app.querySelectorAll('.gap')];const upd=()=>{$('#ck').disabled=gs.some(x=>!x.value.trim())};gs.forEach(x=>{x.oninput=upd;x.onchange=upd});
   $('#ck').onclick=()=>{let ok=true;gs.forEach(x=>{const g=q.gaps[+x.dataset.k];const good=g.options?+x.value===g.answer:[g.answer].concat(g.alt||[]).some(s=>norm(s)===norm(x.value));x.classList.add(good?'ok':'no');if(!good)ok=false});
    ans(ok,'Lösung: '+esc(q.text).replace(/\{(\d+)\}/g,(m,k)=>{const g=q.gaps[+k];return '<b>'+esc(g.options?g.options[g.answer]:g.answer)+'</b>'}))}}}}
 return {html:'<p>Unbekannter Fragetyp.</p>',bind:()=>{}}}
function packQs(){store.pack=store.pack||[];const f=MODES[store.mode][1];return store.pack.map(id=>T.questions.find(q=>q.id===id)).filter(q=>q&&f(q))}
let lastStage=null; // LZ der eben abgeschlossenen Etappe (für das Scrollen)
function quiz(sts){setNav('',false);store.pack=store.pack||[];
 const own=sts.flatMap(s=>s.qs),ownIds=new Set(own.map(q=>q.id)),queue=own.slice().sort((a,b)=>weight(b)-weight(a));
 // Rucksack-Fragen aus früheren Etappen: gemischt einfügen, nie als erste
 const fromPack=new Set();packQs().filter(q=>!ownIds.has(q.id)).forEach(q=>{fromPack.add(q.id);queue.splice(1+Math.floor(Math.random()*queue.length),0,q)});
 let total=queue.length,done=0,xp=0,run=0,packRound=false;
 if(!store.days.includes(today())){store.days.push(today());store.days=store.days.slice(-60);save()}
 const next=()=>{if(queue.length)return show(queue.shift());
  if(!packRound){const m=store.stages[T.id]||{},rest=stages(T).some(s=>!m[s.lz]&&!sts.some(x=>x.lz===s.lz)),pk=packQs();
   if(!rest&&pk.length){packRound=true;pk.forEach(q=>{fromPack.add(q.id);queue.push(q)});total+=pk.length;return show(queue.shift(),true)}}
  finish()};
 function show(q,intro){const pk=fromPack.has(q.id),W=widget(q);
  view(`<div class="top"><button class="x" id="x" aria-label="Schliessen">×</button><div class="bar"><i style="width:${done/total*100}%"></i></div><span class="xp" id="xp">${xp} XP</span></div>
  ${intro?'<div class="card packintro">'+PACK+'<span><b>Rucksack-Runde</b><br><small>Noch einmal die Fragen aus deinem Rucksack.</small></span></div>':''}
  <div class="card" data-q="${q.id}"><span class="tag">LZ ${q.goal}</span><span class="tag">${q.level}</span>${pk?'<span class="tag pk">'+PACK+' Rucksack</span>':''}<div class="q">${esc(q.prompt)}</div>${imgHtml(q.image)}${W.html}<div id="fb"></div></div>`);
  $('#x').onclick=pfad;
  const answer=(ok,sol)=>{app.querySelectorAll('.card button:not(#nx), .card input, .card select').forEach(b=>b.disabled=true);
   const s=store.stats[q.id]=store.stats[q.id]||{r:0,w:0};ok?s.r++:s.w++;
   let gain=0;done++;
   if(ok){run++;store.run++;store.best=Math.max(store.best,store.run);gain=XP_OK+(run>=3?XP_BONUS:0);xp+=gain;store.xp+=gain;confetti();if(store.run>=10)award('serie10');store.pack=store.pack.filter(x=>x!==q.id)}
   else{run=0;store.run=0;if(!store.pack.includes(q.id))store.pack.push(q.id)}
   save();
   $('#fb').innerHTML=`<div class="fb ${ok?'ok':'no'}"><b>${ok?LOB[Math.floor(Math.random()*LOB.length)]+`<span class="plus">+${gain} XP${gain>XP_OK?' (Serienbonus)':''}</span>`+(pk?' Raus aus dem Rucksack.':''):'Noch nicht ganz. Die Frage kommt in deinen Rucksack.'}</b>${!ok&&sol?'<div class="sol">'+sol+'</div>':''}${esc(q.explanation)}</div><button class="btn" id="nx">Weiter</button>`;
   $('.bar i').style.width=done/total*100+'%';$('#xp').textContent=xp+' XP';$('#nx').onclick=next;$('#nx').scrollIntoView({behavior:'smooth',block:'nearest'})};
  W.bind(answer)}
 function finish(){const m=store.stages[T.id]=store.stages[T.id]||{};sts.forEach(s=>m[s.lz]=true);lastStage=sts[sts.length-1].lz;award('etappe');
  if(stages(T).every(s=>m[s.lz]))award('meister');save();
  const pn=packQs().length;
  view(`<section class="hero"><div class="brand"><i></i>Etappe geschafft</div><h1>+${xp} XP</h1><p>${sts.length>1?'Alle Etappen':'Etappe LZ '+sts[0].lz} abgeschlossen. Schön gemacht!</p>${mtn()}</section>
  ${pn?`<div class="card packintro">${PACK}<span>Im Rucksack: ${pn} ${pn>1?'Fragen':'Frage'}<br><small>Sie kommen in der nächsten Etappe wieder.</small></span></div>`:''}
  <button class="btn" id="w">Weiter auf dem Pfad</button><button class="btn sec" id="u">Zur Übersicht</button>`);confetti();
  $('#w').onclick=pfad;$('#u').onclick=uebersicht}
 next()}

function uebersicht(){color(S.color);setNav('uebersicht',true);
 const qs=T.questions,ok=qs.filter(q=>(store.stats[q.id]||{}).r>0).length,ans=qs.filter(q=>store.stats[q.id]).length,p=ok/qs.length,R=52,C=2*Math.PI*R;
 let r=0,a=0;qs.forEach(q=>{const s=store.stats[q.id];if(s){r+=s.r;a+=s.r+s.w}});
 view(`<section class="hero"><div class="brand"><i></i>Übersicht · ${esc(S.short)}</div><h1>Dein Weg bisher</h1><p>${esc(T.name)}</p>${mtn()}</section>
 <div class="card ringwrap"><svg class="ring" viewBox="0 0 130 130"><circle cx="65" cy="65" r="${R}" fill="none" stroke="#2e464a" stroke-width="12"/><circle cx="65" cy="65" r="${R}" fill="none" stroke="var(--c)" stroke-width="12" stroke-linecap="round" stroke-dasharray="${C*p} ${C}" transform="rotate(-90 65 65)" style="transition:stroke-dasharray .8s"/><text x="65" y="66" text-anchor="middle" font-size="26">${Math.round(p*100)}%</text><text x="65" y="86" text-anchor="middle" font-size="11" fill="#93a8a4" style="font-weight:600">gemeistert</text></svg>
 <div class="stats"><div><b>${fmt(store.xp)}</b><small>XP total</small></div><div><b>${r}/${a}</b><small>richtig / beantwortet</small></div><div><b>${ok}/${qs.length}</b><small>Fragen schon richtig</small></div><div><b>${dayStreak()}</b><small>Tage in Folge geübt</small></div></div></div>
 <h3>Abzeichen</h3><div class="badges">${BADGES.map(b=>`<div class="badge ${store.badges[b.id]?'on':''}"><svg viewBox="0 0 56 56"><polygon points="28,2 51,15 51,41 28,54 5,41 5,15" fill="${store.badges[b.id]?'var(--c)':'#3a5155'}"/><g transform="translate(0 0)">${b.ico}</g></svg><b>${b.name}</b><small>${b.txt}</small></div>`).join('')}</div>
 <h3>Lernziele</h3><div class="card"><table>${Object.entries(T.goals).map(([k,v])=>{const q=qs.filter(x=>String(x.goal)===k),o=q.filter(x=>(store.stats[x.id]||{}).r>0).length;return `<tr><td><span class="tag">${k}</span>${esc(v)}</td><td class="r" style="color:${o===q.length?'var(--c)':'var(--mut)'}">${o}/${q.length}</td></tr>`}).join('')}</table></div>
 <button class="btn sec" id="rs">Fortschritt zurücksetzen</button>`);
 $('#rs').onclick=()=>{if(confirm('Ganzen Fortschritt auf diesem Gerät löschen?')){localStorage.removeItem(ST);location.reload()}}}

Promise.all([fetch('questions.json').then(r=>r.json()),fetch('config.json').then(r=>r.json()).catch(()=>({topics:{}}))]).then(([d,c])=>{DATA=d;CFG=c;CFG.topics=CFG.topics||{};home()}).catch(()=>view('<div class="card">Die Fragen konnten nicht geladen werden.</div>'));
if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js');
