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

    # Request Azure AD token (add error handling here)
    token_response = app_msal.acquire_token_for_client(scopes=scope)

    if "access_token" not in token_response:
        return jsonify({
            "error": "MSAL failed to acquire token",
            "error_description": token_response.get("error_description"),
            "correlation_id": token_response.get("correlation_id"),
            "raw": token_response
        }), 500

    access_token = token_response["access_token"]

    # Generate Power BI embed token
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
