import numpy as np
import tensorflow as tf
import os

print("🧠 Starting Smart Concrete ML Training...")

# --- 1. GENERATE SYNTHETIC HACKATHON DATA ---
# We are simulating 3 sensor inputs: [Current Strain %, Strain Rate of Change, Temperature]
# Label: 0 = Healthy Concrete, 1 = Micro-crack forming

num_samples = 2000

# Normal structural behavior (Safe)
safe_strain = np.random.uniform(10, 40, (num_samples // 2, 1))
safe_change = np.random.uniform(0.1, 2.0, (num_samples // 2, 1))
safe_temp = np.random.uniform(20, 35, (num_samples // 2, 1))
safe_labels = np.zeros((num_samples // 2, 1))
safe_data = np.hstack((safe_strain, safe_change, safe_temp))

# Stress behavior (Crack Forming)
crack_strain = np.random.uniform(60, 95, (num_samples // 2, 1))
crack_change = np.random.uniform(5.0, 15.0, (num_samples // 2, 1))
crack_temp = np.random.uniform(35, 50, (num_samples // 2, 1)) # Micro-friction causes heat
crack_labels = np.ones((num_samples // 2, 1))
crack_data = np.hstack((crack_strain, crack_change, crack_temp))

# Combine and shuffle
X = np.vstack((safe_data, crack_data))
y = np.vstack((safe_labels, crack_labels))

# Normalize data (Scale 0 to 1) for the microcontroller
X_normalized = X / [100.0, 20.0, 60.0]

# --- 2. BUILD THE NEURAL NETWORK ---
# Keep it super lightweight so it runs fast on the ESP32 chip
model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, activation='relu', input_shape=(3,)),
    tf.keras.layers.Dense(4, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid') # Outputs a probability (0.0 to 1.0)
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# --- 3. TRAIN THE MODEL ---
print("🏋️ Training the Neural Network...")
model.fit(X_normalized, y, epochs=20, batch_size=32, validation_split=0.2)

# --- 4. CONVERT TO TENSORFLOW LITE ---
print("📦 Converting to TensorFlow Lite format...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
# Optimize for size to fit on the ESP32
converter.optimizations = [tf.lite.Optimize.DEFAULT] 
tflite_model = converter.convert()

# Save the .tflite file
with open('smart_concrete_model.tflite', 'wb') as f:
    f.write(tflite_model)

# --- 5. EXPORT AS C-ARRAY (TINYML FORMAT) ---
# Microcontrollers read C-arrays much easier than raw files. 
# We convert the tflite file into a C header file automatically here.
def get_c_array(tflite_model):
    c_str = "const unsigned char model_tflite[] = {\n  "
    for i, val in enumerate(tflite_model):
        c_str += f"0x{val:02x}, "
        if (i + 1) % 12 == 0:
            c_str += "\n  "
    c_str += "\n};\n"
    c_str += f"const unsigned int model_tflite_len = {len(tflite_model)};\n"
    return c_str

with open('smart_concrete_model.h', 'w') as f:
    f.write(get_c_array(tflite_model))

print("✅ SUCCESS! Generated 'smart_concrete_model.tflite' and 'smart_concrete_model.h'")