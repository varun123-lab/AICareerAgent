async function getInterviewQuestions() {
  const input = document.getElementById("interview-role").value;
  const outputBox = document.getElementById("interview-output");
  const loading = document.getElementById("interview-loading");
  outputBox.innerText = "";
  loading.style.display = "block";
  try {
    const response = await fetch("http://127.0.0.1:5002/mock-interview", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ role: input })
    });
    if (!response.ok) throw new Error("Backend error");
    const data = await response.json();
    outputBox.innerText = data.questions || "No interview questions returned.";
  } catch (error) {
    outputBox.innerText = "\u26a0\ufe0f Error: " + error.message;
  }
  loading.style.display = "none";
}

document.getElementById("interview-btn").addEventListener("click", getInterviewQuestions);
document.getElementById("interview-role").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getInterviewQuestions();
  }
});
