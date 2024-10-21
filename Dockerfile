FROM python:3.10-slim-buster

# Install cron
RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Give execution rights on the cron script
RUN chmod +x /app/scheduler/scheduler.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
RUN /app/scheduler/scheduler.sh

# Run the command on container startup
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
