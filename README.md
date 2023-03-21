# parkrunRoster
A tool to generate a traffic light dashboard showing the state of a Parkrun volunteer roster

![Example Dashboard Image](https://github.com/jones139/parkrunRoster/blob/main/roster_hartlepool.png?raw=true)

# Command Line Usage
  - Download the html futureroster file for the required parkrun (e.g. https://www.parkrun.org.uk/hartlepool/futureroster/)
  - Use makeRosterImg.py to create a dashboard image file based on the futureroster html.


# Web App Usage
  - Run main.py to serve a simple web app at http://localhost:8080 to generate images.
  - http://localhost:8080/get?pRunName=<parkrun name> should dispaly a png image for the specified parkrun.   <parkrun name> should
      be the name that is in the futureroster url (e.g. hartlepool, rossmere-juniors)
  - Note that the app caches roster images and will only generate a new one if one does not exist for the requested parkrun or if the stored image is more than 10 minutes old.
  - There are no other useful endpoints


# Docker Install of Web App
  - Install Docker:
      - curl -fsSL https://get.docker.com -o get-docker.sh
      - sh get-docker.sh
  - Add the required user(s) to the new docker group in /et/group (then log out and back in again)
  - make build  (builds a docker container for the app)
  - make start  (runs the app in a docker container)
  - Install nginx
  - Create a new site in /etc/nginx/sites-enabled



Any queries or comments, please email graham@openseizuredetector.org.uk, or raise an issue on this repository.



