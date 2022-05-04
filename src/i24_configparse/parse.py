import configparser
from ast import literal_eval
import warnings
import os


class Params():
    def __init__(self):
        pass

def parse_cfg(env,cfg_name = None,obj = None,SCHEMA = True):
    """
    Loads config file within system config directory specified by cfg_name, and within this file loads 
    the specified config enviroment. If an object is specified, each field is set as an attribute
    If no object is specified, a dummy Params object is returned with these attributes
    If SCHEMA, each attribute is checked to ensure it corresponds to the schema
    cfg_name -  str (name of file within config_directory)
    
    """
    
    # if no cfg_name is specified, use default name based on object type
    if cfg_name is None and obj is not None:
        cfg_name = type(obj).__name__ + ".config"
    elif cfg_name is None:
        raise Exception("Either obj or cfg_name must be passed to cfg_parse")
    
    
    def lex_cast_type(name):
        return __builtins__.get(name)
    
    config = configparser.ConfigParser()
    config_path = os.path.join(os.environ["user_config_directory"],cfg_name)
    config.read(config_path)
    
    # verify config path is valid
    if len(config.sections()) == 0:
        raise Exception("invalid config path specified, no such file exists or file is empty: {}".format(cfg_name))
    if len(config.defaults()) == 0:
        warnings.warn("No DEFAULT env specified in config file {}".format(cfg_name),UserWarning)    
    
    # get schema
    if SCHEMA:
        if 'SCHEMA' not in config.sections():
            warnings.warn("'SCHEMA' not in {}, so no schema will be enforced.".format(cfg_name),UserWarning)
            SCHEMA = False
        
        else:
            # parse types from SCHEMA
            schema = dict(config["SCHEMA"])
    
    # get params
    if env not in config.sections():
        warnings.warn("{} specified as config environment in {} but no such environment exists. Using DEFAULT instead".format(env,cfg_name),UserWarning)
        env = "DEFAULT"
    
    params = dict([(key,literal_eval(config[env][key])) for key in config[env].keys()])
    # type-check each against schema
    if SCHEMA:
        for key in params.keys():
            if key not in schema.keys() or (key in config.defaults() and schema[key] == config.defaults()[key]):
                raise KeyError("Key {} not specified in {} schema".format(key,cfg_name))
            if type(params[key]) != lex_cast_type(schema[key]):
                raise TypeError("Provided config value {}:{} in {} does not match schema. ENV:{}, SCHEMA:{}".format(key,params[key],cfg_name,type(params[key]),lex_cast_type(schema[key])))
                    
        
        
    # assign params to object
    if obj is None:
        obj = Params()
    
    [setattr(obj,key,params[key]) for key in params.keys()]

    return obj            