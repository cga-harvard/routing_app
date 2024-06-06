


# Routing App

## How to run locally

### Create a env
```bash
conda env create --file environment.yml
```
### Run the App

```bash
conda activate routing_app
# panel serve testing_app.ipynb
panel serve --port 5006 routing_app.py
```

## How to run using docker 

### build and run the docker image

change CMD commands in Dockerfile and run,

```bash
docker build -t routing_app:0.1 .  
docker run -p 5006:5006 routing_app:0.1
```

### build and push the docker image to docker hub

push to docker hub, please change the happybeetles to your own user name, you need login to Dockerhub both in your terminal, you need create a repo called routing_app in your docker hub.

```bash
docker build --platform=linux/amd64 -t routing_app:1.3 .
docker tag routing_app:1.3 happybeetles/routing_app
docker push happybeetles/routing_app
```

## About the backend

For the whole planet service, you can following these steps,

1. Download the planet.osm.pbf file from [here](https://download.bbbike.org/osm/planet/)
2. follow the instruction [here](https://github.com/Project-OSRM/osrm-backend)

```bash
wget https://download.bbbike.org/osm/planet/planet-latest.osm.pbf

```

```bash
# it may take a while
# sudo docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/planet-latest.osm.pbf || echo "osrm-extract failed"
```

## Deployment in openshift

1. Deploy the backend first, you can do it using the Openshift web portal to deploy the backend from [this Github repo](https://github.com/wybert/routing_app_service).
2. Please find the backend service ip address in the Openshift web portal by click on the pod's name, and update the backend service ip address in the `routing_app.py` file. change the following line in the `routing_app.py` file.

```python

# create a router object 
router = OSRMRouter(mode="driving",
                    base_url="http://<ip_address_of_the_backend_service>:5000"
                    )

```

3. Build the Docker image and push it to the docker hub. You can use the following command to build the docker image. 

```bash
docker build --platform=linux/amd64 -t routing_app:1.3 .
docker tag routing_app:1.3 happybeetles/routing_app
docker push happybeetles/routing_app
```

You need to login to your own docker hub account before you can push the image to the docker hub. My docker hub account is `happybeetles`, you need to change it to your own docker hub account.

4. Deploy the frontend using the Openshift web portal from the Docker image you just pushed to the docker hub. For Openshift setting, you need use this url `routing-ui-gis-data-science-big-data-projects-at-cga.apps.shift.nerc.mghpcc.org` for the frontend service

5. Once done, visit the frontend service url `routing-ui-gis-data-science-big-data-projects-at-cga.apps.shift.nerc.mghpcc.org`, you should be able to see the frontend.

## Tips

If you don't have enough memory, you may need to create a swap file. Create a biger swap file, please refer to [here](https://webapp.chatgpt4google.com/s/MTk2Njgw)


## To do
