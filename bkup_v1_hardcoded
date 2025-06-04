window.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('reportContainer');
  if (!container) {
    console.error("Power BI container not found.");
    return;
  }

  const sdkScript = document.createElement('script');
  sdkScript.src = 'https://cdn.jsdelivr.net/npm/powerbi-client@2.21.0/dist/powerbi.min.js';

  sdkScript.onload = () => {
    fetch("https://powerbi-token-server.onrender.com/getEmbedToken")
      .then(res => res.json())
      .then(data => {
        if (!data.token || !data.embedUrl) {
          container.innerText = "Failed to load embed config.";
          console.error("Embed token response invalid:", data);
          return;
        }

        const models = window['powerbi-client'].models;
        const config = {
          type: 'report',
          id: data.reportId,
          embedUrl: data.embedUrl,
          accessToken: data.token,
          tokenType: models.TokenType.Embed,
          settings: {
            filterPaneEnabled: true,
            navContentPaneEnabled: true
          }
        };

        container.innerHTML = ''; // Clear "Loading..." message
        window.powerbi.embed(container, config);
      })
      .catch(err => {
        container.innerText = "Failed to load Power BI report.";
        console.error("Power BI embed fetch error:", err);
      });
  };

  sdkScript.onerror = () => {
    container.innerText = "Failed to load Power BI SDK.";
    console.error("Power BI SDK load error.");
  };

  document.body.appendChild(sdkScript);
});
