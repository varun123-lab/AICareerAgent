// Learning agent logic

// Function to beautify learning resources response
function beautifyLearningResources(resources) {
  // Split text into paragraphs
  let formattedResources = resources.replace(/\n\n/g, '</p><p>');
  formattedResources = '<p>' + formattedResources + '</p>';
  
  // Style headers (lines that end with :)
  formattedResources = formattedResources.replace(/^([^:]+:)$/gm, '<h4 class="learning-header">$1</h4>');
  
  // Style numbered lists
  formattedResources = formattedResources.replace(/^\d+\.\s+(.+)$/gm, '<div class="learning-item"><span class="learning-number">$&</span></div>');
  
  // Style bullet points
  formattedResources = formattedResources.replace(/^[-•]\s+(.+)$/gm, '<div class="learning-bullet">📚 $1</div>');
  
  // Style bold text (words in **text**)
  formattedResources = formattedResources.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  
  // Style course/resource titles (lines that start with uppercase and contain common keywords)
  formattedResources = formattedResources.replace(/^([A-Z][^.!?]*(?:Course|Tutorial|Guide|Book|Resource|Platform|Certification)[^.!?]*)$/gm, '<div class="resource-title">🎓 $1</div>');
  
  // Clean up empty paragraphs
  formattedResources = formattedResources.replace(/<p><\/p>/g, '');
  
  return `
    <div class="learning-container">
      <div class="learning-content">
        ${formattedResources}
      </div>
    </div>
    <style>
      .learning-container {
        background: linear-gradient(135deg, rgba(156, 39, 176, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        border-left: 6px solid #9C27B0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        min-height: 200px;
        max-width: 100%;
        position: relative;
      }
      .learning-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #9C27B0, transparent);
        border-radius: 12px 12px 0 0;
      }
      .learning-content {
        font-size: 16px;
        line-height: 1.8;
      }
      .learning-content p {
        margin-bottom: 20px;
        line-height: 1.8;
        color: #f0f0f0;
        font-size: 16px;
      }
      .learning-header {
        color: #9C27B0;
        margin: 25px 0 15px 0;
        font-size: 1.3em;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(156, 39, 176, 0.3);
        border-bottom: 2px solid rgba(156, 39, 176, 0.3);
        padding-bottom: 8px;
      }
      .learning-item {
        margin: 15px 0;
        padding: 15px 20px;
        background: rgba(156, 39, 176, 0.15);
        border-radius: 8px;
        border-left: 4px solid #9C27B0;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      }
      .learning-item:hover {
        background: rgba(156, 39, 176, 0.2);
        transform: translateX(5px);
      }
      .learning-bullet {
        margin: 12px 0;
        padding: 15px 20px;
        color: #e8e8e8;
        font-size: 15px;
        background: rgba(156, 39, 176, 0.08);
        border-radius: 6px;
        border-left: 3px solid #9C27B0;
        transition: all 0.3s ease;
        line-height: 1.6;
      }
      .learning-bullet:hover {
        background: rgba(156, 39, 176, 0.15);
        padding-left: 25px;
      }
      .resource-title {
        margin: 18px 0;
        padding: 15px 20px;
        background: rgba(156, 39, 176, 0.2);
        border-radius: 8px;
        color: #BA68C8;
        font-size: 16px;
        font-weight: 600;
        border-left: 4px solid #9C27B0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      }
      .resource-title:hover {
        background: rgba(156, 39, 176, 0.25);
        transform: translateX(8px);
      }
      .error-message {
        color: #ff6b6b;
        background: rgba(255, 107, 107, 0.15);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ff6b6b;
        font-size: 16px;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.2);
      }
      strong {
        color: #BA68C8;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(186, 104, 200, 0.3);
      }
    </style>
  `;
}

async function getLearningResources() {
  const input = document.getElementById("learning-input").value;
  const outputBox = document.getElementById("learning-output");
  const loading = document.getElementById("learning-loading");
  
  if (!input.trim()) {
    outputBox.innerHTML = "<div class='error-message'>⚠️ Please enter a learning goal or topic.</div>";
    return;
  }
  
  outputBox.innerHTML = "";
  loading.style.display = "block";
  
  console.log("[DEBUG] Button clicked. Input:", input);
  
  try {
    console.log("[DEBUG] Sending POST to /learning-resources...");
    const response = await fetch("http://127.0.0.1:5000/learning-resources", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ topic: input })
    });
    
    console.log("[DEBUG] Response status:", response.status);
    
    if (!response.ok) {
      throw new Error("Failed to fetch response from server. Status: " + response.status);
    }
    
    const data = await response.json();
    console.log("[DEBUG] Response data:", data);
    
    // Beautify the response
    const resources = data.resources || "No learning resources found.";
    outputBox.innerHTML = beautifyLearningResources(resources);
  } catch (error) {
    console.error("[DEBUG] Error in getLearningResources:", error);
    outputBox.innerHTML = "<div class='error-message'>⚠️ Error: " + error.message + "</div>";
  }
  
  loading.style.display = "none";
}

// Event listeners
document.getElementById("learning-btn").addEventListener("click", getLearningResources);
document.getElementById("learning-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    getLearningResources();
  }
});