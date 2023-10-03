#!/bin/bash

useradd -m wikivi
usermod --shell /bin/bash wikivi

apt-get install -y postgresql python3-pip python3-venv



