# Signal Profile Updater
This repository was made for some personal fun :D
The objective of the application updates every day the profile picture of my Signal profile, it is done by generating a profile picture by choosing a random word from a custom word list and then using that word as a query to downloading a picture from Unsplash via it's API.  
After editing the picture by drawing the chosen word, the number of days from first deployment, the last profile update's date, and a signature "PxHoussem", the application will update the Signal profile's picture.

## Requirements
- The Signal API docker container must be running locally: https://github.com/bbernhard/signal-cli-rest-api
- The phone number should be registered with the Signal API docker container (checkout [source](https://github.com/bbernhard/signal-cli-rest-api) on how to do so)

## Build the image
```bash
docker build -t signal_profile_updater .
```

## Run the image
```bash
export API_KEY="<UNSPLASH API KEY>"
export IP_ADDRESS="<IP ADDRESS>"
export PORT="8080"
export PHONE_NUMBER="<PHONE NUMBER>"

docker run \
	-e UNSPLASH_ACCESS_KEY=$API_KEY \
	-e IP_ADDRESS=$IP_ADDRESS \
	-e PORT=$PORT \
	-e PHONE_NUMBER=$PHONE_NUMBER \
	--name profile_updater --rm signal_profile_updater
```

## Delete the container
```bash
docker container rm profile_updater
```
