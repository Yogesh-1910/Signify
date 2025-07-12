
<div align="center">
  <img src="https://github.com/user-attachments/assets/7597cea9-97dc-4bb3-b53b-59a069046ab8" height="513" alt="Signify logo"/>
</div> 


<h1 align="center">Signify: Sign Language to Text Translation</h1>

<p align="center">
  A vision-based system that translates American Sign Language (ASL) into text and speech in real-time using standard webcams.
</p>

<p align="center">
  <!-- Badges -->
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-green?style=for-the-badge&logo=flask" alt="Flask Framework">
  <img src="https://img.shields.io/badge/Library-OpenCV-red?style=for-the-badge&logo=opencv" alt="OpenCV">
  <img src="https://img.shields.io/badge/ML%20Library-Scikit--learn-orange?style=for-the-badge&logo=scikit-learn" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Project%20Status-Completed-brightgreen?style=for-the-badge" alt="Project Status">
</p>

This project, developed as part of the Bachelor of Engineering in AI & ML, aims to bridge the communication gap for the deaf and mute community by providing an accessible and cost-effective translation tool.

---

### About The Project

There are over 430 million people globally who require assistance for hearing-related disabilities. Signify addresses this challenge by creating a real-time, vision-based American Sign Language (ASL) translator.

Unlike expensive, sensor-based solutions (like specialized gloves), this project leverages the power of machine learning with standard, everyday webcams. This approach makes the technology highly accessible, scalable, and easy to use. The system uses a **Random Forest Classifier** to interpret hand gestures, achieving a balance between performance and computational efficiency, making it suitable for a wide range of devices.

The inclusion of **LIME (Local Interpretable Model-Agnostic Explanations)** also ensures that the model's predictions are transparent and trustworthy.

---

### Core Features

-   **Real-Time Gesture Recognition:** Translates ASL gestures from a live webcam feed.
-   **Sign-to-Text Conversion:** Displays recognized letters and words in a text box.
-   **Text-to-Speech Output:** Converts the translated text into audible speech for enhanced accessibility.
-   **User-Friendly Controls:** Simple buttons to start/stop the camera, begin/end detection, save output, and clear text.
-   **Standard Hardware:** Runs on any computer with a standard webcam, eliminating the need for costly sensors.
-   **Web-Based Interface:** Built with Flask, allowing easy access through a web browser.

---

### Technology Stack

This project was built using the following technologies:

-   **Backend:** Flask
-   **Machine Learning:** Scikit-learn (RandomForestClassifier, GridSearchCV)
-   **Computer Vision:** OpenCV, MediaPipe
-   **Data Processing:** Python, NumPy, Pickle
-   **Frontend:** HTML, CSS, JavaScript

---

### System Architecture

The project workflow is divided into two main phases: **Model Training** and **Real-Time Inference**.

1.  **Data Collection:** A dataset of ASL alphabet images is collected using OpenCV.
2.  **Feature Extraction:** **MediaPipe** is used to detect 21 key landmarks (like fingertips and knuckles) on the hand in each image. These landmark coordinates form the feature vector for our model.
3.  **Model Training:**
    -   The extracted landmark data is standardized to ensure uniform feature vector lengths.
    -   A **Random Forest Classifier** is trained on this dataset.
    -   **GridSearchCV** is used to perform hyperparameter tuning to find the optimal model configuration.
    -   The best-performing model is saved as a `.p` (pickle) file.
4.  **Real-Time Inference (The Web App):**
    -   The Flask server initializes the webcam.
    -   For each frame, MediaPipe detects hand landmarks.
    -   The trained Random Forest model predicts the sign based on the landmarks.
    -   The predicted letter is displayed on the UI, and the user can choose to convert the final text to speech.

---

### Getting Started

To get a local copy up and running, follow these simple steps.

#### Prerequisites

Make sure you have Python (3.8+) and pip installed on your system.

#### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/Yogesh-1910/Signify.git
    cd Signify
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    (First, ensure you have a `requirements.txt` file in your repository)
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```sh
    python app.py
    ```

5.  **Open your browser** and navigate to `http://127.0.0.1:8000` (or the port specified in your Flask app).

---

### For Developers & Contributors

Hello Developers! Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

---

### Future Improvements

While this project provides a robust proof-of-concept, future work could include:

-   **Adopting Deep Learning:** Implementing a CNN or LSTM-based model to potentially increase the accuracy above the current 72.55%.
-   **Expanding the Vocabulary:** Adding support for complete words and phrases, not just individual letters.
-   **Multi-Language Support:** Incorporating datasets for other sign languages (e.g., British or Indian Sign Language).
-   **Improving the UI/UX:** Enhancing the user interface for a more seamless experience.

---

### License

Distributed under the MIT License. See `LICENSE` for more information.

---

### Acknowledgments

-   This project was completed by **Yogesh S** and **Apurva S**.
-   Special thanks to our guide, **Prof. Vani**, for her mentorship and support throughout this project.
