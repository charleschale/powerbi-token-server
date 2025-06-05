# Power BI Token Server

This Flask application returns an embed token for a Power BI report so it can be displayed on a website. It exposes a single endpoint `/getEmbedToken` which expects `reportId`, `groupId` and `datasetId` query parameters.

## Requirements

* Python 3.10 or newer
* The packages listed in `requirements.txt`

It is recommended to create a virtual environment before installing dependencies.
Make sure to specify the Python version when creating the environment:

```bash
# Windows
py -3.10 -m venv venv
# macOS/Linux
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, running `\.venv\Scripts\Activate.ps1` may be blocked by the execution policy. Temporarily bypass it with:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1
```

Use `venv\Scripts\activate.bat` for the Command Prompt.

## Configuration

Update `TENANT_ID`, `CLIENT_ID` and the allowed CORS domain at the top of `app.py` if needed. The application expects a `CLIENT_SECRET` environment variable. Set it in your shell before starting the app:

```bash
export CLIENT_SECRET="<your AAD app client secret>"
```

## Running the server

After installing the dependencies and setting `CLIENT_SECRET`, start the Flask app:

```bash
python app.py
```

The server will listen on port `5000` by default. The embed token endpoint will be available at `http://localhost:5000/getEmbedToken`.

## Embedding in WordPress

Include `wp-powerbi-embed.js` on your WordPress page and define the Power BI configuration before loading the script:

```html
<div id="reportContainer" style="height:600px;"></div>
<script>
  window.PowerBIEmbedConfig = {
    reportId: "<report-id>",
    groupId: "<workspace-id>",
    datasetId: "<dataset-id>"
  };
</script>
<script src="/path/to/wp-powerbi-embed.js"></script>
```

The script fetches an embed token from your Flask server and renders the report using the Power BI client library.
