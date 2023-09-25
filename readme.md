


## Create a env
```bash
conda env create --file environment.yml
```
## Run the App

```bash
conda activate routing_app
# panel serve testing_app.ipynb
panel serve --port 5006 --address 0.0.0.0 --allow-websocket-origin=199.94.60.108:5006 testing_app.ipynb 
```

## Docker deployment

```bash
docker build -t routing_app:0.1 .  
docker run -p 5006:5006 routing_app:0.1
```

## backend

1. Download the planet.osm.pbf file from [here](https://download.bbbike.org/osm/planet/)
2. follow the instruction [here](https://github.com/Project-OSRM/osrm-backend)

```bash
wget https://download.bbbike.org/osm/planet/planet-latest.osm.pbf

```

```bash
# install docker in ubuntu
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin 

# docker-compose-plugin

sudo apt-get update
# sudo apt-get install docker-compose-plugin

sudo docker run hello-world
# docker compose version

```


```bash
# it may take a while
sudo docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/planet-latest.osm.pbf || echo "osrm-extract failed"
```

```bash

```

## Tips

Create a biger swap file, please refer to [here](https://webapp.chatgpt4google.com/s/MTk2Njgw)


## To do

- [ ] add the backend