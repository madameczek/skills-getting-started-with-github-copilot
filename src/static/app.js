// Function to delete participant (global scope)
async function deleteParticipant(activity, email) {
  try {
    const response = await fetch(
      `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
      { method: "DELETE" }
    );

    if (response.ok) {
      fetchActivities(); // Refresh list after deletion
    } else {
      alert("Failed to remove participant");
    }
  } catch (error) {
    console.error("Error deleting participant:", error);
    alert("Failed to remove participant");
  }
}

// Function to fetch activities (global scope)
async function fetchActivities() {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");

  try {
    const response = await fetch("/activities");
    const activities = await response.json();

    // Clear loading message
    activitiesList.innerHTML = "";
    
    // Clear dropdown options except first
    const options = activitySelect.querySelectorAll("option");
    options.forEach((opt, idx) => {
      if (idx > 0) opt.remove();
    });

    // Populate activities list
    Object.entries(activities).forEach(([name, details]) => {
      const activityCard = document.createElement("div");
      activityCard.className = "activity-card";

      const spotsLeft = details.max_participants - details.participants.length;

      let participantsList = details.participants.length > 0 
        ? `<div style="margin-top: 10px;">${details.participants.map(email => `
              <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; border-radius: 3px;">
                <span>${email}</span>
                <button type="button" onclick="deleteParticipant('${name}', '${email}')" style="background-color: #c62828; padding: 4px 8px; font-size: 12px; cursor: pointer;">
                  ✕
                </button>
              </div>
            `).join('')}</div>`
        : '<p style="margin-top: 10px; font-style: italic; color: #666;">No participants yet</p>';

      activityCard.innerHTML = `
        <h4>${name}</h4>
        <p>${details.description}</p>
        <p><strong>Schedule:</strong> ${details.schedule}</p>
        <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        <div style="margin-top: 15px; background-color: #e3f2fd; padding: 15px; border-radius: 5px; border: 1px solid #ddd;" class="participants-section">
          <strong>Participants:</strong>
          ${participantsList}
        </div>
      `;

      activitiesList.appendChild(activityCard);

      // Add option to select dropdown
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      activitySelect.appendChild(option);
    });
  } catch (error) {
    activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
    console.error("Error fetching activities:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
