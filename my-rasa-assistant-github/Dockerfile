# Extend the official Rasa SDK image
FROM rasa/rasa-pro:3.15.10

# Use subdirectory as working directory
WORKDIR /app

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code
# SQL
RUN pip install --no-cache-dir psycopg2-binary
# dnspython is required for mongodb+srv:// URLs
RUN pip install --no-cache-dir pymongo dnspython

# Copy everything from your local folder into the /app folder of the container
COPY --chown=1001:1001 . /app

ENV HOME=/tmp
RUN mkdir -p /tmp/.config/gcloud && chown -R 1001:1001 /tmp

# By best practices, don't run the code with root user
USER 1001

ENTRYPOINT ["rasa"]
CMD ["run", "--enable-api", "--port", "5005", "--cors", "*", "--endpoints", "endpoints.yml", "--credentials", "credentials.yml"]
