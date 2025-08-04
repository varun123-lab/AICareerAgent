console.log('Main JS loaded');

// Learning page initialization without authentication
document.addEventListener('DOMContentLoaded', async () => {
  console.log('Learning page loaded - Ready to use!');
  
  // Initialize learning resources after page load
  getLearningResources();
});

document.getElementById("learning-btn").addEventListener("click", getLearningResources);
document.getElementById("learning-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getLearningResources();
  }
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
    const response = await fetch("http://127.0.0.1:5002/learning-resources", {
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