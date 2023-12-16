# import psutil
# import time

# def get_python_service_cpu_utilization():
#     python_processes = [proc for proc in psutil.process_iter(attrs=['pid', 'name']) if "python" in proc.info['name']]
#     cpu_percent = sum(proc.cpu_percent() for proc in python_processes) / psutil.cpu_count()
#     return cpu_percent

# while True:
#     cpu_utilization_value = get_python_service_cpu_utilization()
#     with open('./metrics/python_service_cpu_utilization.prom', 'w') as file:
#         file.write('# HELP python_service_cpu_utilization CPU utilization of the Python service\n')
#         file.write('# TYPE python_service_cpu_utilization gauge\n')
#         file.write(f'python_service_cpu_utilization {cpu_utilization_value}\n')
#     time.sleep(5)
# # time.sleep(150)


import time
import psutil
import os

def measure_disk_latency():
    disk_latency = psutil.disk_io_counters(perdisk=False).read_time / psutil.disk_io_counters(perdisk=False).read_count
    return disk_latency

def write_to_textfile(metric_value):
    with open('./metrics/disk_latency.prom', 'w') as file:
        file.write('# HELP disk_latency_ms Average latency of disk operations in milliseconds\n')
        file.write('# TYPE disk_latency_ms gauge\n')
        file.write('custom_disk_latency_ms {}\n'.format(metric_value))


def emulate_disk_latency():
    file_path = "./cpu_util.sh" 
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("This is a test file.")
    
    for i in range(10):
        with open(file_path, 'r') as file:
            content = file.read()
        
        time.sleep(0.1)
        
        with open(file_path, 'a') as file:
            file.write("This is a new line.\n")
        
        time.sleep(0.1)


def main():
    while True:
        emulate_disk_latency()
        disk_latency = measure_disk_latency()
        write_to_textfile(disk_latency)
        time.sleep(5)

if __name__ == "__main__":
    main()
