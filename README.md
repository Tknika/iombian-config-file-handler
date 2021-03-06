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

- Clone the repo into a temp folder:

> ```git clone https://github.com/Tknika/iombian-config-file-handler.git /tmp/iombian-config-file-handler && cd /tmp/iombian-config-file-handler```

- Create the installation folder and move the appropiate files (edit the user):

> ```sudo mkdir /opt/iombian-config-file-handler```

> ```sudo cp requirements.txt /opt/iombian-config-file-handler```

> ```sudo cp -r src/* /opt/iombian-config-file-handler```

> ```sudo cp systemd/iombian-config-file-handler.service /etc/systemd/system/```

> ```sudo chown -R iompi:iompi /opt/iombian-config-file-handler```

- Create the virtual environment and install the dependencies:

> ```cd /opt/iombian-config-file-handler```

> ```python3 -m venv venv```

> ```source venv/bin/activate```

> ```pip install --upgrade pip```

> ```pip install -r requirements.txt```

- Start the script

> ```sudo systemctl enable iombian-config-file-handler.service && sudo systemctl start iombian-config-file-handler.service```

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