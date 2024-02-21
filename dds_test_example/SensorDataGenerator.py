#SensorDataGenerator.py
import json
import threading
import time
import random

class SensorDataGenerator:
    def __init__(self, update_interval=10, **fixed_params):
        self.json_data= {}
        self.update_interval = update_interval
        self.fixed_params = fixed_params
        self.running = True
        self.callback = None
        self.update_thread = threading.Thread(target=self.generate_data_periodically)
        self.update_thread.start()

    def set_callback(self, callback):
        self.callback = callback    

    def generate_random_data(self):
        # 这里生成您的随机数据
        data = {
            # 数据字段，根据需要调整
            'capacity': random.randint(800, 1200),
            'remaining_capacity': random.randint(100, 800),
            'voltage': random.uniform(10.0, 12.5),
            'latitude': random.uniform(-90, 90),
            'longitude': random.uniform(-180, 180),
            'altitude': random.uniform(100, 10000),
            'speed': random.uniform(0, 100),
            'direction': random.randint(0, 360)
        }
        for key, value in self.fixed_params.items():
            data[key] = value
        return data

    def generate_data_periodically(self):
        while self.running:
            try:
                data = self.generate_random_data()
                json_data = json.dumps(data)
                if self.callback:
                    self.callback(json_data)
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Error in generate_data_periodically: {e}")
                time.sleep(self.update_interval)

    def stop(self):
        self.running = False
        self.update_thread.join()



