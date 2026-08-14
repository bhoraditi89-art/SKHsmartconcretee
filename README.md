# 🧱 Smart Concrete: Self-Healing with Embedded Neural Networks

## 🚀 Overview
Conventional concrete lacks real-time monitoring and suffers from thermal stress and early-age cracking. This project is a working 1x1x1 physical prototype of a "Smart Concrete" system that acts like a living body. It combines biological self-healing properties (using *Bacillus subtilis* bacteria) with an embedded fiber-optic "nervous system" and an ESP32 microcontroller to predict, detect, and autonomously heal structural fractures.

## ✨ Key Features
*   **The Nervous System:** Embedded fiber-optic sensors continuously monitor internal strain, stress, and temperature.
*   **AI Detection:** An embedded Neural Network processes sensor data via an ESP32 to predict and pinpoint microscopic fractures in real-time.
*   **Biological Healing:** Micro-encapsulated *Bacillus subtilis* bacteria rupture upon crack formation, consuming nutrients and actively sequestering CO2 to precipitate limestone (CaCO3) and seal the crack.
*   **Live Dashboard:** Real-time structural health monitoring and "Damage Detected / Healed" alerts pushed via MQTT.

## 🛠️ Technology Stack
**Hardware:**
*   ESP32 Microcontroller
*   Embedded Fiber Optic Sensors & Optical Interrogator
*   1x1x1 Concrete Replica (Standard Cement + Aggregates)
*   Micro-encapsulated *Bacillus subtilis* + Calcium Nutrient Broth

**Software:**
*   C++ / MicroPython (ESP32 Firmware)
*   TensorFlow Lite (Embedded Neural Network)
*   MQTT Protocol & Custom Cloud Dashboard

## 📂 Repository Structure
*   `/firmware` - Source code for the ESP32 microcontroller.
*   `/ml_model` - Neural network training and deployment scripts.
*   `/dashboard` - Code for the real-time structural health dashboard.
*   `/hardware` - Circuit diagrams and physical mold dimensions.
*   `/docs` - Pitch presentations and reference research papers.

## 🏆 Hackathon Details
Developed for **DIPEX 2026**
*   **Theme:** Sustainable Civil Infrastructures
*   **Category:** Hardware
