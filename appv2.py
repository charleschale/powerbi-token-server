from flask import Flask, jsonify, request
from flask_cors import CORS
import msal
import requests
import os
import re

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app, origins=["https://work.hale.global", "https://haleglobal.com", "https://www.haleglobal.com"])

# Azure AD / Power BI credentials
TENANT_ID = os.getenv("TENANT_ID", "3be3af3c-46a1-461d-93b1-44954da5e032")
CLIENT_ID = os.getenv("CLIENT_ID", "191260ff-ab3f-4d75-a211-780754200954")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def is_valid_guid(value):
    return re.fullmatch(r'[a-fA-F0-9\-]{36}', value or '') is not None

@app.route("/getEmbedToken", methods=["GET"])
def get_embed_token():
    # Get query params
    report_id = request.args.get("reportId")
    group_id = request.args.get("groupId")
    dataset_id = request.args.get("datasetId")
    user_email = request.args.get("username")  # Optional for RLS

    # Debug log
    print("Embed token request received:")
    print("  Report ID:", report_id)
    print("  Group ID:", group_id)
    print("  Dataset ID:", dataset_id)
    if user_email:
        print("  Username (for RLS):", user_email)

    # Validate inputs
    if not all([report_id, group_id, dataset_id]):
        return jsonify({"error": "Missing one or more query parameters."}), 400

    if not (is_valid_guid(report_id) and is_valid_guid(group_id) and is_valid_guid(dataset_id)):
        return jsonify({"error": "One or more parameters are not valid GUIDs."}), 400

    # Get Azure AD token
    authority_url = f"https://login.microsoftonline.com/{TENANT_ID}"
    scope = ["https://analysis.windows.net/powerbi/api/.default"]

    app_msal = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority_url,
        client_credential=CLIENT_SECRET
    )

    token_response = app_msal.acquire_token_for_client(scopes=scope)

    if "access_token" not in token_response:
        return jsonify({
            "error": "Failed to acquire Azure AD token.",
            "details": token_response
        }), 500

    access_token = token_response["access_token"]

    # Construct embed payload
    payload = {
        "accessLevel": "View",
        "allowSaveAs": False,
        "allowUncertifiedVisuals": True,
        "datasets": [{"id": dataset_id}]
    }

    if user_email:
        payload["identities"] = [{
            "username": user_email,
            "roles": ["UserEmailRole"],
            "datasets": [dataset_id]
        }]

    # Call Power BI API to generate token
    embed_url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}/GenerateToken"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(embed_url, headers=headers, json=payload)

    if response.status_code != 200:
        print("❌ Embed token generation failed")
        print("➡️  Payload sent:", payload)
        print("📥  API Response:", response.text)
        print("🔐  Email passed:", user_email)
        print("📊  Dataset ID:", dataset_id)
        print("🧾  Report ID:", report_id)

        return jsonify({
            "error": "Failed to generate embed token",
            "status": response.status_code,
            "response": response.text,
            "payload_used": payload
        }), 500

    token = response.json().get("token")
    embed_iframe_url = f"https://app.powerbi.com/reportEmbed?reportId={report_id}&groupId={group_id}"

    return jsonify({
        "token": token,
        "embedUrl": embed_iframe_url,
        "reportId": report_id
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
