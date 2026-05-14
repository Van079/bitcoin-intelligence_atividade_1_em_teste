import requests
import json

RPC_USER = "teste"
RPC_PASSWORD = "teste"
RPC_PORT = 38332

RPC_URL = f"http://127.0.0.1:{RPC_PORT}"

headers = {
    "content-type": "application/json"
}

def rpc_call(method, params=[]):

    payload = json.dumps({
        "jsonrpc": "1.0",
        "id": "python",
        "method": method,
        "params": params
    })

    response = requests.post(
        RPC_URL,
        headers=headers,
        data=payload,
        auth=(RPC_USER, RPC_PASSWORD)
    )

    result = response.json()

    if result.get("error"):
        raise Exception(result["error"])

    return result["result"]