async function loadMempool() {

    const response = await fetch("/api/mempool/summary");

    const data = await response.json();

    document.getElementById("txCount").innerText =
        data.tx_count;

    document.getElementById("avgFee").innerText =
        data.avg_fee_rate;

    document.getElementById("minFee").innerText =
        data.min_fee_rate;

    document.getElementById("maxFee").innerText =
        data.max_fee_rate;

    document.getElementById("lowTx").innerText =
        data.fee_distribution.low;

    document.getElementById("mediumTx").innerText =
        data.fee_distribution.medium;

    document.getElementById("highTx").innerText =
        data.fee_distribution.high;
}

async function loadBlockchainLag() {

    const response = await fetch("/api/blockchain/lag");

    const data = await response.json();

    document.getElementById("blocks").innerText =
        data.blocks;

    document.getElementById("headers").innerText =
        data.headers;

    document.getElementById("lag").innerText =
        data.lag;
}

async function updateDashboard() {

    await loadMempool();

    await loadBlockchainLag();
}

updateDashboard();

setInterval(updateDashboard, 5000);