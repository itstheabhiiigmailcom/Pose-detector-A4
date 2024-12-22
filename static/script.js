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

      // Send the selected exercise to the backend
      try {
        videoFeed.src = `/video_feed?exercise=${selectedExercise}`;
        videoFeed.style.display = "block";
      } catch (error) {
        console.error("Error starting detection:", error);
      }
    }
  });

  // Stop detection
  document.getElementById("stopDetection").addEventListener("click", async () => {
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
});
