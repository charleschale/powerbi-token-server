defineCustomElement('powerbi-embed', () => {
  const el = document.createElement('div');
  el.innerText = '✅ Custom Element Loaded Successfully';
  el.style.background = '#e0ffe0';
  el.style.padding = '20px';
  el.style.fontSize = '20px';
  return el;
});
