# authentik-webfinger
webfinger sidecar container for authentik + tailscale


Clone repo

adjust line 17 in webfinger.py to point to your authentik instance

docker build -t webfinger .

docker run -p 8000:8000 webfinger
