# 🗑️ Autonomous Waste Sorting System — Edge AI Deployment

> Real-time waste classification using computer vision and on-device ML inference on Raspberry Pi hardware.

---

## Overview

An edge AI–based autonomous waste sorting system that performs real-time waste classification using computer vision and on-device machine learning inference on Raspberry Pi hardware.

The system integrates:
- Image acquisition
- ML-based waste classification
- Real-time inference pipelines
- Actuator control logic
- Monitoring interfaces

to enable fully automated waste segregation with minimal human intervention.

Designed for resource-constrained environments, the project focuses on **low-latency embedded AI inference** and **hardware-software integration** for intelligent waste management applications.

---

## System Workflow

```
Camera Input → Preprocessing → ML Inference → Control Logic → Actuator
                                                     ↓
                                            Dashboard / Logging
```

1. **Camera module** captures incoming waste object images
2. **Image preprocessing pipeline** prepares frames for inference
3. **On-device ML model** performs real-time waste classification
4. **Control logic** triggers sorting actuator based on predicted category
5. **Dashboard / logging services** display system activity and classification statistics

---

## Features

| Feature | Description |
|---|---|
| 🔍 Real-time Classification | Computer vision–based waste detection and classification |
| ⚡ Edge AI Inference | On-device ML inference on Raspberry Pi — no cloud dependency |
| 🕐 Low Latency | End-to-end inference latency of **1.5–2 seconds** per object |
| 🤖 Automated Sorting | Actuator-based sorting logic driven by model predictions |
| 🧩 Modular Pipeline | Decoupled inference, control, and monitoring components |
| 📊 Real-time Monitoring | Live dashboard with classification logs and statistics |
| 🔧 Extensible Categories | Easily add new waste categories without redesigning the pipeline |
| 🔌 Hardware Integration | Seamless hardware-software co-design for embedded AI systems |

---

## Tech Stack

- **Hardware** — Raspberry Pi, Camera Module, Sorting Actuator
- **ML / CV** — TensorFlow Lite, OpenCV
- **Inference** — On-device model serving, optimized for CPU-constrained hardware
- **Control Logic** — Python-based actuator coordination
- **Monitoring** — Real-time logging and classification dashboard

---

## Project Structure

```
waste-sorting-system/
├── inference/          # ML model and on-device inference pipeline
├── preprocessing/      # Image acquisition and frame preparation
├── control/            # Actuator control logic
├── monitoring/         # Dashboard and logging services
├── models/             # Trained model weights
└── README.md
```

---

## Results

- 🕐 **1.5–2 second** end-to-end latency per object on Raspberry Pi
- ✅ Fully local inference — zero cloud dependency
- 🔌 Seamless hardware-software integration with physical actuator control
