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

Set the required credentials using environment variables before starting the app:

```bash
export TENANT_ID="<your AAD tenant ID>"
export CLIENT_ID="<your AAD application ID>"
export CLIENT_SECRET="<your AAD app client secret>"
```

The allowed CORS domains are defined in `app.py` and can be adjusted if needed.

## Running the server

After installing the dependencies and setting the environment variables, start the Flask app:

```bash
python app.py
```

The server will listen on port `5000` by default. The embed token endpoint will be available at `http://localhost:5000/getEmbedToken`.

## Embedding in WordPress

Include `embedScript.js` on your WordPress page and provide the report information using attributes (or by defining `window.PowerBIEmbedConfig` before the script loads). The optional `embed.css` file styles the embedded report. If no `<link id="powerbi-embed-styles">` element is present, the script automatically creates one pointing to `embed.css` located next to the script:

```html
<!-- Optional: include the stylesheet yourself (the script adds it automatically) -->
<link id="powerbi-embed-styles" rel="stylesheet" href="/path/to/embed.css">
<div id="reportContainer"
     data-report-id="<report-id>"
     data-group-id="<workspace-id>"
     data-dataset-id="<dataset-id>"
     data-server-url="http://localhost:5000"><!-- optional override -->
  Loading Power BI...
</div>
<script src="/path/to/embedScript.js"></script>
```

The `embed2.css` stylesheet defines a `--header-height` CSS custom property with
a default value of `80px`. You can override this variable in your own CSS if
your theme's header height differs:

```css
:root {
  --header-height: 80px;
}
```

By default the script contacts `https://powerbi-token-server.onrender.com` for tokens.
To use a different endpoint, provide a `data-server-url` attribute or define
`window.PowerBIEmbedConfig.serverUrl` before the script loads:

```html
<!-- Option 1: set the attribute on the container -->
<div id="reportContainer" data-server-url="https://my-token-server.example.com"></div>

<!-- Option 2: configure the global before loading the script -->
<script>
  window.PowerBIEmbedConfig = {
    serverUrl: "https://my-token-server.example.com"
  };
</script>
<script src="/path/to/embedScript.js"></script>
```

The script fetches an embed token from your Flask server and renders the report using the Power BI client library.

### WordPress-ready snippet

The example snippet above can be saved as an HTML file for a WordPress **Custom HTML** block. It loads the `embed.css` stylesheet and the `embedScript.js` script and exposes the same `data-*` attributes for configuration.

### Testing locally

Copy the `embed-html` file anywhere on your system to try the embed code outside of WordPress. Set the required `data-report-id`, `data-group-id` and `data-dataset-id` attributes to your own IDs. To use a token server other than `https://powerbi-token-server.onrender.com`, provide its address with a `data-server-url` attribute or by defining `window.PowerBIEmbedConfig.serverUrl` before the script loads.
Save the snippet above as an HTML file and paste it into a Custom HTML block, editing the IDs as needed.

## Running tests

Install the dependencies before running the test suite so `pytest` can import the `app` module:

```bash
pip install -r requirements.txt
pytest
```

The CI workflow under `.github/workflows/python-tests.yml` installs the same packages automatically.

## License

This project is licensed under the [MIT License](LICENSE).
