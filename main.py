"""Python Flask WebApp OAuth 2.0 Authorization code flow example
"""

import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import Flask, abort, redirect, render_template, session, url_for

appConf = {
    "OAUTH2_CLIENT_ID": "mywebapp",
    "OAUTH2_CLIENT_SECRET": "kpUdB9LnM5DNUUlqT0nIy2WGN7HcS5TG",
    "OAUTH2_ISSUER": "http://localhost:8080/realms/myorg",
    "FLASK_SECRET": "ALongRandomlyGeneratedString",
    "FLASK_PORT": 3000
}

app = Flask(__name__)
app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
        # 'code_challenge_method': 'S256'  # enable PKCE
    },
    server_metadata_url=f'{appConf.get("OAUTH2_ISSUER")}/.well-known/openid-configuration',
)


@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback")
def callback():
    token = oauth.myApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))


@app.route("/login")
def login():
    # check if session already present
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/loggedout")
def loggedOut():
    # check if session already present
    if "user" in session:
        abort(404)
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    # https://stackoverflow.com/a/72011979/2746323
    id_token = session["user"]["id_token"]
    session.clear()
    return redirect(
        appConf.get("OAUTH2_ISSUER")
        + "/protocol/openid-connect/logout?"
        + urlencode(
            {
                "post_logout_redirect_uri": url_for("loggedOut", _external=True),
                "id_token_hint": id_token
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=appConf.get("FLASK_PORT", 3000), debug=False)
