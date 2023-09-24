


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


## To do

- [ ] add the backend