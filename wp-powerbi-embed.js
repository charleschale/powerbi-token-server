window.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('reportContainer');
  if (!container) return;

  container.innerText = 'Loading Power BI...';
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
        container.innerText = ''; // Clear loading message
        window.powerbi.embed(container, config);
      })
      .catch(err => {
        container.innerText = 'Failed to load Power BI report.';
        console.error('Power BI embed error:', err);
      });
  };

  sdkScript.onerror = () => {
    container.innerText = 'Failed to load Power BI SDK.';
    console.error('Power BI SDK load error.');
  };

  document.body.appendChild(sdkScript);
});

