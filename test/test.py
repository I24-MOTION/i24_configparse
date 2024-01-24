import time
import os, sys
import warnings
from src.i24_configparse import parse_cfg

# set os environment config path
cwd = os.getcwd()
#config_path = os.path.join(cwd,cfg)
config_path = os.path.join(cwd, "test_config1") + os.pathsep + os.path.join(cwd, "test_config2")
os.environ["USER_CONFIG_DIRECTORY"] = config_path # note that this may not affect processes globally
os.environ["TEST_CONFIG_SECTION"] = "DEBUG"

print("USER_CONFIG_DIRECTORY = {}".format(os.environ["USER_CONFIG_DIRECTORY"]))

#%% Input Tests

# TEST 1 - Exception thrown when no cfg_name or obj are passed
try:
    parse_cfg("TEST_CONFIG_SECTION")
    print("TEST  1: FAIL- does not correctly handle case with no cfg_name or obj input")
except Exception as e:
    print("TEST  1: PASS - (Correctly throws Exception: {})".format(e))
    
    
# TEST 2 - Exception when  cfg_path is specified incorrectly
try:
    parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test_badpath.config")
    print("TEST  2: FAIL- Does not raise error when invalid config name was specified")
except FileNotFoundError as e:
    print("TEST  2: PASS - (Correctly throws Exception: {})".format(e))    
except Exception as e:
    print("TEST  2: FAIL - Incorrectly throws Exception: {}".format(e))
 

# TEST 3 - UserWarning when no DEFAULT env is specified in config
with warnings.catch_warnings(record = True) as w:
    cfg = parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test2.config")
    if w[-1].category == UserWarning:
        print("TEST  3: PASS - (Correctly throws UserWarning when no DEFAULT env is specified in config)")
    else:
        print("TEST  3: FAIL - Does not raise UserWarning when no DEFAULT env is specified")   
 
# TEST 4 - UserWarning when invalid environment is specified
with warnings.catch_warnings(record = True) as w:
    cfg = parse_cfg("DEBUG_MISSPELL",cfg_name = "test1.config")
    if w[-1].category == UserWarning:
        print("TEST  4: PASS - (Correctly throws UserWarning and switched to DEFAULT when invalid env is specified)")
    else:
        print("TEST  4: FAIL - Does not raise UserWarning when invalid env was specified")
        
    
#%% Correct Behavior Tests


# TEST 5 -  verify correct behavior with default paramas object
start = time.time()
cfg = parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test1.config")
elapsed = time.time() - start
try:
    cfg.a,cfg.b,cfg.c,cfg.d,cfg.e
    print("TEST  5: PASS - (Took {:.5f}s to check schema for 5 attributes)".format(elapsed))
except AttributeError:
    print("TEST  5: FAIL - Param object doesn't have all attributes specified in config")


# TEST 6 - verify correct behavior with input object
class TestObj():
    def __init__(self):
        pass

obj = parse_cfg("TEST_CONFIG_SECTION",obj = TestObj())
try:
    obj.a,obj.b,obj.c,obj.d,obj.e
    print("TEST  6: PASS")
except AttributeError:
    print("TEST  6: FAIL- param object doesn't have all attributes specified in config")
    
    

#%% Schema Tests

# TEST 7 - Exception when invalid type is specified in schema
try:
    parse_cfg("TEST_CONFIG_SECTION",cfg_name = "testtt3.config")
    print("TEST  7: FAIL- does not raise error when invalid config name was specified")
except Exception as e:
    print("TEST  7: PASS - (Correctly throws Exception: {})".format(e))   
    
    
# TEST 8 - Exception when schema doesn't include a key included in params
try:
    parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test4.config")
    print("TEST  8: FAIL- does not raise error when schema is missing parameter")
except KeyError as e:
    print("TEST  8: PASS - (Correctly throws Exception: {})".format(e))   


# TEST 9 - UserWarning when no schema is given in config
with warnings.catch_warnings(record = True) as w:
    cfg = parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test5.config")
    if len(w) > 0 and w[-1].category == UserWarning:
        print("TEST  9: PASS - (Correctly throws UserWarning when no schema is given in config)")
    else:
        print("TEST  9: FAIL - does not raise UserWarning when no schema is given in config")    
    
    
