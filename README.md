# pybossa-gravatar

[![Build Status](https://travis-ci.org/alexandermendes/pybossa-gravatar.svg?branch=master)]
(https://travis-ci.org/alexandermendes/pybossa-gravatar)
[![Coverage Status](https://coveralls.io/repos/alexandermendes/pybossa-gravatar/badge.svg)]
(https://coveralls.io/github/alexandermendes/pybossa-gravatar?branch=master)

A [PyBossa](https://github.com/PyBossa/pybossa) plugin for [Gravatar](http://en.gravatar.com/) integration.


## Installation

Copy the [pybossa_gravatar](pybossa_gravatar) folder into your PyBossa 
[plugins](https://github.com/PyBossa/pybossa/tree/master/pybossa/plugins) directory. The 
plugin will be available after you next restart the server. 


## Configuration

The default configuration settings for pybossa-gravatar are:

``` Python
GRAVATAR_SIZE = 512
GRAVATAR_DEFAULT_IMAGE = 'identicon'
GRAVATAR_RATING = 'g'
GRAVATAR_FORCE_DEFAULT = False
GRAVATAR_SECURE_REQUESTS = False
```

You can modify these settings by adding them to your main PyBossa configuration file. 
See the [Gravatar documentation](http://en.gravatar.com/site/implement/images/) for a
description of each setting.


## Usage

Once the plugin is installed a Gravatar will be set as the default avatar for
all new users. Users can replace this by uploading their own avatar in the usual
way. Users can also switch to using a Gravatar at any time via:

```
http://{pybossa-site-url}/account/<name>/update/gravatar/set
```

One option would be to add a button to
[update.html](https://github.com/PyBossa/pybossa-default-theme/blob/master/templates/projects/update.html) 
that will only appear if the plugin is installed, like this:

``` HTML+Django
{% if 'pybossa-gravatar' in plugins.keys() %}
    <a href="{{url_for('set_gravatar', name=current_user.name)}}" class="btn btn-primary">
        Import Gravatar
    </a>
{% endif %}
```


## Testing

This plugin makes use of the PyBossa test suite while running tests. The
[Travis CI configuration file](.travis.yml) contains all of the required commands to set
up a test environment and run the tests.


## Contributing

See the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to suggest improvements, 
report bugs or submit pull requests.