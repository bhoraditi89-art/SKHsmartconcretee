import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# --- 1. CONFIGURATION ---
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# We use a free public broker here for easy hackathon testing
MQTT_BROKER = "broker.hivemq.com"  
CLIENT_ID = "esp32-smart-concrete"
TOPIC_STRAIN = b"dipex2026/concrete/strain"
TOPIC_ALERT = b"dipex2026/concrete/alerts"

# --- 2. SENSOR SETUP ---
# Fiber optic amplifier connected to GPIO 34
sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)  # Allows reading up to 3.3V

# --- 3. WI-FI CONNECTION ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Wi-Fi Connected! IP:", wlan.ifconfig()[0])

# --- 4. MAIN LOOP ---
def run_system():
    connect_wifi()
    
    print("Connecting to Dashboard...")
    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.connect()
    print("Dashboard Connected!")

    while True:
        # Read the fiber optic sensor (gives a value from 0 to 4095)
        raw_value = sensor.read()
        
        # Convert raw data to a simulated stress percentage (0-100%)
        strain_percent = (raw_value / 4095) * 100
        
        print("Current Strain: {:.1f}%".format(strain_percent))
        
        # Send live data to the dashboard
        client.publish(TOPIC_STRAIN, str(strain_percent))
        
        # Trigger alert if strain is too high (Crack Detected!)
        if strain_percent > 75.0:
            print("CRACK DETECTED! Sending Alert...")
            client.publish(TOPIC_ALERT, "CRACK_DETECTED")
            
        # Wait 2 seconds before taking the next reading
        time.sleep(2) 

# Start the system
try:
    run_system()
except KeyboardInterrupt:
    print("System Stopped")