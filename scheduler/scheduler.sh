#!bin/bash

# UNIX script to setup cron job to run the cine monitor python script
# every 24 hrs

# Get parent path of current directory
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

touch /monitor.log
crontab -e
echo "Setting up cron job to run every day at 10AM"

# Run the script every day at 10AM
0 10 * * * parent_pat/monitor.py >> /monitor.log 2>&1
