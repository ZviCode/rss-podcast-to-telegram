# Use an appropriate base image
FROM python:3.9-slim

# Install cron
RUN apt-get update && apt-get install -y cron

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install any Python dependencies
RUN pip install -r requirements.txt

# Copy the crontab file and setup cron
COPY crontab /etc/cron.d/rssfeed-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/rssfeed-cron

# Apply cron job
RUN crontab /etc/cron.d/rssfeed-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
