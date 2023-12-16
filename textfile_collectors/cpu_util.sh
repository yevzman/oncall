#!/bin/bash

# Function to calculate Python service CPU utilization
get_python_service_cpu_utilization() {
  python_processes=$(ps -e -o pid,comm | awk '$2=="python"{print $1}')
  total_cpu_percent=0
  cpu_count=$(nproc)

  for pid in $python_processes
  do
    cpu_percent=$(ps -p "$pid" -o %cpu | tail -n 1)
    total_cpu_percent=$(echo "$total_cpu_percent + $cpu_percent" | bc)
  done

  avg_cpu_utilization=$(echo "scale=2; $total_cpu_percent / $cpu_count" | bc)
  echo $avg_cpu_utilization
}

# Get current time
current_time=$(date +%s)

# CPU utilization calculation
cpu_utilization_value=$(get_python_service_cpu_utilization)

# Write to the metric file
cat > /var/lib/node_exporter/textfile_collector/python_service_cpu_utilization.prom <<EOF
# HELP python_service_cpu_utilization CPU utilization of the Python service
# TYPE python_service_cpu_utilization gauge
python_service_cpu_utilization $cpu_utilization_value $current_time
EOF
