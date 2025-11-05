document.addEventListener("DOMContentLoaded", async () => {
    // Toggle sections
    document.querySelectorAll(".toggle-header").forEach(header => {
        header.addEventListener("click", () => {
        const target = document.querySelector(header.dataset.target);
        target.style.display = target.style.display === "none" ? "block" : "none";
        });
    });

    // Fetch Expense Breakdown
    const expenseRes = await fetch("/expense-breakdown");
    const expenseData = await expenseRes.json();

    const expenseLabels = expenseData.map(e => e.category || "Uncategorized");
    const expenseTotals = expenseData.map(e => e.total);

    const expenseCtx = document.getElementById("expenseChart").getContext("2d");
    new Chart(expenseCtx, {
        type: "pie",
        data: {
        labels: expenseLabels,
        datasets: [{
            data: expenseTotals,
            backgroundColor: [
            "#2ecc71", "#27ae60", "#1abc9c", "#16a085", "#7bed9f"
            ],
            borderColor: "#fff",
            borderWidth: 2
        }]
        },
        options: {
        plugins: {
            legend: { position: "bottom" },
            title: { display: true, text: "Expenses by Category" }
        }
        }
    });

    // Fetch Balance Trend
    const balanceRes = await fetch("/balance-trend");
    const balanceData = await balanceRes.json();

    const balanceLabels = balanceData.map(b => b.day);
    const balanceValues = balanceData.map(b => b.balance);

    const balanceCtx = document.getElementById("balanceChart").getContext("2d");
    new Chart(balanceCtx, {
        type: "line",
        data: {
        labels: balanceLabels,
        datasets: [{
            label: "Balance",
            data: balanceValues,
            borderColor: "#2ecc71",
            backgroundColor: "rgba(46, 204, 113, 0.2)",
            tension: 0.3,
            fill: true,
            pointRadius: 3
        }]
        },
        options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            title: { display: true, text: "Balance Over Time" }
        },
        scales: {
            y: { beginAtZero: true }
        }
        }
    });
});
