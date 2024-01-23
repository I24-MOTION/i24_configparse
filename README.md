# i24_configparse

### NEW Installation Link

```
pip install git+https://github.com/Lab-Work/i24_configparse@latest
```

Then, within your file:

```
os.environ["USER_CONFIG_DIRECTORY"] = <path to your config directories>   # a $PATH like list of directories containing the configuration files (separated by semicolon), 
os.environ["MY_CONFIG_SECTION"] = "DEBUG"                               # os variable name that stores the section of the config files to be used

from i24_configparse import parse_cfg, parse_delim


# for INI like configuration files
from i24_configparse import parse_cfg
params = parse_cfg("MY_CONFIG_SECTION",cfg_name = "parameter_file.config")

# for CSV like, delimited list files (returns a single entry for the specified key-value pair)
from i24_configparse import parse_delimited
params = parse_delimited("access.list", "key", "value")

# for CSV like, delimited list files (returns all entries in a dictionary for the specified key)
from i24_configparse import parse_delimited
params = parse_delimited("test1.list", "key")

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

### The list structure (single query)
access.list:
```
name=str|host=str|user=str|password=str
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

### The list structure (query all)
test1.list:
```
a=int|b=str|c=bool|d=float
 0 | B0 | false | 0
 1 | B1 | true | 1.1
 2 | B2 | False | 2.2
 3 | B3 | True | 3.3
 4 | B4 | off | 4.4
 5 | B5 | on | 5.5
 6 | B6 | Off | 6.6
 7 | B7 | On | 7.7
 8 | B8 | 0 | 8.8
 9 | B9 | 1 | 9.9

```

and the result for ("b"):
```

params['B0'].d
>>> 0.0
params['B1'].d
>>> 1.1
params['B6'].c
>>> False
params['B9'].c
>>> True

```
