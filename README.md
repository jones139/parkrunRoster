# parkrunRoster
A tool to generate a traffic light dashboard showing the state of a Parkrun volunteer roster

![Example Dashboard Image](https://github.com/jones139/parkrunRoster/blob/main/roster_hartlepool.png?raw=true)

# Command Line Usage
  - Download the html futureroster file for the required parkrun (e.g. https://www.parkrun.org.uk/hartlepool/futureroster/)
  - Use makeRosterImg.py to create a dashboard image file based on the futureroster html.


# Web App Usage
  - Install Docker:
      - curl -fsSL https://get.docker.com -o get-docker.sh
      - sh get-docker.sh
  - Add the required user(s) to the new docker group in /et/group (then log out and back in again)
  - make build  (builds a docker container for the app)
  - make start  (runs the app in a docker container)



Any queries or comments, please email graham@openseizuredetector.org.uk, or raise an issue on this repository.



