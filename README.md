# Abandoned 🚧

> **⚠️ This project is no longer actively maintained.**

Thank you for your interest in this project. Unfortunately, it has been **abandoned** and is no longer receiving updates or support. Please feel free to fork, modify, or use the code as you see fit, but note that issues and pull requests will not be reviewed.


# Grass
An unofficial Docker Image for [getgrass.io](https://app.getgrass.io/register/?referralCode=VqlevN7hfQLGGiQ)
Available on [Docker Hub](https://hub.docker.com/r/camislav/grass)

## What's Grass?
Grass allows you to earn passive income by sharing your network bandwidth

## How to get started?
1. Register a Grass Account if you don't have one already: [getgrass.io](https://app.getgrass.io/register/?referralCode=VqlevN7hfQLGGiQ)
2. Either build this image from source, or download it from Docker Hub
3. Set envriomental variables to their respective values: GRASS_USER and GRASS_PASS
4. You're good to go! Once started, the docker exposes your current network status and lifetime earnings on port 80

### Docker Run Command
```
docker run -d \
    --name Grass \
    -p 8080:80 \
    -e GRASS_USER=myuser@mail.com \
    -e GRASS_PASS=mypass \
    -e ALLOW_DEBUG=False \
    camislav/grass
```

Please replace 8080 with the port you want to be able to access the status with, as well as GRASS_USER and GRASS_PASS

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.


