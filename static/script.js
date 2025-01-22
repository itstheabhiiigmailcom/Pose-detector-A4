document.addEventListener("DOMContentLoaded", function () {
  const dropdownButton = document.getElementById("dropdownButton");
  const dropdownMenu = document.getElementById("dropdownMenu");
  const videoFeed = document.getElementById("videoFeed");

  // Toggle dropdown menu visibility
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("hidden");
  });

  // Handle exercise selection
  dropdownMenu.addEventListener("click", async (event) => {
    if (event.target.classList.contains("dropdown-item")) {
      const selectedExercise = event.target.getAttribute("data-exercise");

      // Hide dropdown menu
      dropdownMenu.classList.add("hidden");
      // change the text of button as well
      dropdownButton.textContent = `${selectedExercise.charAt(0).toUpperCase() + selectedExercise.slice(1)} Exercise`;
      // Send the selected exercise to the backend
      try {
        videoFeed.src = `/video_feed?exercise=${selectedExercise}`;
        videoFeed.style.display = "block";
        const response = await fetch(`/exercise_count?exercise=${selectedExercise}`);
      } catch (error) {
        console.error("Error starting detection:", error);
      }
    }
  });

  setInterval(async () => {
    const response = await fetch("/exercise_count?exercise=all");
    const data = await response.json();
    document.getElementById("exerciseCounts").innerHTML = `
        Push-ups: ${data.pushup} <br>
        Sit-ups: ${data.situp} <br>
        Squats: ${data.squat} <br>
        Cardio: ${data.cardio}
    `;
  }, 1000);

  setInterval(async () => {
    const response = await fetch("/total_energy");
    const data = await response.json();
    document.getElementById('calorieburned').innerHTML = `Energy Spent : ${data.total_energy_spent}`;
  }, 1000)

  // Stop detection
  document
    .getElementById("stopDetection")
    .addEventListener("click", async () => {
      try {
        const response = await fetch("/stop_detection");
        if (response.ok) {
          videoFeed.style.display = "none";
          videoFeed.src = "";
        } else {
          console.error("Error stopping detection:", response.statusText);
        }
      } catch (error) {
        console.error("Error stopping detection in catch :", error);
      }
    });

  // Reset everything to 0 and stop detection
  document
    .getElementById("resetButton")
    .addEventListener("click", async () => {
      try {
        // Call the stop detection endpoint
        const response = await fetch("/reset")
        if (response.ok) {
          // Stop video feed
          videoFeed.style.display = "none";
          videoFeed.src = "";

          // Reset exercise counts and energy data
          document.getElementById("exerciseCounts").innerHTML = `
            Push-ups: 0 <br>
            Sit-ups: 0 <br>
            Squats: 0   <br>
            Cardio: 0
          `;
          document.getElementById('calorieburned').innerHTML = `Energy Spent : 0`;

          // Optionally, reset any other states as needed
          console.log("Everything has been reset.");
        } else {
          console.error("Error stopping detection:", response.statusText);
        }
      } catch (error) {
        console.error("Error resetting everything:", error);
      }
    });
});
