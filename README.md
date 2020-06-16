# quantML_python_server
Quant ML - REST API
=======

## Overview
This server is used for machine learning solution for forcasting trade trend

## Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install virtualenv
virtualenv env
source \env\Scripts\activate.bar
pip3 install -r requirements.txt
python3 -m imm_server
```

and open your browser to here:

```
http://localhost:8080/api/v1/ui
```

openapi spec definition lives here:

```
http://localhost:8080/swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t imm_server .

# starting up a container
docker run -p 8080:8080 imm_server
```
