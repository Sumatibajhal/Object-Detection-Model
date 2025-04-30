import cv2  # library for detecting objects in images/videos
import numpy as np  # Handles matrice & numerical operations
import tkinter as tk  # Framework for building our UI
from tkinter import filedialog, messagebox  # Tools for file selection and user feedback
import smtplib  # For sending email notifications
from email.mime.text import MIMEText  # To craft neat email messages
import winsound  # Plays sound for alerts 

# Load YOLO model for object detection
net = cv2.dnn.readNet("Object_detection_model/yolov3.weights", "Object_detection_model/yolov3.cfg") 
with open("Object_detection_model/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]  # List of detectable object names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]  # Layers doing the detection magic

# Function to detect objects in an image or frame
def detect_objects(image):
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, scalefactor=0.00392, size=(416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)  # YOLO processes the image through its neural net

    boxes, confidences, class_ids = [], [], []  # Collecting bounding boxes, confidence scores, and class IDs
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Only take predictions that YOLO is >50% confident about
                center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                w, h = int(detection[2] * width), int(detection[3] * height)
                x, y = center_x - w // 2, center_y - h // 2  # Convert center coordinates to box corners
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)  # Non-Maximum Suppression to remove overlapping boxes
    indexes = indexes.flatten() if len(indexes) > 0 else []
    return boxes, confidences, class_ids, indexes

# to draw bounding boxes and labels on an image
def draw_boxes(image, boxes, confidences, class_ids, indexes):
    detected_objects = []  # Keep track of detected objects for alerts
    if len(indexes) > 0:
        for i in indexes:
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]} {confidences[i]:.2f}"
            detected_objects.append(classes[class_ids[i]])  # Record the detected object's name
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw green box
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Add label above box

    return detected_objects  # Return list of detected objects for notification purposes

# to send email alerts for specific detections
def send_email_alert(detected_objects):
    sender_email = "sender_email@gmail.com"
    sender_password = "password"
    recipient_email = "receiver_email@gmail.com"

    message = f"Alert! The following objects were detected:\n" + "\n".join(detected_objects)
    msg = MIMEText(message)
    msg["Subject"] = "Object Detection Alert"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# to play sound alerts for specific detections
def play_sound_alert():
    winsound.Beep(1000, 500)  

# to process the uploaded image or video
def process_image():
    file_path = filedialog.askopenfilename(title="Select an Image or Video", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("Video files", "*.mp4 *.avi *.mov")])
    if file_path.endswith((".jpg", ".jpeg", ".png")):
        image = cv2.imread(file_path)
        boxes, confidences, class_ids, indexes = detect_objects(image)
        detected_objects = draw_boxes(image, boxes, confidences, class_ids, indexes)
        cv2.imshow("Detected Objects", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Send email or play sound alert if specific objects are detected
        if "person" in detected_objects or "car" in detected_objects:  # Example criteria
            send_email_alert(detected_objects)  # Send email alert
            play_sound_alert()  # Play sound alert

        # Feedback prompt
        feedback = messagebox.askyesno("Feedback", "Are the detections correct?")
        if not feedback:
            messagebox.showinfo("Thank You!", "Retrying detection with improved parameters...")
            retry_detection(image)  # Retry detection
        messagebox.showinfo("Thank You","Thank You, For your Feedback ;)")

    elif file_path.endswith((".mp4", ".avi", ".mov")):
        cap = cv2.VideoCapture(file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            boxes, confidences, class_ids, indexes = detect_objects(frame)
            detected_objects = draw_boxes(frame, boxes, confidences, class_ids, indexes)
            cv2.imshow("Video Detection", frame)
            if "person" in detected_objects or "car" in detected_objects:  # Example criteria
                send_email_alert(detected_objects)  # Send email alert for video detections
                play_sound_alert()  # Play sound alert for video detections
            if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to exit
                break
        cap.release()
        cv2.destroyAllWindows()

# Retry detection logic for improved results
def retry_detection(image):
    boxes, confidences, class_ids, indexes = detect_objects(image)
    draw_boxes(image, boxes, confidences, class_ids, indexes)
    cv2.imshow("Improved Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# UI
def create_ui():
    root = tk.Tk()
    root.title("Welcome to Object Detection System")
    root.geometry("600x400")
    root.configure(bg="#eaf2f8")

    # Title
    title_label = tk.Label(root, text="Object Detection System", font=("Helvetica", 24, "bold"), bg="#eaf2f8", fg="#2e86c1")
    title_label.pack(pady=20)

    # Description
    description_label = tk.Label(root, text="Upload an Image or Video to detect objects and receive alerts.", font=("Arial", 14), bg="#eaf2f8", fg="#5d6d7e")
    description_label.pack(pady=10)

    # Upload button 
    upload_button = tk.Button(root, text="Upload File", command=process_image, font=("Arial", 14), bg="#2874a6", fg="white", activebackground="#1b4f72", activeforeground="white", width=20, height=2)
    upload_button.pack(pady=20)

    # Footer
    footer_label = tk.Label(root, text="Powered by AI and Computer Vision Technologies", font=("Arial", 12), bg="#eaf2f8", fg="#85929e")
    footer_label.pack(side="bottom", pady=10)

    # Start the GUI loop
    root.mainloop()

# Run the program
create_ui()
