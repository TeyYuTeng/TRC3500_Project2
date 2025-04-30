import serial
import re
import os
# Coin_10_10 Freq: 113-244 Magnitude: > 70000
# Coin_10_30 

# Settings
port = 'COM4'
baudrate = 115200
name = 'test'
output_path = r'C:\Users\yttey\Desktop\TRC3500\Project2Data'  # <-- Change this to your target path

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)

# Construct full file paths
freq_file_path = os.path.join(output_path, f"{name}_frequency.txt")
mag_file_path = os.path.join(output_path, f"{name}_magnitude.txt")

# Open serial port
ser = serial.Serial(port, baudrate, timeout=1)

# Open files for appending
f_freq = open(freq_file_path, "a")
f_mag = open(mag_file_path, "a")

print(f"Writing to:\n{freq_file_path}\n{mag_file_path}")
print("Reading from UART... Press Ctrl+C to stop.")

try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line:
            print(line)
            match = re.search(r"Max Freq:\s*(\d+)\s*Hz,\s*Magnitude:\s*(\d+)", line)
            if match:
                freq = match.group(1)
                mag = match.group(2)
                f_freq.write(freq + ",")
                f_mag.write(mag + ",")
                f_freq.flush()
                f_mag.flush()
except KeyboardInterrupt:
    print("\nTerminated by user.")
finally:
    ser.close()
    f_freq.close()
    f_mag.close()
