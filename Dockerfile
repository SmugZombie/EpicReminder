FROM debian:buster
# Get required packages
RUN apt-get update && apt-get install python3 python3-pip python3-dotenv chromium -y
# Add new non privledged user
RUN useradd epicreminder
# Move app to root
ADD app/requirements.txt /
# Get required libraries
RUN pip3 install -r /requirements.txt
# Copy over the rest of the app
ADD app/ /
# Switch to non privledged user
USER epicreminder
# Run the script
CMD [ "python3", "./EpicReminder.py" ]

