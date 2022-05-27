# i24_configparse

### Installation

```
pip install git+https://github.com/DerekGloudemans/i24_configparse@latest
```

Then, within your file:

```
os.environ["user_config_directory"] = <path to your config directory>   # all config file names will be specified relative to this directory
os.environ["my_config_section"] = "DEBUG"                               # os variable name that stores the section of the config files to be used


# for INI like configuration files
from i24_configparse import parse_cfg
params = parse_cfg("my_config_section",cfg_name = "parameter_file.config")

# for CSV like, delimited list files
from i24_configparse import parse_delim
params = parse_delim("access.list", "name", "P47C01")

```


### The config structure
parameter_file.config:
```
[SCHEMA]
a=int
b=[int]
c=$float
d=str

[DEFAULT]
a=6
b=1,456,3,21
d=Hello World

[RUNTIME]
c=0.756
```

and the result:
```

params.a 
>>> 6
params.b
>>> [1,456,3,21]
params.c
>>> 0.756
params.d
>>>"Hello World"
```

### The list structure
access.list:
```
name|host|user|password
P01C01|10.2.0.1|user1|password1
P47C01|10.2.0.47|user47|logmein
P47C20|10.2.20.3|userT|1234

```

and the result for ("name", "P47C01"):
```

params.name
>>> P47C01
params.host
>>> 10.2.0.47
params.user
>>> user47
params.password
>>> logmein

```