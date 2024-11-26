document.addEventListener('DOMContentLoaded', function() {
    const startDetectionBtn = document.getElementById('startDetection');
    const stopDetectionBtn = document.getElementById('stopDetection');

    // Check if the buttons are found to avoid null reference
    if (startDetectionBtn && stopDetectionBtn) {
        // Add event listener for the Start Detection button
        startDetectionBtn.addEventListener('click', function() {
            fetch('/start_detection') // Start detection
                .then(response => {
                    if (response.ok) {
                        document.getElementById("videoFeed").src = "/video_feed"; // Start the video feed
                        document.getElementById("videoFeed").style.display = "block"; // Show the video feed
                    } else {
                        console.error("Failed to start detection.");
                    }
                })
                .catch(error => console.error("Error:", error));
        });

        // Add event listener for the Stop Detection button
        stopDetectionBtn.addEventListener('click', function() {
            fetch('/stop_detection') // Stop detection
                .then(response => {
                    if (response.ok) {
                        const videoFeed = document.getElementById("videoFeed");
                        videoFeed.src = ""; // Stop the video feed by clearing the src
                        videoFeed.style.display = "none"; // Hide the video feed
                    } else {
                        console.error("Failed to stop detection.");
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    } else {
        console.error("Buttons not found!");
    }
});
