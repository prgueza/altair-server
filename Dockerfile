FROM python:3.7.4
# Create app directory
WORKDIR /srv/altair-server
# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy app source code
COPY . .
# Expose listening port
EXPOSE 8338
# Set up environment variables
ENV PORT=8338
# Runtyme
CMD ["python", "server.py"]