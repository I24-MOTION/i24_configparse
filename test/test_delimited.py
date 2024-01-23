import time
import os, sys
import warnings
from src.i24_configparse import parse_delimited


# set os environment config path
cwd = os.getcwd()
cfg = "./config"
config_path = os.path.join(cwd,cfg)
os.environ["USER_CONFIG_DIRECTORY"] = config_path # note that this may not affect processes globally
#%% Input Tests
    
# Tests for single param output cases  
    
# TEST 0 -  verify correct behavior with default paramas object
try:
    par = parse_delimited("test1.list", 'b', 'B2')
    par.a, par.b, par.c, par.d
    print("TEST  0: PASS - Param object has all attributes specified in header")
except AttributeError:
    print("TEST  0: FAIL- Param object doesn't have all attributes specified in the header")
except Exception as e:
    print("TEST  0: FAIL - Incorrectly throws Exception: {}".format(e))

# TEST 1 -  verify correct type cast with the given schema
try:
    par = parse_delimited("test1.list", 'a', 0)
    assert type(par.a) == int, "type error for 'a'" 
    assert type(par.b) == str, "type error for 'b'"
    assert type(par.c) == bool, "type error for 'c'"
    assert type(par.d) == float, "type error for 'd'"
    print("TEST  1: PASS - Param object has proper types specified in the schema")
except Exception as e:
    print("TEST  1: FAIL - Incorrectly throws Exception: {}".format(e))        
    
# TEST 2 - Verify removal of the additional whitespaces
try:
    par = parse_delimited("test1.list", 'a', 2)
    assert par.b == 'B2', "Whitespaces not removed '{}'".format(par.b) 
    print("TEST  2: PASS - Whitespaces correctly removed")
except Exception as e:
    print("TEST  2: FAIL - Incorrectly behavior: {}".format(e)) 

# TEST 3 - Exception thrown when erroneous / non-existent key_name is passed
try:
    par = parse_delimited("test1.list", 'f', 'B2')
    print("TEST  3: FAIL- Does not correctly handle case when erroneous / non-existent key_name is passed")
except KeyError as e:
    print("TEST  3: PASS - Correctly throws Exception: {}".format(e))
except Exception as e:
    print("TEST  3: FAIL - Incorrectly throws Exception: {}".format(e))
    
# TEST 4 - Exception thrown when no matching key_value exists
try:
    par = parse_delimited("test1.list", 'b', 'B20')
    print("TEST  4: FAIL- Does not correctly handle case when no matching key_value exists")
except ValueError as e:
    print("TEST  4: PASS - Correctly throws Exception: {}".format(e))
except Exception as e:
    print("TEST  4: FAIL - Incorrectly throws Exception: {}".format(e))    
    
    
# TEST 5 - Exception thrown when the key_value and the schema type are mismatched
try:
    par = parse_delimited("test1.list", 'b', 2)
    print("TEST  5: FAIL- Does not correctly handle case when the key_value and the schema type are mismatched")
except KeyError as e:
    print("TEST  5: PASS - Correctly throws Exception: {}".format(e))
except Exception as e:
    print("TEST  5: FAIL - Incorrectly throws Exception: {}".format(e))    


# Tests for multiple param output cases    
    
# TEST 10 - verify correct behavior: dictionary should be returned
try:
    pars = parse_delimited("test1.list", 'b')
    assert type(pars) == dict, "Incorrect return type: {}".format(type(pars))    
    assert type(list(pars.keys())[0]) == str, "Incorrect key type for the dictionary"    
    print("TEST 10: PASS - Correctly returns a dictionary with the proper key type")
except Exception as e:
    print("TEST 10: FAIL - Incorrectly throws Exception / incorrect return value: {}".format(e))
    
# Tests for general errors
    
# TEST 20 - Exception thrown when the length of the header and the value list are mismatched
try:
    par = parse_delimited("test2.list", 'b', 'B2')
    print("TEST 20: FAIL- Does not correctly handle case when the length of parameters and values are mismatched")
except ValueError as e:
    print("TEST 20: PASS - Correctly throws Exception: {}".format(e))
except Exception as e:
    print("TEST 20: FAIL - Incorrectly throws Exception: {}".format(e))
    
# TEST 21 - Exception thrown when unknown datatype found in schema
try:
    pars = parse_delimited("test3.list", 'b')
    print("TEST 21: FAIL- Does not correctly handle case when unknown datatype found in schema")
except KeyError as e:
    print("TEST 21: PASS - Correctly throws Exception: {}".format(e))
except Exception as e:
    print("TEST 21: FAIL - Incorrectly throws Exception: {}".format(e))    
    
# TEST 22 - Exception thrown when schema is improperly formated (proper: "name=type", incorrect e.g.: "name", "name=", "name=type=")
try:
    pars = parse_delimited("test4.list", 'b')
    print("TEST 21: FAIL- Does not correctly handle case when schema is improperly formated")
except KeyError as e:
    print("TEST 21: PASS - Correctly throws Exception: {}".format(e))
except Exception as e:
    print("TEST 21: FAIL - Incorrectly throws Exception: {}".format(e))  
    
# TEST 23 - Boolean value handling: proper acceptance of "True", "true", "False", "false", ..
try:
    pars = parse_delimited("test1.list", 'a')    
    assert pars[0].c == False, " Row '{}' should be False".format(pars[0].b)
    assert pars[1].c == True,  " Row '{}' should be True".format(pars[1].b)
    assert pars[2].c == False, " Row '{}' should be False".format(pars[2].b)
    assert pars[3].c == True,  " Row '{}' should be True".format(pars[3].b)
    assert pars[4].c == False, " Row '{}' should be False".format(pars[4].b)
    assert pars[5].c == True,  " Row '{}' should be True".format(pars[5].b)
    assert pars[6].c == False, " Row '{}' should be False".format(pars[6].b)
    assert pars[7].c == True,  " Row '{}' should be True".format(pars[7].b)
    assert pars[8].c == False, " Row '{}' should be False".format(pars[8].b)
    assert pars[9].c == True,  " Row '{}' should be True".format(pars[9].b)
    print("TEST 21: PASS - Correctly handles boolean values")
except Exception as e:
    print("TEST 21: FAIL - Incorrectly handles boolean values: {}".format(e))
    
# TEST 24 - Exception thrown when erroneous list_name (filename) is passed
try:
    par = parse_delimited("test1-bad.list", 'b', 'B2')
    print("TEST 24: FAIL - Does not correctly handle case when erroneous list_name (filename) are passed")
except FileNotFoundError as e:
    print("TEST 24: PASS - Correctly throws Exception: {}".format(e))
except Exception as e:
    print("TEST 24: FAIL - Incorrectly throws Exception: {}".format(e))