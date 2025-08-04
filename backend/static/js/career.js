// Career agent logic placeholder

// Page initialization without authentication
document.addEventListener('DOMContentLoaded', async () => {
  console.log('Career page loaded - Ready to use!');
});

// Function to beautify career advice response
function beautifyCareerAdvice(advice) {
  // Split text into paragraphs
  let formattedAdvice = advice.replace(/\n\n/g, '</p><p>');
  formattedAdvice = '<p>' + formattedAdvice + '</p>';
  
  // Style headers (lines that end with :)
  formattedAdvice = formattedAdvice.replace(/^([^:]+:)$/gm, '<h4 class="advice-header">$1</h4>');
  
  // Style numbered lists
  formattedAdvice = formattedAdvice.replace(/^\d+\.\s+(.+)$/gm, '<div class="advice-item"><span class="advice-number">$&</span></div>');
  
  // Style bullet points
  formattedAdvice = formattedAdvice.replace(/^[-•]\s+(.+)$/gm, '<div class="advice-bullet">• $1</div>');
  
  // Style bold text (words in **text**)
  formattedAdvice = formattedAdvice.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  
  // Clean up empty paragraphs
  formattedAdvice = formattedAdvice.replace(/<p><\/p>/g, '');
  
  return `
    <div class="advice-container">
      <div class="advice-content">
        ${formattedAdvice}
      </div>
    </div>
    <style>
      .advice-container {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        border-left: 6px solid #4CAF50;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        min-height: 200px;
        max-width: 100%;
        position: relative;
      }
      .advice-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #4CAF50, transparent);
        border-radius: 12px 12px 0 0;
      }
      .advice-content {
        font-size: 16px;
        line-height: 1.8;
      }
      .advice-content p {
        margin-bottom: 20px;
        line-height: 1.8;
        color: #f0f0f0;
        font-size: 16px;
      }
      .advice-header {
        color: #4CAF50;
        margin: 25px 0 15px 0;
        font-size: 1.3em;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
        border-bottom: 2px solid rgba(76, 175, 80, 0.3);
        padding-bottom: 8px;
      }
      .advice-item {
        margin: 15px 0;
        padding: 15px 20px;
        background: rgba(76, 175, 80, 0.15);
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      }
      .advice-item:hover {
        background: rgba(76, 175, 80, 0.2);
        transform: translateX(5px);
      }
      .advice-bullet {
        margin: 12px 0;
        padding: 12px 20px;
        color: #e8e8e8;
        font-size: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 6px;
        border-left: 3px solid #4CAF50;
        transition: all 0.3s ease;
      }
      .advice-bullet:hover {
        background: rgba(255, 255, 255, 0.1);
        padding-left: 25px;
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
        color: #66BB6A;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(102, 187, 106, 0.3);
      }
    </style>
  `;
}

// Function to beautify resume advice response
function beautifyResumeAdvice(advice) {
  // Split text into paragraphs
  let formattedAdvice = advice.replace(/\n\n/g, '</p><p>');
  formattedAdvice = '<p>' + formattedAdvice + '</p>';
  
  // Style bullet points for resume bullets
  formattedAdvice = formattedAdvice.replace(/^[-•]\s+(.+)$/gm, '<div class="resume-bullet">• $1</div>');
  
  // Style numbered lists
  formattedAdvice = formattedAdvice.replace(/^\d+\.\s+(.+)$/gm, '<div class="resume-item"><span class="resume-number">$&</span></div>');
  
  // Style bold text
  formattedAdvice = formattedAdvice.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  
  // Clean up empty paragraphs
  formattedAdvice = formattedAdvice.replace(/<p><\/p>/g, '');
  
  return `
    <div class="resume-container">
      <div class="resume-content">
        ${formattedAdvice}
      </div>
    </div>
    <style>
      .resume-container {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        border-left: 6px solid #2196F3;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        min-height: 200px;
        max-width: 100%;
        position: relative;
      }
      .resume-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #2196F3, transparent);
        border-radius: 12px 12px 0 0;
      }
      .resume-content {
        font-size: 16px;
        line-height: 1.8;
      }
      .resume-content p {
        margin-bottom: 20px;
        line-height: 1.8;
        color: #f0f0f0;
        font-size: 16px;
      }
      .resume-item {
        margin: 15px 0;
        padding: 15px 20px;
        background: rgba(33, 150, 243, 0.15);
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      }
      .resume-item:hover {
        background: rgba(33, 150, 243, 0.2);
        transform: translateX(5px);
      }
      .resume-bullet {
        margin: 15px 0;
        padding: 18px 25px;
        background: rgba(33, 150, 243, 0.12);
        border-radius: 8px;
        color: #e8e8e8;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        border-left: 4px solid #2196F3;
        font-size: 15px;
        line-height: 1.6;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
      }
      .resume-bullet:hover {
        background: rgba(33, 150, 243, 0.18);
        transform: translateX(8px);
        box-shadow: 0 5px 15px rgba(33, 150, 243, 0.2);
      }
      .resume-bullet::before {
        content: '📝';
        margin-right: 10px;
        font-size: 16px;
      }
      strong {
        color: #64B5F6;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(100, 181, 246, 0.3);
      }
    </style>
  `;
}

async function getCareerSuggestions() {
  const input = document.getElementById("career-input").value;
  const outputBox = document.getElementById("career-output");
  const loading = document.getElementById("career-loading");
  outputBox.innerText = "";
  loading.style.display = "block";
  console.log("[DEBUG] Button clicked. Input:", input);
  try {
    console.log("[DEBUG] Sending POST to /career-advice...");
    const response = await fetch("http://127.0.0.1:5002/career-advice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: input })
    });
    console.log("[DEBUG] Response status:", response.status);
    if (!response.ok) {
      throw new Error("Failed to fetch response from server. Status: " + response.status);
    }
    const data = await response.json();
    console.log("[DEBUG] Response data:", data);
    
    // Beautify the response
    const advice = data.advice || "No career suggestions found.";
    outputBox.innerHTML = beautifyCareerAdvice(advice);
  } catch (error) {
    console.error("[DEBUG] Error in getCareerSuggestions:", error);
    outputBox.innerHTML = "<div class='error-message'>⚠️ Error: " + error.message + "</div>";
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
    const response = await fetch("http://127.0.0.1:5000/resume-suggestions", {
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
    outputBox.innerHTML = beautifyResumeAdvice(data.suggestions || "No resume suggestions found.");
  } catch (error) {
    outputBox.innerHTML = "<div class='error-message'>⚠️ Error: " + error.message + "</div>";
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
