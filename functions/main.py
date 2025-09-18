import os
import json
from firebase_functions import https_fn
from firebase_functions.options import set_global_options
import firebase_admin
from firebase_admin import auth, credentials

# -----------------------------
# Global Options for Cost Control
# -----------------------------
set_global_options(max_instances=10)

# -----------------------------
# Initialize Firebase Admin
# -----------------------------
service_account_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
if not service_account_json:
    raise RuntimeError("FIREBASE_SERVICE_ACCOUNT environment variable not set")

service_account_info = json.loads(service_account_json)
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# -----------------------------
# User CRUD Endpoints
# -----------------------------

# Create User
@https_fn.on_request()
def create_user(req: https_fn.Request) -> https_fn.Response:
    try:
        data = req.data
        user = auth.create_user(
            email=data["email"],
            password=data["password"],
            display_name=data.get("displayName")
        )
        return https_fn.Response(json.dumps({"uid": user.uid}), status=200, mimetype="application/json")
    except Exception as e:
        return https_fn.Response(json.dumps({"error": str(e)}), status=400, mimetype="application/json")

# Get User
@https_fn.on_request()
def get_user(req: https_fn.Request) -> https_fn.Response:
    try:
        uid = req.args.get("uid")
        user = auth.get_user(uid)
        return https_fn.Response(
            json.dumps({"uid": user.uid, "email": user.email, "displayName": user.display_name}),
            status=200, mimetype="application/json"
        )
    except Exception as e:
        return https_fn.Response(json.dumps({"error": str(e)}), status=400, mimetype="application/json")

# Update User
@https_fn.on_request()
def update_user(req: https_fn.Request) -> https_fn.Response:
    try:
        data = req.data
        uid = data["uid"]
        user = auth.update_user(
            uid,
            email=data.get("email"),
            display_name=data.get("displayName")
        )
        return https_fn.Response(
            json.dumps({"uid": user.uid, "email": user.email, "displayName": user.display_name}),
            status=200, mimetype="application/json"
        )
    except Exception as e:
        return https_fn.Response(json.dumps({"error": str(e)}), status=400, mimetype="application/json")

# Delete User
@https_fn.on_request()
def delete_user(req: https_fn.Request) -> https_fn.Response:
    try:
        data = req.data
        uid = data["uid"]
        auth.delete_user(uid)
        return https_fn.Response(json.dumps({"success": True}), status=200, mimetype="application/json")
    except Exception as e:
        return https_fn.Response(json.dumps({"error": str(e)}), status=400, mimetype="application/json")
