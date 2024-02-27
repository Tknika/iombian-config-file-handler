# IoMBian Config File Handler

This service handles the configuration file located in the "/boot/config/parameters.yml" path.

The communication must be done through a ZeroMQ socket (5555 port by default), following the REQ/REP pattern. The available commands are:

- ```is_configured()```
- ```get_device_id()```
- ```get_refresh_token()```
- ```get_api_key()```
- ```get_project_id()```
- ```get_config_date()```
- ```reset()```
- ```save_config(<new_config>)```

## Installation

- Define project name in an environment variable:

> ```PROJECT_NAME=iombian-config-file-handler```

- Clone the repo into a temp folder:

> ```git clone https://github.com/Tknika/${PROJECT_NAME}.git /tmp/${PROJECT_NAME} && cd /tmp/${PROJECT_NAME}```

- Create the installation folder and move the appropiate files (edit the user):

> ```sudo mkdir /opt/${PROJECT_NAME}```

> ```sudo cp requirements.txt /opt/${PROJECT_NAME}```

> ```sudo cp -r src/* /opt/${PROJECT_NAME}```

> ```sudo cp systemd/${PROJECT_NAME}.service /etc/systemd/system/```

> ```sudo chown -R iompi:iompi /opt/${PROJECT_NAME}```

- Create the virtual environment and install the dependencies:

> ```cd /opt/${PROJECT_NAME}```

> ```python3 -m venv venv```

> ```source venv/bin/activate```

> ```pip install --upgrade pip```

> ```pip install -r requirements.txt```

- Start the script

> ```sudo systemctl enable ${PROJECT_NAME}.service && sudo systemctl start ${PROJECT_NAME}.service```

## Docker

To build the docker image, from the cloned repository, execute the docker build command in the same level as the Dockerfile.

`docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .`

For example: `docker build -t iombian-config-file-handler:latest .`

After building the image, execute it with docker run

`docker run --name ${CONTAINER_NAME} --privileged --rm -d -p 5555:5555 -v /run/systemd/system:/run/systemd/system -v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket -v /bin/systemctl:/bin/systemctl -v /boot/config/parameters.yml:/app/parameters.yml -e RESET_EVENT=tripe_click`

- --name is used to define the name of the created container.

- -privileged is for granting privileges to the docker container.
This is needed because the iombian-button-handler needs to create a thread to listen to the button events.

- --rm can be used to delete the container when it stops.
This parameter is optional.

- -d is used to run the container detached.
This way the container will run in the background.
This parameter is optional.

- -p is used to expose the internal 5555 port to the external 5555 port.
The 5555 port is where other services will need to connect to get the configuration information.
The port is exposed so the services from outside the containers network can access to the configuration.

- -v is used to pass a volume to the container.
The first three volumes are used to give the container acces to some files.
This volumes are necessary so the container can reboot the host machine.
The last volume is used to access the machine configuration from the container.

- -e can be used to define the environment variables:
    - CONFIG_PORT: the port where the services will connect to acces the configuration.
    Default value is 5555.
    - RESET_EVENT: the button event to reset the raspberry.
    Default value is long_long_click.
    - LOG_LEVEL: define the log level for the python logger.
    This can be NOTSET, DEBUG, INFO, WARNING, ERROR or CRITICAL.
    Default value is INFO.
    - BUTTON_EVENTS_HOST: the host where the button events will be published.
    Default value is the localhost 127.0.0.1.
    - BUTTON_EVENTS_PORT: the port where the button events will be published.
    Default value is 5556.
    - YAML_FILE_PATH: The path where the parameters.yml file is located inside the container.
    Default path is /app/parameters.yml.

## Author

(c) 2021 [Aitor Iturrioz Rodríguez](https://github.com/bodiroga)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
