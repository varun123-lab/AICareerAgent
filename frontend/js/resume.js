async function getResume() {
  const input = document.getElementById("resume-input").value;
  const outputBox = document.getElementById("resume-output");

  outputBox.innerText = "Generating resume bullets...";

  try {
    const response = await fetch("http://localhost:5000/generate-resume", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ experience: input })
    });

    if (!response.ok) throw new Error("Backend error");

    const data = await response.json();
    outputBox.innerText = data.resume || "No resume generated.";
  } catch (error) {
    outputBox.innerText = "⚠️ Error: " + error.message;
  }
}

document.getElementById("resume-btn").addEventListener("click", getResume);
document.getElementById("resume-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getResume();
  }
});