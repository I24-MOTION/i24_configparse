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
