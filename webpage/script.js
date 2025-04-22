document.addEventListener('DOMContentLoaded', function () {
    const videoFeed = document.getElementById('video-feed');
    const startCameraBtn = document.getElementById('start-camera');
    const stopCameraBtn = document.getElementById('stop-camera');
    const startDetectionBtn = document.getElementById('start-detection');
    const stopDetectionBtn = document.getElementById('stop-detection');
    const languageSelect = document.getElementById('language-select');
    const audioPlayer = document.getElementById('audioPlayer');
    const savedLettersDiv = document.getElementById('savedLetters');

    let selectedLanguage = 'en'; // Default language

    // Handle language selection
    languageSelect.addEventListener('change', function () {
        selectedLanguage = languageSelect.value;
        console.log('Selected language:', selectedLanguage);
        fetchAudio(selectedLanguage); // Fetch and play audio for the selected language
    });

    // Start camera
    startCameraBtn.addEventListener('click', function () {
        fetch('http://127.0.0.1:8000/start-camera', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Camera started:', data);
                videoFeed.src = 'http://127.0.0.1:8000/video_feed';
                videoFeed.style.display = 'block';
                startCameraBtn.disabled = true;
                stopCameraBtn.disabled = false;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Stop camera
    stopCameraBtn.addEventListener('click', function () {
        fetch('http://127.0.0.1:8000/stop-camera', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Camera stopped:', data);
                videoFeed.src = '';
                videoFeed.style.display = 'none';
                startCameraBtn.disabled = false;
                stopCameraBtn.disabled = true;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Start detection
    startDetectionBtn.addEventListener('click', function () {
        fetch('http://127.0.0.1:8000/start-detection', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Detection started:', data);
                startDetectionBtn.disabled = true;
                stopDetectionBtn.disabled = false;
                updateSavedLetters(); // Update saved letters when detection starts
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Stop detection
    stopDetectionBtn.addEventListener('click', function () {
        fetch('http://127.0.0.1:8000/stop-detection', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Detection stopped:', data);
                startDetectionBtn.disabled = false;
                stopDetectionBtn.disabled = true;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Save text
    document.getElementById('save-text').addEventListener('click', function () {
        fetch('http://127.0.0.1:8000/save-text', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Text saved:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Convert text to audio
    document.getElementById('convert-to-audio').addEventListener('click', function () {
        fetch('http://127.0.0.1:8000/convert-to-audio', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Text converted to audio:', data);
                if (data.audio_files) {
                    console.log('Audio files generated:', data.audio_files);
                    fetchAudio(selectedLanguage); // Fetch and play audio for the selected language
                } else {
                    console.warn('No audio files returned in the response.');
                }
            })
            .catch((error) => {
                console.error('Error occurred while converting text to audio:', error);
            });
    });

    // Clear text
    document.getElementById('clear-text').addEventListener('click', function () {
        fetch('http://127.0.0.1:8000/clear-text', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Text cleared:', data);
                savedLettersDiv.innerText = ''; // Clear the displayed saved letters
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Fetch and play audio
    function fetchAudio(langCode) {
        const audioUrl = `http://127.0.0.1:8000/get-audio/${langCode}`;
        console.log(`Fetching audio from: ${audioUrl}`); // Debug log

        fetch(audioUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Audio file not found for language: ${langCode}`);
                }
                audioPlayer.src = audioUrl;
                audioPlayer.play();
            })
            .catch(error => {
                console.error('Error fetching or playing audio:', error);
                alert('Audio file not found or failed to play.');
            });
    }

    // Update saved letters
    function updateSavedLetters() {
        fetch('http://127.0.0.1:8000/get-detected-letters', {
            method: 'GET'
        })
            .then(response => response.json())
            .then(data => {
                savedLettersDiv.innerText = data.detected_letters;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    // Initial call to display saved letters on page load
    updateSavedLetters();
});