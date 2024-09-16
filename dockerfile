# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Set environment variables
ENV COHERE_API_KEY=<Lt7NBVBllT6ZU1FwA3bUq1NmTYASnP14fLIInOct> 

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "app.py"]
