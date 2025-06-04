window.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('reportContainer');
  if (!container) {
    console.error("❌ Power BI container not found.");
    return;
  }

  const config = window.PowerBIEmbedConfig || {};
  const { reportId, groupId, datasetId } = config;

  if (!reportId || !groupId || !datasetId) {
    container.innerText = "❌ Missing embed configuration.";
    console.error("❌ Required IDs are missing:", config);
    return;
  }

  const sdkScript = document.createElement('script');
  sdkScript.src = 'https://cdn.jsdelivr.net/npm/powerbi-client@2.21.0/dist/powerbi.min.js';

  sdkScript.onload = () => {
    const url = `https://powerbi-token-server.onrender.com/getEmbedToken?reportId=${reportId}&groupId=${groupId}&datasetId=${datasetId}`;
    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error(`Server responded with ${res.status}`);
        return res.json();
      })
      .then(data => {
        if (!data.token || !data.embedUrl) {
          container.innerText = "❌ Invalid embed token received.";
          console.error("❌ Server response invalid:", data);
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

        container.innerHTML = '';
        window.powerbi.embed(container, config);
      })
      .catch(err => {
        container.innerText = "❌ Failed to load Power BI report.";
        console.error("❌ Fetch or embed error:", err);
      });
  };

  sdkScript.onerror = () => {
    container.innerText = "❌ Failed to load Power BI SDK.";
    console.error("❌ SDK script load error.");
  };

  document.body.appendChild(sdkScript);
});
