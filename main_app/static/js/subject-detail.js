document.addEventListener("DOMContentLoaded", function () {
    const progressValue = parseInt(
        document.getElementById("progressChart").getAttribute("data-progress")
    );

    const data = {
        labels: ["Completed", "Remaining"],
        datasets: [
            {
                data: [progressValue, 100 - progressValue],
                backgroundColor: ["#F6D55C", "#3CAEA3"],
                hoverBackgroundColor: ["#FFB627", "#218F86"],
            },
        ],
    };

    const ctx = document.getElementById("progressChart").getContext("2d");

    const myPieChart = new Chart(ctx, {
        type: "pie",
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: "white",
                    },
                },
            },
        },
    });
});
