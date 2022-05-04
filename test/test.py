import time
import os, sys
import warnings
from src.i24_configparse.parse import parse_cfg






# set os environment config path
cwd = os.getcwd()
cfg = "./config"
config_path = os.path.join(cwd,cfg)
os.environ["user_config_directory"] = config_path # note that this may not affect processes globally

#%% Input Tests

# TEST 1 - Exception thrown when no cfg_name or obj are passed
try:
    parse_cfg("DEBUG")
    print("TEST 1: FAIL- does not correctly handle case with no cfg_name or obj input")
except Exception as e:
    print("TEST 1: PASS - (Correctly throws Exception: {})".format(e))
    
    
# TEST 2 - Exception when  cfg_path is specified incorrectly
try:
    parse_cfg("DEBUG",cfg_name = "test_badpath.config")
    print("TEST 2: FAIL- does not raise error when invalid config name was specified")
except Exception as e:
    print("TEST 2: PASS - (Correctly throws Exception: {})".format(e))


# TEST 3 - UserWarning when no DEFAULT env is specified in config
with warnings.catch_warnings(record = True) as w:
    cfg = parse_cfg("DEBUG",cfg_name = "test2.config")
    if w[-1].category == UserWarning:
        print("TEST 3: PASS - (Correctly throws UserWarning when no DEFAULT env is specified in config)")
    else:
        print("TEST 3: FAIL - does not raise UserWarning when no DEFAULT env is specified")   
 
# TEST 4 - UserWarning when invalid environment is specified
with warnings.catch_warnings(record = True) as w:
    cfg = parse_cfg("DEBUG_MISSPELL",cfg_name = "test1.config")
    if w[-1].category == UserWarning:
        print("TEST 4: PASS - (Correctly throws UserWarning and switched to DEFAULT when invalid env is specified)")
    else:
        print("TEST 4: FAIL - does not raise UserWarning when invalid env was specified")
        
    
#%% Correct Behavior Tests


# TEST 5 -  verify correct behavior with default paramas object
start = time.time()
cfg = parse_cfg("DEBUG",cfg_name = "test1.config")
elapsed = time.time() - start
try:
    cfg.a,cfg.b,cfg.c,cfg.d,cfg.e
    print("TEST 5: PASS - took {:.5f}s to check schema for 5 attributes".format(elapsed))
except AttributeError:
    print("TEST 5: FAIL- param object doesn't have all attributes specified in config")


# TEST 6 - verify correct behavior with input object
class TestObj():
    def __init__(self):
        pass

obj = parse_cfg("PROD",obj = TestObj())
try:
    obj.a,obj.b,obj.c,obj.d,obj.e
    print("TEST 6: PASS")
except AttributeError:
    print("TEST 6: FAIL- param object doesn't have all attributes specified in config")
    
    

#%% Schema Tests

# TEST 7 - Exception when invalid type is specified in schema
try:
    parse_cfg("DEBUG",cfg_name = "test3.config")
    print("TEST 7: FAIL- does not raise error when invalid config name was specified")
except Exception as e:
    print("TEST 7: PASS - (Correctly throws Exception: {})".format(e))   
    
    
# TEST 8 - Exception when schema doesn't include a key included in params
try:
    parse_cfg("DEBUG",cfg_name = "test4.config")
    print("TEST 8: FAIL- does not raise error when schema is missing parameter")
except KeyError as e:
    print("TEST 8: PASS - (Correctly throws Exception: {})".format(e))   


# TEST 9 - UserWarning when no schema is given in config
with warnings.catch_warnings(record = True) as w:
    cfg = parse_cfg("DEBUG",cfg_name = "test5.config")
    if w[-1].category == UserWarning:
        print("TEST 9: PASS - (Correctly throws UserWarning when no schema is given in config)")
    else:
        print("TEST 9: FAIL - does not raise UserWarning when no schema is given in config")    
    
    
# TEST 10 - Exception when item is not of schema-enforced type
try:
    parse_cfg("DEBUG",cfg_name = "test6.config")
    print("TEST 10: FAIL- does not raise  Exception when item is not of schema-enforced type")
except Exception as e:
    print("TEST 10: PASS - (Correctly throws Exception: {})".format(e))

# TEST 11 - No exception with schema-checking disabled
try:
    parse_cfg("DEBUG",cfg_name = "test6.config",SCHEMA = False)
    parse_cfg("DEBUG",cfg_name = "test3.config",SCHEMA = False)
    parse_cfg("DEBUG",cfg_name = "test4.config",SCHEMA = False)
    print("TEST 11: PASS - Does not raise Exception when schema-checking is disabled")
except Exception as e:
    print("TEST 11: FAIL - (Incorrectly throws Exception: {})".format(e))   
    