import configparser
from ast import literal_eval
import warnings
import os


class Params():
    def __init__(self):
        pass

def parse_cfg(env_sec_name,cfg_name = None,obj = None,SCHEMA = True, return_type = "obj"):
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
    config_path = os.path.join(os.environ["USER_CONFIG_DIRECTORY"],cfg_name)
    config.read(config_path)
    
    # verify config path is valid
    if len(config.sections()) == 0:
        raise Exception("invalid config path specified, no such file exists or file is empty: {}".format(cfg_name))
    if len(config.defaults()) == 0:
        warnings.warn("No DEFAULT env specified in config file {}".format(cfg_name),UserWarning)    
    
    # get schema
    if 'SCHEMA' not in config.sections():
        if SCHEMA:
            warnings.warn("'SCHEMA' not in {}, so no schema will be enforced.".format(cfg_name),UserWarning)
            SCHEMA = False
            schema = {}
    else:
        # parse types from SCHEMA
        schema = dict(config["SCHEMA"])

    
    # get params
    try:
        env = os.environ[env_sec_name]
    except:
        env = "NONE"
    if env not in config.sections() and env != "DEFAULT":
        warnings.warn("{} specified as config environment in {} but no such environment exists. Using DEFAULT instead".format(env,cfg_name),UserWarning)
        env = "DEFAULT"
    
    params = dict([(key,config[env][key]) for key in config[env].keys()])
    # type-check each against schema
 
    for key in params.keys():
            if SCHEMA:
                if key not in schema.keys() or (key in config.defaults() and schema[key] == config.defaults()[key]):
                    raise KeyError("Key {} not specified in {} schema".format(key,cfg_name))
                
            # deal with optional parameter specifier $
            if key in schema.keys():
                schema_val = schema[key]
                if schema_val[0] == "$":
                    schema_val = schema_val[1:]
                
                if schema_val[0] == "[" and schema_val[-1] == "]":
                    schema_val = schema_val[1:-1]
                    items = params[key].split(",")
                    out = []
                    
                    if schema_val == "int":  
                        [out.append(int(literal_eval(item))) for item in items]
                    elif schema_val == "float":
                        [out.append(float(literal_eval(item))) for item in items]
                    elif schema_val == "bool":
                        [out.append(bool(literal_eval(item))) for item in items]
                    elif schema_val == "str":
                        out = items
                    params[key] = out
                
                # cast param as specified type
                elif schema_val == "int":
                    params[key] = int(literal_eval(params[key]))
                elif schema_val == "float":
                    params[key] = float(literal_eval(params[key]))
                elif schema_val == "bool":
                    params[key] = bool(literal_eval(params[key]))
                elif schema_val == "str":
                    params[key] = str(params[key])
                
            elif not SCHEMA:
                try:
                	params[key] = literal_eval(params[key])
                except:
                    pass
            else:
                raise ValueError("Invalid type specified in schema for key {}".format(key))
            
    # enforce that all schema objects are in environment or are optional\
    for key in schema.keys():
        if schema[key][0] != "$":
            if key not in params.keys():
                raise KeyError("Key {} specified in schema as required argument but not listed in ENV:{} or DEFAULT".format(key,env))
     
    if return_type == "obj":
        # assign params to object
        if obj is None:
            obj = Params()
        
        [setattr(obj,key,params[key]) for key in params.keys()]
    else:
        return params

    return obj            
