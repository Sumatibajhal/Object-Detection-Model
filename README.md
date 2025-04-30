Object Detection System with Real-Time Alerts
Overview
This project implements a real-time object detection system using the YOLOv3 algorithm. It allows users to upload images and videos for object detection, visually highlights detected objects, and provides notifications via email or sound alerts for specified objects.

The system features an interactive Graphical User Interface (GUI) built with Tkinter, making it accessible for both technical and non-technical users.

Features
✅ Real-Time Object Detection – Processes images and videos using the YOLOv3 algorithm. 
✅ Graphical User Interface (GUI) – Simple and intuitive interface for easy file uploads. 
✅ Bounding Box Visualization – Labels and confidence scores for detected objects. 
✅ Notifications – Sends email alerts and plays sound when specific objects are detected (e.g., "person" or "car"). 
✅ User Feedback Integration – Allows users to refine detections through feedback and retry detection if necessary. 
✅ Scalability – Modular design for future enhancements like cloud integration and mobile applications.

Installation
Prerequisites
Ensure you have the following installed:

Python 3.x

pip (Python Package Installer)

CUDA-enabled GPU (Optional but recommended for faster detection)

Install Dependencies
Run the following command to install the required libraries:

bash
pip install opencv-python numpy tkinter smtplib winsound
If using a GPU for acceleration, install CUDA dependencies (NVIDIA required).

Usage
1. Clone the Repository
bash
git clone https://github.com/yourusername/object-detection-system.git
cd object-detection-system
2. Run the Object Detection System
bash
python main.py
3. Upload an Image or Video
Click on "Upload File" in the GUI to select an image or video.

The system will detect objects and display results in a new window.

4. Receive Alerts
If specified objects (e.g., "person," "car") are detected, an email notification will be sent.

A sound alert will play when a target object is found.

5. Provide Feedback
A prompt asks users whether the detection was correct.

If unsatisfied, users can retry with adjusted settings.

Project Structure
object-detection-system/
│── Object_detection_model/
│   ├── yolov3.cfg
│   ├── yolov3.weights
│   ├── coco.names
│── main.py
│── requirements.txt
│── README.md
yolov3.cfg – Configuration file for YOLO model.

yolov3.weights – Pre-trained weights for object detection.

coco.names – List of object classes YOLO can detect.

main.py – Main script handling the detection and GUI.

dog.jpg, eagle.jpg, giraffe.jpg - Test Cases

README.md – Documentation for the project.

Future Scope
🌐 Cloud-Based Dashboards – Extend functionality with cloud logging and remote monitoring.

📲 Mobile App Integration – Allow users to upload files and receive alerts via mobile.

🎯 Custom Object Training – Train YOLO for specialized object detection (e.g., medical images, retail products).

📡 IoT Deployment – Optimize for edge devices like Raspberry Pi and Jetson Nano.
![Screenshot 2025-04-24 210203](https://github.com/user-attachments/assets/f150b02b-7204-4396-9c22-56bdde0df470)
![dog](https://github.com/user-attachments/assets/6f49ca4a-5746-40b2-9328-3257cdea009d)
![Screenshot 2025-04-24 210223](https://github.com/user-attachments/assets/8ba304da-436d-48b7-8b01-194fbcc41637)
![Screenshot 2025-04-24 210234](https://github.com/user-attachments/assets/e6840180-e143-4def-9d9f-4462d6243d8c)
![Screenshot 2025-04-24 211929](https://github.com/user-attachments/assets/06c85c04-6e83-4927-ad99-c9fe6e0da050)
![Screenshot 2025-04-24 212013](https://github.com/user-attachments/assets/ef08bbae-ee32-4a37-8606-5c83aff21072)

