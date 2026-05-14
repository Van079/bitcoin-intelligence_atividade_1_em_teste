from flask import Flask, jsonify, render_template
from rpc import rpc_call

app = Flask(__name__)

# =========================
# FRONTEND
# =========================

@app.route("/")
def index():
    return render_template("index.html")

# =========================
# MEMPOOL SUMMARY
# =========================

@app.route("/api/mempool/summary")
def mempool_summary():

    mempool_info = rpc_call("getmempoolinfo")
    raw_mempool = rpc_call("getrawmempool", [True])

    tx_count = mempool_info["size"]
    total_vsize = mempool_info["bytes"]

    fee_rates = []

    distribution = {
        "low": 0,
        "medium": 0,
        "high": 0
    }

    for txid, tx in raw_mempool.items():

        fee_btc = tx.get("fees", {}).get("base", 0)
        vsize = tx.get("vsize", 1)

        fee_sat = fee_btc * 100000000

        fee_rate = fee_sat / vsize

        fee_rates.append(fee_rate)

        # CLASSIFICAÇÃO
        if fee_rate < 10:
            distribution["low"] += 1

        elif fee_rate <= 50:
            distribution["medium"] += 1

        else:
            distribution["high"] += 1

    avg_fee = round(sum(fee_rates) / len(fee_rates), 2) if fee_rates else 0
    min_fee = round(min(fee_rates), 2) if fee_rates else 0
    max_fee = round(max(fee_rates), 2) if fee_rates else 0

    return jsonify({
        "tx_count": tx_count,
        "total_vsize": total_vsize,
        "avg_fee_rate": avg_fee,
        "min_fee_rate": min_fee,
        "max_fee_rate": max_fee,
        "fee_distribution": distribution
    })

# =========================
# BLOCKCHAIN LAG
# =========================

@app.route("/api/blockchain/lag")
def blockchain_lag():

    info = rpc_call("getblockchaininfo")

    blocks = info["blocks"]
    headers = info["headers"]

    lag = headers - blocks

    return jsonify({
        "blocks": blocks,
        "headers": headers,
        "lag": lag
    })

if __name__ == "__main__":
    app.run(debug=True)