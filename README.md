# Face Recognition Authentication Project

## Overview
This project is a face recognition-based authentication system, developed in Python, and built using the Tkinter library for GUI and DeepFace for facial recognition. The project was built with the assistance of Amazon Q, which significantly accelerated the development process, allowing the entire application to be completed in just 44 minutes. As a recognition of this achievement, I was awarded an Amazon Q coin.

The application allows users to register by capturing their facial images and stores these images for future recognition. The system then uses face recognition technology to authenticate registered users before granting them access to a secure terminal.

## Features
- **User Registration**: Capture a new user's facial data and store it for future use.
- **Face Authentication**: Authenticate a user's face to provide secure access to a confidential area.
- **Graphical User Interface (GUI)**: Built using Tkinter for easy navigation.
- **Real-Time Camera Feed**: Utilizes OpenCV to capture the camera feed in real-time.
- **Secure Access Control**: Only authenticated users can access the classified terminal.
- **Amazon Q Integration**: Assisted in developing the application quickly, acting as a code suggestion and completion tool similar to GitHub Copilot.

## Requirements
- Python 3.8 or higher
- **DeepFace**: Used for facial recognition
- **OpenCV**: For accessing the camera and capturing frames
- **Pillow (PIL)**: For image processing
- **Tkinter**: For GUI elements

### Python Libraries
Install the required Python libraries using the following command:

```sh
pip install deepface opencv-python Pillow
```

## Project Structure
- **`main.py`**: Contains the main code for the face recognition authentication system.
- **`registered_faces/`**: Directory to store the facial images of registered users.

## How to Run the Project
1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the Dependencies**
   Install the required Python libraries as mentioned in the requirements.

3. **Run the Application**
   Start the application by running the main script.
   ```sh
   python main.py
   ```

## Using the Application
1. **Login Screen**: Upon launching, you will see the login screen with two options:
   - **Initiate Facial Scan**: If you are an existing user, click this button to authenticate your face.
   - **Register New User**: If you are a new user, click this button to register.

2. **User Registration**:
   - Enter your name in the text box.
   - Click the "Capture and Register" button to register your face.

3. **Authentication**:
   - Click "Initiate Facial Scan" to start facial authentication.
   - The system will scan your face and provide access if your face matches one in the database.

4. **Secure Area**:
   - If authenticated, you will gain access to a secure area that simulates a classified terminal.

## Application Workflow
1. **Login Page**: Users can choose to either register a new account or authenticate themselves.
2. **Registration Page**: Users provide their name, and their facial image is captured and stored.
3. **Authentication Page**: Users initiate facial recognition to gain access to the secure terminal.
4. **Secure Terminal Page**: If authentication is successful, users can view the secure information.

## Amazon Q Integration
Amazon Q, similar to GitHub Copilot, was used in this project to assist in code generation, offering suggestions and code completions that greatly accelerated the development process. The use of Amazon Q made it possible to complete the project in just 44 minutes. As a result of this achievement, an Amazon Q coin was awarded.

## Challenges and Solutions
- **Real-time Camera Feed**: Implemented threading to ensure smooth camera performance without blocking the main application.
- **Facial Recognition Accuracy**: DeepFace was utilized to improve facial recognition accuracy and handle different conditions like lighting and angles.
- **Full-Screen Mode for GUI**: Set the application to run in full-screen mode for an immersive experience, with the option to exit full-screen using the `Esc` key.

## Future Enhancements
- **Two-Factor Authentication (2FA)**: Adding an extra layer of security, such as OTP verification.
- **Face Spoofing Detection**: Integrating methods to detect and prevent the use of photos or videos for authentication.
- **Cloud Integration**: Save registered faces securely in the cloud to enable cross-device authentication.

## Acknowledgments
- **DeepFace**: For providing the facial recognition functionality.
- **Amazon Q**: For accelerating the development process through AI-powered code assistance.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any questions or feedback, please reach out to **Alvin Kamau** via LinkedIn or email.

