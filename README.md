# signal-profile-updater

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
