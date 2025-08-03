document.getElementById("learning-btn").addEventListener("click", getLearningResources);
document.getElementById("learning-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getLearningResources();
  }
});
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
async function getLearningResources() {
  const input = document.getElementById("learning-input").value;
  const outputBox = document.getElementById("learning-output");
  const loading = document.getElementById("learning-loading");
  outputBox.innerText = "";
  loading.style.display = "block";
  try {
    const response = await fetch("http://localhost:5000/learning-resources", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: input })
    });
    if (!response.ok) throw new Error("Backend error");
    const data = await response.json();
    outputBox.innerText = data.resources || "No resources found.";
  } catch (error) {
    outputBox.innerText = "⚠️ Error: " + error.message;
  }
  loading.style.display = "none";
}
document.getElementById("learning-btn").addEventListener("click", getLearningResources);
document.getElementById("learning-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getLearningResources();
  }
});
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
document.getElementById("learning-btn").addEventListener("click", getLearningResources);
document.getElementById("learning-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getLearningResources();
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});
// Initial call to populate resources on page load
getLearningResources();
document.addEventListener("DOMContentLoaded", function() {
  getLearningResources();
});
document.getElementById("learning-input").addEventListener("input", function() {
  const input = this.value.trim();
  if (input) {
    getLearningResources();
  } else {
    document.getElementById("learning-output").innerText = "Please enter a learning goal.";
  }
});         