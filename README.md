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

Include `wp-powerbi-embed.js` on your WordPress page and provide the report information using attributes (or by defining `window.PowerBIEmbedConfig` before the script loads). The optional `powerbi-embed.css` file styles the embedded report. If no `<link id="powerbi-embed-styles">` element is present, the script automatically creates one pointing to `powerbi-embed.css` located next to the script:

```html
<!-- Optional: include the stylesheet yourself (the script adds it automatically) -->
<link id="powerbi-embed-styles" rel="stylesheet" href="/path/to/powerbi-embed.css">
<div id="reportContainer"
     data-report-id="<report-id>"
     data-group-id="<workspace-id>"
     data-dataset-id="<dataset-id>"
     data-server-url="http://localhost:5000"><!-- optional override -->
  Loading Power BI...
</div>
<script src="/path/to/wp-powerbi-embed.js"></script>
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
<script src="/path/to/wp-powerbi-embed.js"></script>
```

The script fetches an embed token from your Flask server and renders the report using the Power BI client library.

### WordPress-ready snippet

An example file `embed-html-wordpress.html` contains the markup needed for a WordPress **Custom HTML** block. It loads the `powerbi-embed.css` stylesheet and the `wp-powerbi-embed.js` script and exposes the same `data-*` attributes for configuration.

### Testing locally

Copy the `embed-html` file anywhere on your system to try the embed code outside of WordPress. Set the required `data-report-id`, `data-group-id` and `data-dataset-id` attributes to your own IDs. To use a token server other than `https://powerbi-token-server.onrender.com`, provide its address with a `data-server-url` attribute or by defining `window.PowerBIEmbedConfig.serverUrl` before the script loads.
A WordPress-ready snippet is available in `embed-html-wordpress.html`. Paste it into a Custom HTML block and edit the IDs as needed.

## Running tests

Install the dependencies before running the test suite so `pytest` can import the `app` module:

```bash
pip install -r requirements.txt
pytest
```

The CI workflow under `.github/workflows/python-tests.yml` installs the same packages automatically.

## License

This project is licensed under the [MIT License](LICENSE).
