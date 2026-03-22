
let chart;

function predict() {

    let year = document.getElementById("year").value;
    let mileage = document.getElementById("mileage").value;
    let engine = document.getElementById("engine").value;
    let power = document.getElementById("power").value;


    let features = [
        Number(year),
        Number(mileage),
        Number(engine),
        Number(power)
    ];

  
    if (features.some(isNaN) || features.includes(0)) {
        alert("Please enter all fields correctly!");
        return;
    }

    document.getElementById("result").innerText = "Predicting...";
    document.getElementById("confidence").innerText = "";

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ features: features })
    })
    .then(response => response.json())
    .then(data => {

        
        if (data.error) {
            document.getElementById("result").innerText = data.error;
            return;
        }

      
        document.getElementById("result").innerText =
            "Prediction: ₹ " + data.prediction;

      
        document.getElementById("confidence").innerText =
            "Confidence: " + data.confidence + "%";

       
        drawChart(features);
    })
    .catch(error => {
        console.error(error);
        alert("Server error! Check backend.");
    });
}



function drawChart(data) {

    const labels = ['Year', 'Mileage', 'Engine', 'Power'];

    let ctx = document.getElementById('chart').getContext('2d');

    // Destroy previous chart if exists
    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Feature Impact',
                data: data,
                tension: 0.4,
                fill: true,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}



window.onload = function () {
    drawChart([0, 0, 0, 0]);
};