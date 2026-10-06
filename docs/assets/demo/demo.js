const demoLanguage = location.pathname.includes('/es/') ? 'es' : 'en';
const ids=[];function add(element,kind,text,position,color){ids.push(markaOverlay('demo','add',document.getElementById(element),{id:crypto.randomUUID(),kind,text,position,color,background:kind==='highlight'?color+'20':'transparent',width:Number(document.getElementById('width').value),style:'solid',radius:6,text_color:contrastColor(color),size:28,group:'demo'}));}
const labels={en:['Mark elements and explain the sequence. The form stays clickable.','Highlight','Numbered dots','Add note','Clear','Highlight color','Email','Save changes','Saved','Annotations use the same overlay engine as the Python package.'],es:['Marca elementos y explica la secuencia. El formulario sigue permitiendo clics.','Resaltar','Puntos numerados','Agregar nota','Limpiar','Color del resaltado','Correo','Guardar cambios','Guardado','Las anotaciones usan el mismo motor visual que el paquete Python.']};
function language(){const l=labels[demoLanguage];['intro','highlight','dots','note','clear','color-label','profile-label','save'].forEach((id,i)=>document.getElementById(id).textContent=l[i]);document.getElementById('help').textContent=l[9];document.documentElement.lang=demoLanguage;}
document.getElementById('highlight').onclick=()=>add('email','highlight','','top',document.getElementById('color').value);
document.getElementById('dots').onclick=()=>{add('email','dot','1','left',document.getElementById('dot-color').value);add('save','dot','2','left',document.getElementById('dot-color').value);};
document.getElementById('note').onclick=()=>add('save','note',demoLanguage==='es'?'Guardar los cambios':'Save the changes','right',document.getElementById('note-color').value);
document.getElementById('clear').onclick=()=>markaOverlay('demo','clear',null,{id:null,group:null});
document.getElementById('save').onclick=()=>document.getElementById('notice').textContent=labels[demoLanguage][8];
language();

function contrastColor(color){const rgb=color.match(/[a-f0-9]{2}/gi).map(v=>parseInt(v,16));return rgb[0]*.299+rgb[1]*.587+rgb[2]*.114>150?'#253044':'#ffffff';}

const controls=demoLanguage==='es'?['Grosor del borde (px)','Color de los puntos','Color de las notas']:['Border width (px)','Dot color','Note color'];['width-label','dot-color-label','note-color-label'].forEach((id,i)=>document.getElementById(id).textContent=controls[i]);
