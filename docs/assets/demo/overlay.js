const markaOverlay = function(){
// Every browser context owns its annotations. No original styles are modified.
const [owner, action, element, options] = arguments;
const key = '__marka_' + owner;
if (action === 'add' && (!CSS.supports('color',options.color) || !CSS.supports('color',options.background) || !CSS.supports('color',options.text_color))) throw new Error('Invalid CSS color');
let state = window[key];
if (!state && action === 'add') {
  const root = document.createElement('div');
  root.dataset.markaRoot = owner;
  root.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:2147483646;overflow:hidden;';
  document.documentElement.appendChild(root);
  state = window[key] = {root, entries:new Map(), frame:null};
  state.draw = () => {
    for (const entry of state.entries.values()) {
      const r = entry.element.getBoundingClientRect();
      const visible = entry.element.isConnected && r.width > 0 && r.height > 0;
      entry.node.style.display = visible ? 'block' : 'none';
      if (!visible) continue;
      if (entry.kind === 'highlight') {
        Object.assign(entry.node.style,{left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px'});
      } else {
        const position = entry.options.position;
        let x = position === 'left' ? r.left : position === 'right' ? r.right : r.left+r.width/2;
        let y = position === 'top' ? r.top : position === 'bottom' ? r.bottom : r.top+r.height/2;
        if (entry.kind === 'note' || entry.kind === 'label') {
          if (position === 'top') y -= entry.node.offsetHeight/2 + 10;
          if (position === 'bottom') y += entry.node.offsetHeight/2 + 10;
          if (position === 'left') x -= entry.node.offsetWidth/2 + 10;
          if (position === 'right') x += entry.node.offsetWidth/2 + 10;
        }
        Object.assign(entry.node.style,{left:Math.max(0,Math.min(innerWidth-entry.node.offsetWidth,x-entry.node.offsetWidth/2))+'px',top:Math.max(0,Math.min(innerHeight-entry.node.offsetHeight,y-entry.node.offsetHeight/2))+'px'});
      }
    }
    state.frame = requestAnimationFrame(state.draw);
  };
  state.frame = requestAnimationFrame(state.draw);
}
if (action === 'add') {
  if (!element || !element.isConnected) throw new Error('Marka target is no longer attached');
  if (!CSS.supports('color',options.color) || !CSS.supports('color',options.background)) throw new Error('Invalid CSS color');
  const node = document.createElement('div');
  node.dataset.markaId = options.id;
  node.style.cssText = 'position:absolute;box-sizing:border-box;pointer-events:none;font:600 13px/1.4 Arial,sans-serif;';
  if (options.kind === 'highlight') {
    Object.assign(node.style,{border:options.width+'px '+options.style+' '+options.color,borderRadius:options.radius+'px',background:options.background});
    if (options.text) {
      const label = document.createElement('span'); label.textContent = options.text;
      label.style.cssText = 'position:absolute;left:0;top:0;padding:2px 6px;max-width:100%;overflow-wrap:anywhere;background:'+options.color+';color:'+options.text_color+';border-radius:3px;';
      node.appendChild(label);
    }
  } else {
    node.textContent = options.text;
    Object.assign(node.style,{background:options.color,color:options.text_color,padding:options.kind==='dot'?'0':'8px 12px',borderRadius:options.kind==='dot'?'50%':'7px',maxWidth:'220px',overflowWrap:'anywhere'});
    if (options.kind === 'dot') Object.assign(node.style,{width:options.size+'px',height:options.size+'px',textAlign:'center',lineHeight:options.size+'px'});
    if (options.kind === 'note') {
      const pointer = document.createElement('span');
      pointer.style.cssText = 'position:absolute;width:10px;height:10px;background:'+options.color+';transform:rotate(45deg);left:calc(50% - 5px);bottom:-5px;';
      if (options.position === 'bottom') Object.assign(pointer.style,{top:'-5px',bottom:'auto'});
      if (options.position === 'left') Object.assign(pointer.style,{left:'auto',right:'-5px',top:'calc(50% - 5px)',bottom:'auto'});
      if (options.position === 'right') Object.assign(pointer.style,{left:'-5px',top:'calc(50% - 5px)',bottom:'auto'});
      node.appendChild(pointer);
    }
  }
  state.root.appendChild(node);
  state.entries.set(options.id,{node,element,options,kind:options.kind,group:options.group});
  // Paint synchronously as well as tracking scroll, resize and DOM movement.
  cancelAnimationFrame(state.frame); state.draw();
  return options.id;
}
if (!state) return 0;
if (action === 'clear') {
  let removed = 0;
  for (const [id,entry] of state.entries) {
    if ((!options.id || options.id===id) && (options.group===null || options.group===entry.group)) {
      entry.node.remove(); state.entries.delete(id); removed++;
    }
  }
  if (!state.entries.size) {cancelAnimationFrame(state.frame);state.root.remove();delete window[key];}
  return removed;
}
return state.entries.size;

};
