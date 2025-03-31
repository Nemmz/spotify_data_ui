# Use the official Python 3.13 image as the base
FROM python:3.13

# Copy everything not excluded by .dockerignore into the container directory /app
COPY . /app

# Install the required packages
# --no-cache-dir prevents unnecessary cache storage, reducing image size.
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt \
    && pip install --no-cache-dir --upgrade -r /app/tests/requirements.txt

# Set the working directory for the application
# I.e.: CMD, RUN, or ENTRYPOINT commands will execute inside /app.
WORKDIR /app

# Define the default command to run when the container starts
# Using CMD instead of ENTRYPOINT allows users to override the command if needed:
CMD ["streamlit", "run", "app/artist_inquiry_ui.py"]