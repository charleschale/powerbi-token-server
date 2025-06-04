window.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('reportContainer');
  if (!container) {
    console.error("Power BI container not found.");
    return;
  }

  const configData = window.PowerBIEmbedConfig || {};
  const { reportId, groupId, datasetId } = configData;

  console.log("Embed Params:", { reportId, groupId, datasetId });

  if (!reportId || !groupId || !datasetId) {
    container.innerText = "Missing embed configuration data.";
    console.error("Missing report/group/dataset IDs.");
    return;
  }

  const sdkScript = document.createElement('script');
  sdkScript.src = 'https://cdn.jsdelivr.net/npm/powerbi-client@2.21.0/dist/powerbi.min.js';

  sdkScript.onload = () => {
    const url = `https://powerbi-token-server.onrender.com/getEmbedToken?reportId=${reportId}&groupId=${groupId}&datasetId=${datasetId}`;
    console.log("Fetching token from:", url);

    fetch(url)
      .then(res => res.json())
      .then(data => {
        console.log("Server Response:", data);
        if (!data.token || !data.embedUrl) {
          container.innerText = "Failed to load embed config.";
          console.error("Embed token response invalid:", data);
          return;
        }

        const models = window['powerbi-client'].models;
        const isMobile = window.innerWidth < 768;

        const config = {
          type: 'report',
          id: data.reportId,
          embedUrl: data.embedUrl,
          accessToken: data.token,
          tokenType: models.TokenType.Embed,
          settings: {
            layoutType: isMobile ? models.LayoutType.Master : models.LayoutType.Custom,
            navContentPaneEnabled: true,
            panes: {
              navigationPane: { visible: true }
            }
          }
        };

        container.innerHTML = '';
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
