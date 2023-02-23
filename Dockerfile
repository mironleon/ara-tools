FROM python:3.11-slim

# install the notebook package
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache notebook jupyterlab

# copy package directory
COPY . /tmp/aratools
RUN pip install /tmp/aratools

RUN apt-get update -y
RUN apt-get install texlive-latex-extra  -y

# create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}
USER ${USER}

COPY /tests/example_data ${HOME}/example_data
RUN mkdir input_csvs output_pdfs
COPY /aratools/Notebooks/generate_pdfs.ipynb ${HOME}
