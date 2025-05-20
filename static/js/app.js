document.addEventListener("DOMContentLoaded", function() {
    console.log("Script cargado correctamente"); // Verificar carga
    document.getElementById("imagenEstadio").classList.add("hidden"); // Oculta la imagen al inicio
});

function calcularTFG() {
    const altura = document.getElementById("altura").value;
    const creatinina = document.getElementById("creatinina").value;

    if (!altura || !creatinina) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    fetch('/calcular_tfg', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ altura, creatinina }) // Se eliminó "grupo"
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta API:", data); // Debug en consola

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("resultado").innerText = `TFG: ${data.TFG} mL/min/1.73m²`;
        document.getElementById("estadio").innerText = `🩺 Estadio: ${data.Estadio}`;
        document.getElementById("recomendacion").innerText = `📢 Recomendación: ${data.Recomendación}`;

        let colorMap = {
            "Estadio 1": "green",
            "Estadio 2": "yellow",
            "Estadio 3": "orange",
            "Estadio 4": "red",
            "Estadio 5": "darkred"
        };

        document.getElementById("estadio").style.color = colorMap[data.Estadio] || "gray";

        document.querySelector(".result-section").style.display = "block";
    })
    .catch(error => console.error("Error:", error));
}

