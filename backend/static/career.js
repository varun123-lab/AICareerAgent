// Career agent logic placeholder
async function getCareerSuggestions() {
  const input = document.getElementById("career-input").value;
  const outputBox = document.getElementById("career-output");
  const loading = document.getElementById("career-loading");
  outputBox.innerText = "";
  loading.style.display = "block";
  try {
    const response = await fetch("http://localhost:5000/career-advice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: input })
    });
    if (!response.ok) {
      throw new Error("Failed to fetch response from server.");
    }
    const data = await response.json();
    outputBox.innerText = data.advice || "No career suggestions found.";
  } catch (error) {
    outputBox.innerText = "⚠️ Error: " + error.message;
  }
  loading.style.display = "none";
}
document.getElementById("career-btn").addEventListener("click", getCareerSuggestions);
document.getElementById("career-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getCareerSuggestions();
  }
});
// Resume agent logic placeholder
async function getResume() {
  const input = document.getElementById("resume-input").value;
  const outputBox = document.getElementById("resume-output");
  const loading = document.getElementById("resume-loading");
  outputBox.innerText = "";
  loading.style.display = "block";
  try {
    const response = await fetch("http://localhost:5000/resume-suggestions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ resumeText: input })
    });
    if (!response.ok) {
      throw new Error("Failed to fetch response from server.");
    }
    const data = await response.json();
    outputBox.innerText = data.suggestions || "No resume suggestions found.";
  } catch (error) {
    outputBox.innerText = "⚠️ Error: " + error.message;
  }
  loading.style.display = "none";
}
document.getElementById("resume-btn").addEventListener("click", getResume);
document.getElementById("resume-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getResume();
  }
});

// Interview agent logic placeholder
async function getCareerAdvice() {
  const input = document.getElementById("career-input").value;
  const outputBox = document.getElementById("career-output");
  outputBox.innerText = "Loading...";
  try {
    const response = await fetch("http://localhost:5000/career-advice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input })
    });
    if (!response.ok) throw new Error("Backend error");
    const data = await response.json();
    outputBox.innerText = data.advice || "No advice found.";
  } catch (error) {
    outputBox.innerText = "\u26a0\ufe0f Error: " + error.message;
  }
}
document.getElementById("career-btn").addEventListener("click", getCareerAdvice);
document.getElementById("career-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getCareerAdvice();
  }
});