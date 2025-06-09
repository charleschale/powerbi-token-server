
(function () {
  const container = document.getElementById("reportContainer");
  const loading = document.createElement("div");
  loading.id = "powerbi-loading";
  loading.textContent = "Loading Power BI...";
  loading.style.position = "absolute";
  loading.style.top = "0";
  loading.style.left = "0";
  loading.style.right = "0";
  loading.style.bottom = "0";
  loading.style.display = "flex";
  loading.style.alignItems = "center";
  loading.style.justifyContent = "center";
  loading.style.backgroundColor = "rgba(255, 255, 255, 0.8)";
  loading.style.zIndex = "2000";
  if (getComputedStyle(container).position === "static") {
    container.style.position = "relative";
  }
  container.appendChild(loading);

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
          loading.remove();
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
        report.on("loaded", () => {
          loading.remove();
          console.log("✅ Power BI report loaded");
        });
        report.on("error", err => {
          console.error("❌ Power BI render error:", err.detail);
          container.innerText = "Power BI failed to render.";
          loading.remove();
        });
      })
      .catch(err => {
        console.error("Fetch error:", err);
        container.innerText = "Failed to fetch embed token.";
        loading.remove();
      });
  };

  sdkScript.onerror = () => {
    console.error("❌ Failed to load Power BI SDK");
    document.getElementById("reportContainer").innerText = "Failed to load SDK.";
    loading.remove();
  };

  document.body.appendChild(sdkScript);
})();
