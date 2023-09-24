FROM condaforge/mambaforge
# update the base image
# RUN apt-get update
# RUN apt-get install -yq wget git vim tmux

# RUN wget "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
# RUN bash Mambaforge-$(uname)-$(uname -m).sh -b -p mambaforge
# RUN rm Mambaforge-$(uname)-$(uname -m).sh
# RUN ./mambaforge/bin/conda init bash

COPY environment.yml environment.yml
RUN mamba env update -n base -f environment.yml
# RUN source ./mambaforge/bin/activate $(head -1 environment.yml | cut -d' ' -f2)
# RUN conda activate $(head -1 environment.yml | cut -d' ' -f2)
# RUN echo "conda activate $(head -1 ~/environment.yml | cut -d' ' -f2)" >> ~/.bashrc
# SHELL ["/bin/bash", "--login", "-c"]

COPY testing_app.ipynb testing_app.ipynb

# RUN my app panel serve --port 5006 --address 0.0.0.0 --allow-websocket-origin=199.94.60.108:5006 testing_app.ipynb 
CMD ["panel", "serve", "--port", "5006", "--address", "0.0.0.0","testing_app.ipynb"]
# expose the port 5006
EXPOSE 5006

