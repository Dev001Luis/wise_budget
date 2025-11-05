// =============================
// Global chart instances
// =============================
window.expenseChartInstance = window.expenseChartInstance || null;
window.balanceChartInstance = window.balanceChartInstance || null;

// =============================
// Utility Functions
// =============================
function getRandomColor() {
    const hue = Math.floor(Math.random() * 360);
    return `hsl(${hue}, 70%, 60%)`;
}

// =============================
// Load Expense Pie Chart
// =============================
// async function loadExpenseChart() {
//     try {
//         const [dataRes, colorRes] = await Promise.all([
//             fetch("/expense-breakdown"),
//             fetch("/category-colors")
//         ]);

//         if (!dataRes.ok || !colorRes.ok) throw new Error("Failed to fetch expense data or colors");

//         const data = await dataRes.json();
//         const colors = await colorRes.json();
//         console.log(colors)

//         const labels = data.map(d => d.category || "Uncategorized");
//         const amounts = data.map(d => d.total);
//         const bgColors = labels.map(cat => colors[cat] || getRandomColor());
//         console.log(bgColors)

//         const ctx = document.getElementById("expenseChart").getContext("2d");

//         if (window.expenseChartInstance) window.expenseChartInstance.destroy();

//         window.expenseChartInstance = new Chart(ctx, {
//             type: "pie",
//             data: { labels, datasets: [{ data: amounts, backgroundColor: bgColors }] },
//             options: { responsive: true, plugins: { legend: { position: "left" } } }
//         });

//     } catch (err) {
//         console.error("Error loading expense chart:", err);
//     }
// }

// =============================
// Load Expense Pie Chart (with auto DB color insert)
// =============================
async function loadExpenseChart() {
    try {
        const [dataRes, colorRes] = await Promise.all([
            fetch("/expense-breakdown"),
            fetch("/category-colors")
        ]);

        if (!dataRes.ok || !colorRes.ok) throw new Error("Failed to fetch expense data or colors");

        const data = await dataRes.json();
        const existingColors = await colorRes.json();
        const newColors = {};

        const labels = data.map(d => d.category || "Uncategorized");
        const amounts = data.map(d => d.total);

        const bgColors = labels.map(cat => {
            if (existingColors[cat]) {
                return existingColors[cat];
            } else {
                const color = getRandomColor();
                newColors[cat] = color;
                return color;
            }
        });

        // Insert missing colors into DB if any
        if (Object.keys(newColors).length > 0) {
            console.log(newColors)
            console.log(JSON.stringify(newColors))
            await fetch("/update-category-colors", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(newColors)
            });
        }

        const ctx = document.getElementById("expenseChart").getContext("2d");
        if (window.expenseChartInstance) window.expenseChartInstance.destroy();

        window.expenseChartInstance = new Chart(ctx, {
            type: "pie",
            data: { labels, datasets: [{ data: amounts, backgroundColor: bgColors }] },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "left" },
                    title: { display: false }
                }
            }
        });
    } catch (err) {
        console.error("Error loading expense chart:", err);
    }
}

// =============================
// Load Balance Line Chart
// =============================
async function loadBalanceChart() {
    try {
        const balanceRes = await fetch("/balance-trend");
        if (!balanceRes.ok) throw new Error("Failed to fetch balance trend");

        const balanceData = await balanceRes.json();
        const labels = balanceData.map(b => b.day);
        const balances = balanceData.map(b => b.balance);

        const ctx = document.getElementById("balanceChart").getContext("2d");

        if (window.balanceChartInstance) window.balanceChartInstance.destroy();

        window.balanceChartInstance = new Chart(ctx, {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: "Balance",
                    data: balances,
                    borderColor: "#2ecc71",
                    backgroundColor: "rgba(46,204,113,0.2)",
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: "Balance Over Time" }
                },
                scales: { y: { beginAtZero: true } }
            }
        });

    } catch (err) {
        console.error("Error loading balance chart:", err);
    }
}

// =============================
// Modal Edit Category Colors
// =============================
async function openEditColorsModal() {
    try {
        const res = await fetch("/edit-colors-modal");
        if (!res.ok) throw new Error("Could not load modal HTML");

        const html = await res.text();
        document.getElementById("modalContainer").innerHTML = html;

        const modalEl = document.getElementById("editColorModal");
        const modal = new bootstrap.Modal(modalEl);
        modal.show();

        // Handle form submission
        const saveBtn = document.getElementById("saveColorsBtn");
        saveBtn.addEventListener("click", async () => {
            const form = document.getElementById("editColorsForm");
            const formData = new FormData(form);
            const colors = {};
            formData.forEach((value, key) => colors[key] = value);

            await fetch("/update-category-colors", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(colors)
            });

            modal.hide();
            await loadExpenseChart(); // refresh chart with updated colors
        });

    } catch (err) {
        console.error("Error opening edit colors modal:", err);
    }
}

// =============================
// Toggle Sections Only for Headers
// =============================
function setupToggleSections() {
    document.querySelectorAll(".toggle-header").forEach(header => {
        header.addEventListener("click", () => {
            const target = document.querySelector(header.dataset.target);
            if (!target) return;
            target.style.display = target.style.display === "none" ? "block" : "none";
        });
    });
}

// =============================
// DOMContentLoaded Initialization
// =============================
document.addEventListener("DOMContentLoaded", async () => {
    setupToggleSections();
    await loadExpenseChart();
    await loadBalanceChart();

    const editBtn = document.getElementById("editColorsBtn");
    if (editBtn) editBtn.addEventListener("click", openEditColorsModal);
});
