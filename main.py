import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import json
import hmac
import hashlib
import requests

load_dotenv()

SUBMISSION_URL = os.environ.get("SUBMISSION_URL")
SIGNING_SECRET = os.environ.get("SIGNING_SECRET")
RESUME_LINK = os.environ.get("RESUME_LINK")
REPOSITORY_LINK = os.environ.get("REPOSITORY_LINK")
ACTION_RUN_LINK = os.environ.get("ACTION_RUN_LINK")


def get_encoded_payload() -> str:
    payload = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "name": "Avenir Dumani",
        "email": "dumaniavenir@gmail.com",
        "resume_link": RESUME_LINK,
        "repository_link": REPOSITORY_LINK,
        "action_run_link": ACTION_RUN_LINK,
    }
    return json.dumps(obj=payload, sort_keys=True, separators=(",", ":"))


def get_header_signature(payload: str) -> str:
    encoded_key = SIGNING_SECRET.encode()
    digest = hmac.new(
        key=encoded_key,
        msg=payload.encode(),
        digestmod=hashlib.sha256,
    )
    return digest.hexdigest()


def make_request() -> None:
    payload = get_encoded_payload()
    header_signature = get_header_signature(payload=payload)
    headers = {"X-Signature-256": f"sha256={header_signature}"}

    submission_request = requests.post(
        url=SUBMISSION_URL,
        headers=headers,
        data=payload,
    )
    result = submission_request.text
    with open("result.json", "w") as fd:
        fd.write(result)


if __name__ == "__main__":
    make_request()
