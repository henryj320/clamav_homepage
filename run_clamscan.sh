#!/bin/bash

if grep -q "virusEvent=True" "/home/henry/Software/clamav_homepage/updates/.env"; then
	echo "Exiting. Virus already found!"
	exit 1
fi

start_time=$(date +%s)

# Run clamscan and capture its output.
scan_output=$(clamscan -i -r /home/henry/SharedFolder --exclude-dir=/home/henry/SharedFolder/Henry/Backups/Media --exclude-dir=/home/henry/SharedFolder/Henry/Backups/Documents --exclude-dir=/home/henry/SharedFolder/Tyler/hj320mcserver.xyz_Backups --exclude-dir=/home/henry/SharedFolder/Tyler/Backups_from_the_happening)

log_file_location="/home/henry/SharedFolder/Henry/Logs/clamav.log"

# Calculate how long it took to run.
end_time=$(date +%s)
duration=$((end_time - start_time))
formatted_duration=$(date -u -d @$duration +'%H:%M:%S')

# Check the exit status of clamscan
if [ $? -ne 0 ]; then
    echo "clamscan encountered an error or found a virus."
    echo "$scan_output"  # Output the details of the scan
    echo "virusEvent=True" > /home/henry/Software/clamav_homepage/updates/.env

    output=$(echo "$(date "+%Y-%m-%d %H:%M:%S") - $scan_output")
    echo "$output" >> $log_file_location
    echo "Scan Duration: $formatted_duration" >> $log_file_location
else
    echo "No viruses found."
    echo "virusEvent=False" > /home/henry/Software/clamav_homepage/updates/.env

    output=$(echo "$(date "+%Y-%m-%d %H:%M:%S") - No viruses found.")
    echo "$output" >> $log_file_location
    echo "Scan Duration: $formatted_duration" >> $log_file_location
fi

