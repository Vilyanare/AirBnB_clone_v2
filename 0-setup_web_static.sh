#!/usr/bin/env bash
# installs nginx and then sets up web static environment
sudo apt-get update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo -e '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>' > ~/index.html
sudo mv ~/index.html /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
HBNB_STATIC="\ \n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "29i$HBNB_STATIC" /etc/nginx/sites-available/default
sudo service nginx restart
