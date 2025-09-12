import RPi.GPIO as GPIO
import time
import torch
import cv2
from torchvision import transforms, models
from PIL import Image
from picamera2 import Picamera2
import os
from datetime import datetime
from threading import Thread
from flask import Flask, jsonify, render_template_string

# -----------------------
# Shared state for dashboard
# -----------------------
latest_status = {
    "status": None,
    "confidence": 0.0,
    "timestamp": None,
    "total_count": 0,
    "bio_count": 0,
    "nonbio_count": 0
}

# -----------------------
# Flask Setup
# -----------------------
app = Flask(__name__)

@app.route("/")
def dashboard():
    # Simple HTML dashboard (can later move to templates/)
    return render_template_string("""
        <h1>Autonomous Waste Bin Dashboard</h1>
        <p><b>Last Status:</b> {{ status["status"] }}</p>
        <p><b>Confidence:</b> {{ "%.2f"|format(status["confidence"]*100) }}%</p>
        <p><b>Timestamp:</b> {{ status["timestamp"] }}</p>
        <p><b>Total Count:</b> {{ status["total_count"] }}</p>
        <p><b>Bio Count:</b> {{ status["bio_count"] }}</p>
        <p><b>Non-Bio Count:</b> {{ status["nonbio_count"] }}</p>
        <meta http-equiv="refresh" content="3">
    """, status=latest_status)

@app.route("/status")
def get_status():
    return jsonify(latest_status)

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# -----------------------
# GPIO Setup
# -----------------------
GPIO.setmode(GPIO.BCM)

TRIG = 14
ECHO = 18
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

SERVO_PIN = 23
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

# -----------------------
# Camera + Model Setup
# -----------------------
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (224, 224)}))
picam2.start()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

model = models.resnet18()
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load(
    '/home/Pranav_Srikarthik/Downloads/resnet18_model.pth',
    map_location=torch.device('cpu')
))
model.eval()

# -----------------------
# Helper Functions
# -----------------------
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
    
    elapsed_time = stop_time - start_time
    return (elapsed_time * 34300) / 2

def actuate_servo(direction):
    print("Actuating servo...")
    if direction == 1:
        print("Non-biodegradable")
        servo.ChangeDutyCycle(3.5)
    elif direction == 0:
        print("Biodegradable waste")
        servo.ChangeDutyCycle(6.5)
    time.sleep(1)
    servo.ChangeDutyCycle(5)
    time.sleep(1)
    servo.ChangeDutyCycle(0)

# -----------------------
# Main Loop
# -----------------------
def main_loop():
    try:
        while True:
            distance = measure_distance()
            print(f"Distance: {distance:.2f} cm")

            if distance < 11:
                print("Object detected! Analyzing image...")
                image_path = '/home/Pranav_Srikarthik/captured_image.jpg'
                picam2.capture_file(image_path, format="jpeg")

                pil_image = Image.open(image_path)
                pil_image.save('/home/Pranav_Srikarthik/temp_preprocessed_image_corrected.jpg')

                input_tensor = transform(pil_image).unsqueeze(0)

                with torch.no_grad():
                    output = model(input_tensor)
                    probabilities = torch.nn.functional.softmax(output, dim=1)
                    confidence, predicted = torch.max(probabilities, 1)

                    predicted_class = predicted.item()
                    confidence_score = probabilities[0][predicted_class].item()

                    # Update shared state for dashboard
                    latest_status["status"] = "Bio" if predicted_class == 0 else "Non-Bio"
                    latest_status["confidence"] = confidence_score
                    latest_status["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    latest_status["total_count"] += 1
                    if predicted_class == 0:
                        latest_status["bio_count"] += 1
                    else:
                        latest_status["nonbio_count"] += 1

                    print(f'Predicted class: {predicted_class} | Confidence: {confidence_score:.2f}')
                    actuate_servo(predicted_class)

            time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        GPIO.cleanup()
        picam2.stop()
        servo.stop()

# -----------------------
# Start Flask in Background + Run Loop
# -----------------------
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    main_loop()
