document.addEventListener("DOMContentLoaded", function () {
    const upcomingExamsData = JSON.parse(
        document
            .getElementById("upcoming-exams-data")
            .getAttribute("data-upcoming-exams")
    );

    let currentIndex = 0;

    function showNextExam() {
        const exam = upcomingExamsData[currentIndex];
        document.getElementById("exam-details").textContent =
            exam.name + " | Date: " + exam.exam_date + " |";
        currentIndex = (currentIndex + 1) % upcomingExamsData.length;
    }

    showNextExam();
    setInterval(showNextExam, 5000);
});

document.addEventListener("DOMContentLoaded", function () {
    const subjectsData = JSON.parse(
        document.getElementById("subjects-data").getAttribute("data-subjects")
    );

    const labels = subjectsData.map((subject) => subject.name);
    const progressData = subjectsData.map((subject) => subject.progress);

    const ctx = document.getElementById("donutChart").getContext("2d");
    const donutChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [
                {
                    data: progressData,
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.5)",
                        "rgba(54, 162, 235, 0.5)",
                        "rgba(255, 206, 86, 0.5)",
                        "rgba(75, 192, 192, 0.5)",
                        "rgba(153, 102, 255, 0.5)",
                        "rgba(255, 140, 0, 0.5)",
                        "rgba(127, 255, 0, 0.5)",
                        "rgba(147, 112, 219, 0.5)",
                        "rgba(50, 205, 50, 0.5)",
                    ],
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true,
                position: "bottom",
            },
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
