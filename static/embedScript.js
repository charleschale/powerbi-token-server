(function () {
  const sdkScript = document.createElement("script");
  sdkScript.src = "https://cdn.jsdelivr.net/npm/powerbi-client@2.21.0/dist/powerbi.min.js";

  sdkScript.onload = () => {
    const container = document.getElementById("reportContainer");
    const configData = window.PowerBIEmbedConfig || {
      reportId: container.dataset.reportId,
      groupId: container.dataset.groupId,
      datasetId: container.dataset.datasetId,
    };

    const url = `https://powerbi-token-server.onrender.com/getEmbedToken?reportId=${configData.reportId}&groupId=${configData.groupId}&datasetId=${configData.datasetId}`;

    fetch(url)
      .then(res => res.json())
      .then(data => {
        if (!data.token || !data.embedUrl) {
          container.innerText = "Invalid token response.";
          console.error("Token response error:", data);
          return;
        }

        const models = window["powerbi-client"].models;
        const config = {
          type: "report",
          id: configData.reportId,
          embedUrl: data.embedUrl,
          accessToken: data.token,
          tokenType: models.TokenType.Embed,
          settings: {
            layoutType: models.LayoutType.Custom,
            customLayout: {
              displayOption: models.DisplayOption.ActualSize
            },
            panes: {
              navigationPane: { visible: true },
              pageNavigation: {
                visible: true,
                position: models.PageNavigationPosition.Bottom
              }
            }
          }
        };

        container.innerHTML = "";
        const report = powerbi.embed(container, config);

        // === Event hooks start here ===
        report.on("loaded", () => console.log("✅ Power BI report loaded"));

        report.on("error", err => {
          console.error("❌ Power BI render error:", err.detail);
          container.innerText = "Power BI failed to render.";
        });

        // 👇 Add this line to catch visual-specific errors
        report.on("visualRenderFailed", event => {
          console.error("❌ Visual failed to render:", event.detail);
        });
        // === Event hooks end ===
      })
      .catch(err => {
        console.error("Fetch error:", err);
        container.innerText = "Failed to fetch embed token.";
      });
  };

  sdkScript.onerror = () => {
    console.error("❌ Failed to load Power BI SDK");
    document.getElementById("reportContainer").innerText = "Failed to load SDK.";
  };

  document.body.appendChild(sdkScript);
})();