# TEST 10 - Exception when item is not of schema-enforced type
try:
    parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test6.config")
    print("TEST 10: FAIL- does not raise  Exception when item is not of schema-enforced type")
except Exception as e:
    print("TEST 10: PASS - (Correctly throws Exception: {})".format(e))

# TEST 11 - No exception with schema-checking disabled
try:
    #parse_cfg("DEBUG",cfg_name = "test6.config",SCHEMA = False)
    #parse_cfg("DEBUG",cfg_name = "test3.config",SCHEMA = False)
    parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test10.config",SCHEMA = False)
    print("TEST 11: PASS - (Does not raise Exception when schema-checking is disabled)")
except Exception as e:
    print("TEST 11: FAIL - Incorrectly throws Exception: {}".format(e))   
    
    
#%% Additional tests
    
# TEST 12 - Check that error is thrown when schema-specified params are not included
try:
    parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test7.config")
    print("TEST 12: FAIL- does not raise error when parameters are missing from env")
except Exception as e:
    print("TEST 12: PASS - (Correctly throws Exception: {})".format(e))     
    
    
# TEST 13 - Check that no error is thrown when schema-specified params with optional tag are not included
try:
    parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test8.config")
    print("TEST 13: PASS - (No error thrown when optional schema parameters not specified in env)")   
except Exception as e:
    print("TEST 13: FAIL - Raises error when optional parameters are missing from env: {}".format(e))
    
    
# TEST 14 - Check that types are correctly cast
params = parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test9.config")
try:
    assert type(params.a) == int and params.a == 1, "a"
    assert type(params.b) == str and params.b == "Test String 1", "b"
    assert type(params.c) == float and params.c == 1.0, "c"
    assert type(params.d) == bool and params.d, "d"
    assert type(params.e) == float and params.e == 1.405
    assert type(params.g) == bool and not params.g, "g"
    print("TEST 14: PASS - (Types are correctly cast)")
except AssertionError as e:
    print("TEST 14: FAIL - types are not correctly cast: {}".format(e))


# TEST 15 - Check dictionary return type
d = parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test8.config",return_type = "dict")
if type(d) == dict:
    print("TEST 15: PASS - (correctly returns dictionary when specified)")   
else:
    print("TEST 15: FAIL - fails to return dictionary when specified")   


# TEST 16 - check list parsing
try:
    params = parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test11.config")
    print("TEST 16: PASS - (List parameters parsed correctly)")   
    assert len(params.a) == 5 and params.a[0] == 1, "a"
    assert len(params.c) == 3 and not params.c[1] , "c"
except Exception as e:
    print("TEST 16: FAIL - List parameters parsed incorrectly: {}".format(e))
    
    
# TEST 17 - correctly loads from secondary locations
try:
    cfg = parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test17.config")
    cfg.a,cfg.b,cfg.c,cfg.d,cfg.e
    print("TEST 17: PASS - (Correctly loads from secondary locations)")
except Exception as e:
    print("TEST 17: FAIL - Can not load files from secondary locations")
    
# TEST 18 - check warning for superseded configurations
with warnings.catch_warnings(record = True) as w:
    cfg = parse_cfg("TEST_CONFIG_SECTION",cfg_name = "test18.config")
    if len(w) > 0 and w[-1].category == UserWarning:
        print("TEST 18: PASS - (Correctly throws UserWarning when multiple files are available: {})".format(w[-1].message))
    else:
        print("TEST 18: FAIL - does not raise UserWarning when multiple files are available")  
        
        
# TEST 21 - Exception thrown when no cfg_name or obj are passed
try:
    del os.environ["USER_CONFIG_DIRECTORY"]
    parse_cfg("TEST_CONFIG_SECTION",cfg_name="test1.config")
    print("TEST 21: FAIL - does not correctly handle missing environment variable USER_CONFIG_DIRECTORY")
except Exception as e:
    print("TEST 21: PASS - (Correctly throws Exception: {})".format(e))
