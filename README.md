# i24_configparse

### Installation

```
pip install git+https://github.com/DerekGloudemans/i24_configparse@latest
```

Then, within your file:

```
os.environ["user_config_directory"] = <path to your config directory>   # all config file names will be specified relative to this directory
os.environ["my_config_section"] = "DEBUG"                               # os variable name that stores the section of the config files to be used
from i24_configparse.parse import parse_cfg


params = parse_cfg("my_config_section",cfg_name = "parameter_file.config")
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
