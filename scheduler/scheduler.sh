#!/bin/bash

# UNIX script to setup cron job to run the cine monitor python script
# every 24 hrs

# Get parent path of current directory
parent_dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# Ensure the log file exists and is writable
touch /var/log/monitor.log
chmod 644 /var/log/monitor.log

# Create a new crontab entry
# cron_job="0 10 * * * /usr/local/bin/python3 $parent_dir/monitor.py >> /var/log/monitor.log 2>&1"
cron_job="* * * * * /usr/local/bin/python3 $parent_dir/monitor.py >> /var/log/monitor.log 2>&1"
(crontab -l 2>/dev/null; echo "$cron_job") | crontab -

echo "Cron job set up to run every day at 10AM"
