import { defineCustomElement } from '@wix/custom-elements';

defineCustomElement('powerbi-embed', () => {
  const container = document.createElement('div');
  container.id = 'reportContainer';
  container.style.width = '100%';
  container.style.height = '100%';

  const sdkScript = document.createElement('script');
  sdkScript.src = 'https://cdn.jsdelivr.net/npm/powerbi-client@2.21.0/dist/powerbi.min.js';
  sdkScript.onload = () => {
    fetch("https://powerbi-token-server.onrender.com/getEmbedToken")
      .then(res => res.json())
      .then(data => {
        const models = window['powerbi-client'].models;
        const config = {
          type: 'report',
          id: data.reportId,
          embedUrl: data.embedUrl,
          accessToken: data.token,
          tokenType: models.TokenType.Embed,
          settings: {
            filterPaneEnabled: false,
            navContentPaneEnabled: true
          }
        };
        window.powerbi.embed(container, config);
      });
  };

  container.appendChild(sdkScript);
  return container;
});
