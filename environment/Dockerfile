# hash:sha256:b829f022b00d5a2c8d28d66f7f5c0326648d4725e31ea1fb547441f229b25ce7
FROM registry.codeocean.com/codeocean/miniconda3:4.12.0-python3.9-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN conda install -y --channel=opensim-org \
        opensim==4.4 \
    && conda clean -ya

RUN pip3 install -U --no-cache-dir \
    hydra-colorlog==1.2.0 \
    hydra-core==1.2.0 \
    importlib-resources==5.9.0 \
    imufusion==1.0.6 \
    numpy==1.23.3 \
    pandas==2.0.1 \
    scipy==1.9.1 \
    utils==1.0.1
