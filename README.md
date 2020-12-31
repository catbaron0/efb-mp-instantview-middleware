# MPInstanceViewMiddleware: A middleware for EFB 

## Notice

**Middleware ID**: `catbaron.mp_instantview`

The middleware ID was `catbaron.mp_instantview` before version 0.3.0. Please take care of it, especially please remeber to update the configure file of EFB (`$HOME/.ehforwarderbot/profiles/default/config.yaml`).

**MPInstanceViewMiddleware** is a middleware of EFB enable instant view for articles of official accounts.

## How it works
This middleware generates a telegraph page for links sent by official accounts of wechat, which will enable the instant view. Thus you need a `access_token` (introduced later).

## Dependense
* Python >= 3.6
* EFB >= 2.0.0
* PyYaml
* bs4
* requests[sock]

## Install and configuration

### Install
```
git clone https://github.com/catbaron0/efb-mp-instanceview-middleware
cd efb-mp-instantview-middleware
sudo python setup.py install
```

### Enable

Register to EFB
Following [this document](https://ehforwarderbot.readthedocs.io/en/latest/getting-started.html) to edit the config file. The config file by default is `$HOME/.ehforwarderbot/profiles/default`. It should look like:

```yaml
master_channel: foo.demo_master
slave_channels:
- foo.demo_slave
- bar.dummy
middlewares:
- foo.other_middlewares
- catbaron.mp_instantview
```

You only need to add the last line to your config file.

### Configure the middleware

The config file by default is `$HOME/.ehforwarderbot/profiles/default/catbaron.mp_instantview/config.yaml`.
Please create the config file if there is not one. You need to have a telegraph token and save it here. You can get a token following [the document](https://telegra.ph/api#createAccount). The `access_token` is what you need.

This middleware need access to https://telegra.ph, add the proxy url to the configure file if necessary.

```yaml
# Token of telegraph
telegraph_token: ACCESS_TOKEN

# Optional. Proxy url.
# Example:
#  proxy_url: socks5://<user>:<pass>@<host>:<port>
#  proxy_url: socks5://<host>:<port>
#  proxy_url: http://<host>:<port>
proxy_url: PROXY_URL
```

### Restart EFB.
