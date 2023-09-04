import yaml

from app.authorization.auth import create_authorization_token, decode_authorization_token

# Load config
with open("conf/config.yaml") as f:
    config = yaml.safe_load(f)


def test_create_authorization_token():
    token = create_authorization_token("test@mail.com", config["TOKEN_VALID_DURATION"],
                                                   config["ALGORITHM"], config["SECRET_KEY"])
    assert token.count(".") == 2


def test_decode_authorization_token():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ0ZXN0QG1haWwuY29tIiwiZXhwaXJhdGlvbl90aW1lIjoiMjAyMy0wOS0wNFQxOTo1Nzo1MS45MzAzOTcifQ.AlAcmoUNN19jGeobH_CGQhb1ZIzKuN1aVFuqhoMKV3U"
    payload = decode_authorization_token(token)
    assert payload == {'key': 'test@mail.com', 'expiration_time': '2023-09-04T19:57:51.930397'}

