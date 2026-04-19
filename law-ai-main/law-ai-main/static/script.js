document.addEventListener("DOMContentLoaded", function () {
    const generateBtn = document.getElementById("generate");
    const countryInput = document.getElementById("country");
    const situationInput = document.getElementById("situation");
    const responseContainer = document.getElementById("response-container");
    const responseText = document.getElementById("response");
    const loading = document.getElementById("loading");

    generateBtn.addEventListener("click", async function () {
        let country = countryInput.value.trim();
        let situation = situationInput.value.trim();

        if (!country || !situation) {
            alert("⚠️ Please select a country and describe the legal situation.");
            return;
        }

        // Disable button and show loading
        generateBtn.disabled = true;
        generateBtn.innerText = "Generating...";
        loading.style.display = "block";
        responseContainer.style.display = "none";
        responseText.innerHTML = "";

        try {
            let response = await fetch("/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ country, situation }),
            });

            let data = await response.json();

            loading.style.display = "none";
            generateBtn.disabled = false;
            generateBtn.innerText = "Generate Response";
            responseContainer.style.display = "block";

            if (data.response) {
                responseText.innerHTML = `
                    <h3 style="color: #2a5298;">Legal Advice for <strong>${country}</strong>:</h3>
                    <p style="text-align: left;">${data.response.replace(/\n/g, "<br>")}</p>
                `;
            } else {
                responseText.innerHTML = "<strong style='color: red;'>Error:</strong> Unable to generate a response.";
            }
        } catch (error) {
            console.error("Error fetching data:", error);
            responseText.innerHTML = "<strong style='color: red;'>Error:</strong> Server issue. Please try again later.";
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerText = "Generate Response";
        }
    });
});

document.getElementById("download").addEventListener("click", async function () {
    let responseText = document.getElementById("response").innerText;

    if (!responseText) {
        alert("No response available to download!");
        return;
    }

    let response = await fetch("/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ response: responseText })
    });

    let blob = await response.blob();
    let url = window.URL.createObjectURL(blob);
    let a = document.createElement("a");
    a.href = url;
    a.download = "QuineLaw_Response.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
});
