from flask import Flask, render_template, request, redirect, url_for, session
from azure.storage.blob import BlobServiceClient
from config import Config
import msal
import os
import uuid

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)



# Azure Blob Setup
blob_service_client = BlobServiceClient.from_connection_string(Config.AZURE_STORAGE_CONNECTION_STRING)
container_name = Config.AZURE_STORAGE_CONTAINER_NAME

# MSAL for Entra ID
def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        Config.CLIENT_ID,
        authority=Config.AUTHORITY,
        client_credential=Config.CLIENT_SECRET,
        token_cache=cache
    )

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    blobs = blob_service_client.get_container_client(container_name).list_blobs()
    return render_template("index.html", blobs=blobs)

@app.route("/login")
def login():
    auth_url = _build_msal_app().get_authorization_request_url(
        Config.SCOPE,
        redirect_uri=Config.REDIRECT_URI
    )
    return redirect(auth_url)

@app.route("/getAToken")
def authorized():
    code = request.args.get("code")
    if not code:
        return "Login failed", 400

    app_msal = _build_msal_app()
    result = app_msal.acquire_token_by_authorization_code(
        code, scopes=Config.SCOPE, redirect_uri=Config.REDIRECT_URI
    )

    if "id_token_claims" in result:
        session["user"] = result["id_token_claims"]
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri={url_for('index', _external=True)}"
    )

@app.route("/create", methods=["GET", "POST"])
def create():
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        body = request.form["body"]
        image = request.files["image"]

        if image:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=image.filename)
            blob_client.upload_blob(image.stream, overwrite=True)
            image_url = f"https://{Config.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{container_name}/{image.filename}"
        else:
            image_url = None

        return render_template("index.html", title=title, author=author, body=body, image_url=image_url)

    return render_template("create.html")


# Azure expects a variable named 'application' for WSGI entry
application = app

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=5000, debug=True)
