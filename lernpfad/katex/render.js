// Rendert $...$ mit KaTeX, auch in später eingefügten Inhalten (Fragen, Optionen, Lückentexte, Erklärungen).
(function(){const o={delimiters:[{left:"$",right:"$",display:false}],throwOnError:false,ignoredTags:["script","noscript","style","textarea","pre","code","option","select","input"]};
let busy=false;const ob=new MutationObserver(()=>{if(busy)return;busy=true;requestAnimationFrame(()=>{ob.disconnect();try{renderMathInElement(document.body,o)}catch(e){}ob.observe(document.body,{childList:true,subtree:true});busy=false})});
function go(){if(!window.renderMathInElement)return setTimeout(go,30);renderMathInElement(document.body,o);ob.observe(document.body,{childList:true,subtree:true})}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",go);else go()})();
