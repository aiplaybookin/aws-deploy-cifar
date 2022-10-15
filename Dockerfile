FROM python:3.7-slim-buster

ENV GRADIO_SERVER_PORT 80

# Set working directory
WORKDIR /workspace/project

# Install requirements
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt 

COPY inference.py ./

COPY images ./images

# tell the port number the container should expose
EXPOSE 80

# run the application
CMD [ "python3", "inference.py"]