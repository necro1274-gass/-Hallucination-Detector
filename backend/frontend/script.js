async function analyze() {
    const text = document.getElementById("inputText").value;
    const resultsDiv = document.getElementById("results");
    const loading = document.getElementById("loading");

    resultsDiv.innerHTML = "";
    loading.classList.remove("hidden");

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ response: text })
        });

        const data = await response.json();
        const resultData = data.results; // 👈 IMPORTANT

        loading.classList.add("hidden");

        // 🔥 SUMMARY SECTION
        const score = resultData.hallucination_score;

        let color = "green";
        if (score > 30) color = "orange";
        if (score > 60) color = "red";

        const summary = document.createElement("div");
        summary.className = "card";

        summary.innerHTML = `
            <h3>📊 Analysis Summary</h3>

            <div class="score">
                Hallucination Score: <b style="color:${color}">${score}%</b>
            </div>

            <div class="progress-bar">
                <div class="progress" style="width:${score}%; background:${color}"></div>
            </div>

            <p><b>Total Claims:</b> ${resultData.total_claims}</p>
            <p><b>False Claims:</b> ${resultData.false_claims}</p>
        `;

        let verdict = "✅ Reliable";
        if (score > 30) verdict = "⚠️ Mixed Accuracy";
        if (score > 60) verdict = "❌ Likely Hallucinated";
        summary.innerHTML += `
            <p style="margin-top:10px; font-size:18px;">
                <b>AI Verdict:</b> ${verdict}
            </p>
        `;

        resultsDiv.appendChild(summary);
        // 🔥 CLAIMS SECTION
        resultData.results.forEach(item => {
            const card = document.createElement("div");
            card.className = "card " + item.verification.status;

            card.innerHTML = `
                <p><b>Status:</b> 
                <span style="color:${item.verification.status === "false" ? "red" : "lime"}">
                ${item.verification.status.toUpperCase()}
                </span>
                </p>
                <p><b>Status:</b> ${item.verification.status}</p>
                <p><b>Confidence:</b> ${item.verification.confidence}</p>
                <p><b>Reason:</b> ${item.verification.reason}</p>
            `;

            resultsDiv.appendChild(card);
        });

    } catch (error) {
        loading.classList.add("hidden");
        alert("Backend not connected or error occurred");
        console.error(error);
    }
}