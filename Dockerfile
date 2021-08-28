FROM debian:buster
# Get required packages
RUN apt-get update && apt-get install python3 python3-pip python3-dotenv wget -y
RUN /usr/bin/wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | /usr/bin/apt-key add -
RUN /bin/bash -c '/bin/echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install google-chrome-stable -y
# Add new non privledged user
RUN useradd epicreminder
# Move app to root
ADD app/requirements.txt /
# Get required libraries
RUN pip3 install -r /requirements.txt
# Copy over the rest of the app
ADD app/ /app
# Give user ownership
RUN chown -R epicreminder /app
# Switch to non privledged user
# USER epicreminder
WORKDIR "/app"
# Run the script
CMD [ "python3", "/app/EpicReminder.py" ]
