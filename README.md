# CloudVolumeServer
Flask application to serve data via CloudVolume.

This is currently a one-trick pony! The one thing it does is provide an API
endpoint to query multiple x/y/z locations at once.

## Python dependencies

- [CloudVolume](https://github.com/seung-lab/cloud-volume): `pip install cloud-volume`
- [Gunicorn](https://gunicorn.org): `pip install gunicorn`
- [flask](https://palletsprojects.com/p/flask/): `pip install flask`
- [numpy](https://numpy.org): `pip install numpy`
- [pandas](https://pandas.pydata.org): `pip install pandas`

## Deploying

1. Clone this repository on your server
2. Install above dependencies
3. Edit `config.py` and minimally add the path to the volume:
   ```Python
   CloudVolumeKwargs = {
                        cloudpath="file:///fafbz/fafb14/segmentation/"
                       }
   ```
4. Test if Gunicorn can start the workers - from within the repository run:
   ```bash
   gunicorn --workers 1 --bind 0.0.0.0:6000 -m 007 wsgi:app --log-level debug
   ```
   If all works well, CTRL-C to stop.
5. Add Gunicorn to `systemd`:
   ```bash
   sudo nano /etc/systemd/system/cloudvolumeserver.service
   ```
   Then copy paste this (make sure to replace `YOURUSER` and `PATH/TO/REPOSITORY`)
   ```
   [Unit]
   Description=Gunicorn instance to serve the CloudVolumeServer
   After=network.target

   [Service]
   User=YOURUSER
   Group=www-data
   WorkingDirectory=PATH/TO/REPOSITORY/CloudVolumeServer
   ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:6000 -m 007 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```
   Note that you can also bind Gunicorn to a sock instead of a port but that didn't
   work in my hands.

   You can now start the Gunicorn service by running:
   ```
   sudo systemctl start cloudvolumeserver
   sudo systemctl enable cloudvolumeserver
   ```
6. Setup your nginx server and add the following server block to the config
   file in `/etc/nginx/sites-available`:
   ```
   location /seg/ {
                  include proxy_params;                  
                  proxy_pass http://localhost:6000/;
                  }
   ```
7. Restart your nginx: `sudo systemctl restart nginx`
8. All done. Check if the site is running by visiting `http://your-server.url/seg/`.

For more details: the configuration steps roughly follow [this](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04) tutorial.

## Examples

```Python

import requests

# Some random locations
# Please note that we need to query pixel coordinates, not native coordinates
coords = [[58695, 28631,   696],
          [58688, 28632,   691],
          [58691, 28635,   698]]

url = 'http://your-server.url/seg/'
resp = requests.post(url, json=coords)

print('Segment IDs:', resp.json())
```


## License
This code is published under a BSD 2-Clause License.
