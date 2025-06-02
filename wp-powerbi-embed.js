window.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('reportContainer');
  if (!container) {
    console.error("Power BI container not found.");
    return;
  }

  const reportId = container.dataset.reportId || "a6479e28-0ed5-4515-90ec-af205f635699";
  const groupId = container.dataset.groupId || "5c32a84f-0b3d-406c-9097-4930093e3005";
  const datasetId = container.dataset.datasetId || "340c9e95-0459-4b8b-9e36-9c968643d777";

  console.log("Embed Params:", { reportId, groupId, datasetId });

  const sdkScript = document.createElement('script');
  sdkScript.src = 'https://cdn.jsdelivr.net/npm/powerbi-client@2.21.0/dist/powerbi.min.js';

  sdkScript.onload = () => {
    const url = `https://powerbi-token-server.onrender.com/getEmbedToken?reportId=${reportId}&groupId=${groupId}&datasetId=${datasetId}`;
    console.log("Fetching:", url);

    fetch(url)
      .then(res => res.json())
      .then(data => {
        console.log("Response from server:", data);
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
