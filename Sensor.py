import serial
import time
from threading import Thread, Lock
import numpy as np

class SerialProcessor:
    def __init__(self):
        self.ser = serial.Serial('COM4', 115200, timeout=1)
        self.frequencies = []
        self.magnitudes = []
        self.adcs = []
        self.last_received = time.time()
        self.lock = Lock()
        self.running = True

    def read_serial(self):
        line_buffer = ""
        while self.running:
            if self.ser.in_waiting > 0:
                try:
                    data = self.ser.read(self.ser.in_waiting).decode('ascii', errors='ignore')
                    for char in data:
                        if char == '\n':
                            self.process_line(line_buffer.strip())
                            line_buffer = ""
                        else:
                            line_buffer += char
                except Exception as e:
                    print(f"Error: {e}")
            time.sleep(0.01)

    def process_line(self, line):
        if line.startswith("Max Freq:"):
            try:
                parts = line.split(',')
                freq = int(parts[0].split(':')[1].strip().split()[0])
                mag = int(parts[1].split(':')[1].strip().split()[0])
                adc = int(parts[2].split(':')[1].strip().split()[0])

                with self.lock:
                    self.frequencies.append(freq)
                    self.magnitudes.append(mag)
                    self.adcs.append(adc)
                    self.last_received = time.time()
            except (IndexError, ValueError) as e:
                print(f"Parse error: {e}")

    def check_timeout(self):
        while self.running:
            with self.lock:
                if time.time() - self.last_received > 2.0 and self.frequencies:
                    print("\n--- Collected Data ---")
                    print("Frequencies:", self.frequencies)
                    print("Magnitudes:", self.magnitudes)
                    print("ADC values:", self.adcs)

                    # Use frequency to determine object
                    
                    freq = max(self.frequencies)
                    mag = np.average(self.magnitudes)
                    adc = np.average(self.adcs)
                    if freq >= 190:
                        print(f"Frequency: {freq}Hz, Predicted object: Coin")
                        print(f"Magnitude: {mag}")
                        print(f"ADC: {adc}")

                        # 1010, 1030, 3010, 3030 
                        # threshold = [53082.95, 66000, 43400.8674, 64000]
                        threshold = [50082.95, 66000, 35400.8674, 61000]
                        err = [abs(mag - t) for t in threshold]
                        # id = err.index(min(err))
                        id = np.argmin(err)
                        print(id) 
                        
                        if(id == 0):
                            print("Distance: 10cm, Height: 10cm")
                        elif(id == 1):
                            print("Distance: 10cm, Height: 30cm")                        
                        elif(id == 2):
                            print("Distance: 30cm, Height: 10cm")
                        elif(id == 3):
                            print("Distance: 30cm, Height: 30cm")

                    else:
                        print(f"Frequency: {freq}Hz, Predicted object: Eraser")
                        print(f"Magnitude: {mag}")
                        print(f"ADC: {adc}")
                        threshold = np.array([134340.667, 185917.095, 111663.183, 154133.528])
                        err = np.abs(mag - threshold)
                        id = int(np.argmin(err)) 

                        if(id == 0):
                            print("Distance: 10cm, Height: 10cm")
                        elif(id == 1):
                            print("Distance: 10cm, Height: 30cm")                        
                        elif(id == 2):
                            print("Distance: 30cm, Height: 10cm")
                        else:
                            print("Distance: 30cm, Height: 30cm")

                        # if(adc > 500000):
                        #     print("Distance: 10cm, Height: 30cm")
                        # elif(adc > 320000):
                        #     print("Distance: 10cm, Height: 10cm")                        
                        # elif(adc > 190000):
                        #     print("Distance: 30cm, Height: 30cm")
                        # else:
                        #     print("Distance: 30cm, Height: 10cm")

                    # Clear for next batch
                    self.frequencies.clear()
                    self.magnitudes.clear()
                    self.adcs.clear()
            time.sleep(0.1)

processor = SerialProcessor()
try:
    Thread(target=processor.read_serial, daemon=True).start()
    Thread(target=processor.check_timeout, daemon=True).start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    processor.running = False
    processor.ser.close()
