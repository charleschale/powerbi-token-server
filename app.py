from flask import Flask, jsonify, request
from flask_cors import CORS
import msal
import requests
import os

app = Flask(__name__)
CORS(app, origins=["https://work.hale.global"])

TENANT_ID = "3be3af3c-46a1-461d-93b1-44954da5e032"
CLIENT_ID = "191260ff-ab3f-4d75-a211-780754200954"
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

@app.route("/getEmbedToken", methods=["GET"])
def get_embed_token():
    report_id = request.args.get("reportId")
    group_id = request.args.get("groupId")
    dataset_id = request.args.get("datasetId")

    if not all([report_id, group_id, dataset_id]):
        return jsonify({"error": "Missing one or more query parameters."}), 400

    authority_url = f"https://login.microsoftonline.com/{TENANT_ID}"
    scope = ["https://analysis.windows.net/powerbi/api/.default"]

    app_msal = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority_url, client_credential=CLIENT_SECRET
    )
    token_response = app_msal.acquire_token_for_client(scopes=scope)
    access_token = token_response.get("access_token")

    if not access_token:
        return jsonify({"error": "Unable to authenticate with Azure AD", "details": token_response}), 401

    embed_url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/GenerateToken"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "accessLevel": "View",
        "allowSaveAs": False,
        "allowUncertifiedVisuals": True,
        "datasets": [{"id": dataset_id}]
    }

    response = requests.post(embed_url, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "Failed to generate embed token", "details": response.text}), 500

    token = response.json().get("token")
    embed_iframe_url = f"https://app.powerbi.com/reportEmbed?reportId={report_id}&groupId={group_id}"

    return jsonify({
        "token": token,
        "embedUrl": embed_iframe_url,
        "reportId": report_id
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
