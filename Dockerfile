# Set the base image to use
FROM python:3.9.15-slim-buster

# Set working directory
WORKDIR /app

# Copy of our app's requirements file
COPY api/requirements.txt .

# We update Pip and install the Python dependencies required by our application, we use the flag --root-user-action=ignore to avoid warning for using root for this action
RUN python -m pip install --root-user-action=ignore --upgrade pip

RUN pip install --root-user-action=ignore -U pip && pip install --root-user-action=ignore -r requirements.txt

# Copy of folders and files required to run our application
COPY api/ ./api

COPY model/model.pkl ./model/model.pkl

COPY initializer.sh .

# We grant execution permissions to the initializer file of our app
RUN chmod +x initializer.sh

# We expose port 8000 of our app, since it is the default used by FasAPI
EXPOSE 8000

# Command to start the application
ENTRYPOINT ["./initializer.sh"]