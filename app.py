from flask import Flask, jsonify
import msal
import requests
import os

app = Flask(__name__)

# Config values
TENANT_ID = "3be3af3c-46a1-461d-93b1-44954da5e032"
CLIENT_ID = "191260ff-ab3f-4d75-a211-780754200954"
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # <-- pulls from Render environment
GROUP_ID = "5c32a84f-0b3d-406c-9097-4930093e3005"
DATASET_ID = "340c9e95-0459-4b8b-9e36-9c968643d777"
REPORT_ID = "a6479e28-0ed5-4515-90ec-af205f635699"

@app.route("/getEmbedToken", methods=["GET"])
def get_embed_token():
    authority_url = f"https://login.microsoftonline.com/{TENANT_ID}"
    scope = ["https://analysis.windows.net/powerbi/api/.default"]

    app_msal = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority_url, client_credential=CLIENT_SECRET
    )
    token_response = app_msal.acquire_token_for_client(scopes=scope)
    access_token = token_response.get("access_token")

if not access_token:
    print("MSAL token response:", token_response)  # log real error
    return jsonify({"error": "Unable to authenticate with Azure AD"}), 401


    embed_url = f"https://api.powerbi.com/v1.0/myorg/groups/{GROUP_ID}/reports/{REPORT_ID}/GenerateToken"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payload = {
        "accessLevel": "View",
        "allowSaveAs": False,
        "allowUncertifiedVisuals": True,
        "identities": []
    }

    response = requests.post(embed_url, headers=headers, json=payload)
    if response.status_code != 200:
        return jsonify({"error": "Failed to generate embed token", "details": response.text}), 500

    token = response.json()["token"]
    embed_iframe_url = f"https://app.powerbi.com/reportEmbed?reportId={REPORT_ID}&groupId={GROUP_ID}"

    return jsonify({
        "token": token,
        "embedUrl": embed_iframe_url,
        "reportId": REPORT_ID
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
