# pybossa-gravatar

[![Build Status](https://travis-ci.org/alexandermendes/pybossa-gravatar.svg?branch=master)]
(https://travis-ci.org/alexandermendes/pybossa-gravatar)
[![Coverage Status](https://coveralls.io/repos/alexandermendes/pybossa-gravatar/badge.svg)]
(https://coveralls.io/github/alexandermendes/pybossa-gravatar?branch=master) 
[![Code Health](https://landscape.io/github/alexandermendes/pybossa-gravatar/master/landscape.svg)]
(https://landscape.io/github/alexandermendes/pybossa-gravatar/master)

A PyBossa plugin for [Gravatar](http://en.gravatar.com/) integration.


## Installation

Simply copy the [pybossa_gravatar](pybossa_gravatar) folder into your PyBossa 
[plugins](https://github.com/PyBossa/pybossa/tree/master/pybossa/plugins) directory
and reboot the PyBossa server.


## Configuration

To modify the [default settings](default_settings.py) add the setting you want
to change to your main PyBossa configuration file. See the
[gravatar documentation](http://en.gravatar.com/site/implement/images/) for an
explanation of each setting.


## Usage

Once the plugin is installed a gravatar will be set as the default avatar for
all new users. Users can replace this by uploading their own avatar in the usual
way.

Signed in users can also switch back to their gravatar at any time by sending the
following request (perhaps via a button on their profile page):

```
POST http://{pybossa-site-url}/account/set-gravatar
```


## Contributing

For guidelines on how to suggest improvements, report bugs or submit pull
requests please refer to [CONTRIBUTING.md](CONTRIBUTING.md).