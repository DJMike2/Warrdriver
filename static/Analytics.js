document.addEventListener("DOMContentLoaded", function () {


    const chartData = {
        labels: ["1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s"],
        datasets: [{
            label: 'CPU Usage',
            data: [10, 20, 30, 25, 35, 40, 30, 20, 15, 10], // Replace with your CPU usage data
            borderColor: 'blue',
            borderWidth: 2,
            fill: false
        }]
    };

    const canvas2 = document.getElementById('cpuUsageChart');
    const ctx2 = canvas2.getContext('2d');

    const chart = new Chart(ctx2, {
        type: 'line',
        data: chartData,
        options: {
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time (s)'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'CPU Usage (%)'
                    }
                }
            }
        }
    });












    const canvas = document.getElementById("pieChart");
    const ctx = canvas.getContext("2d");
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = canvas.width / 3;

    const colors = ["#6A5ACD", "#005C6E", "#C85A75", "#708090"]; // Colors for each segment
    const colorValues = ["WPS", "WPA", "WPA2", "WPA3"]; // Corresponding values for each color

    let data = [0, 2, 10, 1]; // Values for the pie chart segments
    let startAngle = -Math.PI / 2;
    let targetData = data.slice();
    let animationFrameId;
    let animationDuration = 2000; // Animation duration in milliseconds
    let animationStartTime;

    function drawPieSegment(startAngle, endAngle, color, number) {
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.closePath();
        ctx.fillStyle = color;
        ctx.fill();

        // Calculate the position for the percentage text
        const textX = centerX + radius * 0.7 * Math.cos(startAngle + (endAngle - startAngle) / 2);
        const textY = centerY + radius * 0.7 * Math.sin(startAngle + (endAngle - startAngle) / 2);

        // Display the percentage inside the pie chart
        ctx.fillStyle = "#ffffff"; // Set text color to white for visibility
        ctx.font = "10px Arial";
        ctx.textAlign = "center";
        ctx.fillText(Math.round(number), textX, textY);
    }

    function updatePieChart() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let total = 0;

        for (let i = 0; i < data.length; i++) {
            total += data[i];
        }

        for (let i = 0; i < data.length; i++) {
            const sliceAngle = (Math.PI * 2 * data[i]) / total;
            const endAngle = startAngle + sliceAngle;
            const number = (data[i]);//Pie chart data inside
            drawPieSegment(startAngle, endAngle, colors[i], Math.round(number));
            startAngle = endAngle;
        }
    }

    function animateChart(timestamp) {
        if (!animationStartTime) {
            animationStartTime = timestamp;
        }

        const progress = timestamp - animationStartTime;
        if (progress < animationDuration) {
            for (let i = 0; i < data.length; i++) {
                const diff = targetData[i] - data[i];
                const increment = (diff / animationDuration) * progress;
                data[i] += increment;
            }
            updatePieChart();
            animationFrameId = requestAnimationFrame(animateChart);
        } else {
            // Animation complete
            data = targetData.slice();
            updatePieChart();
            cancelAnimationFrame(animationFrameId);
        }
    }

    // Initial drawing
    updatePieChart();

    // Example: Update chart when values change
    setTimeout(() => {
        targetData = [0, 5, 15, 5]; // New values
        animationStartTime = null; // Reset animation start time
        cancelAnimationFrame(animationFrameId);
        requestAnimationFrame(animateChart);
    }, 2000); // Update after 2 seconds

    // Display legend with color values
    const legend = document.getElementById("legend");
    for (let i = 0; i < colors.length; i++) {
        legend.innerHTML += `<div style="color: ${colors[i]};font-size: 12px;font-weight:bold;">${colorValues[i]}</div>`;
    }
});