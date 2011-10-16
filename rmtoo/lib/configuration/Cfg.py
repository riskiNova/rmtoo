'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
 The Configuration Class hold values from the different configuration
 sources, i.e. configuration class, JSON configuration objects and the
 command line.
 
 History: this is a new implementation of the old Configuration 
 and command line parameter handling. 
   
 (c) 2011 by flonatel GmhH & Co. KG

 For licensing details see COPYING
'''
import json

from types import StringType, DictType
from rmtoo.lib.configuration.CfgEx import CfgEx
from rmtoo.lib.configuration.CmdLineParams import CmdLineParams
from rmtoo.lib.configuration.Utils import Utils

class Cfg:
    '''
    Configuration Class

    Stores all the values from different sources into one data container
    which is a dictionary.

    Has some special access methods like get_value("key.subkey.subsubkey")
    to simplify configuration access.
    '''

    def __init__(self):
        '''Constructs an empty configuration
           This can be filled later on with the different merge
           methods.'''
        self.config = {}

    @staticmethod
    def new_by_json_str(jstr):
        '''Creates a new Cfg object with the contents of the given
           string.  The string must be a valid JSON structure.
           This is a static factory method.'''
        config = Cfg()
        config.merge_json_str(jstr)
        return config

    def merge_json_str(self, jstr):
        '''Adds all the values from the given JSON string to
           the existing configuration.'''
        print("STR [%s]" % jstr)
        jdict = json.loads(jstr)
        if type(jdict) != DictType:
            raise CfgEx("Given JSON string encodes no dictionary.")
        self.merge_dictionary(jdict)

    def merge_dictionary(self, ldict):
        '''Merges the contents of the local dictionary into the 
           existing one.
           If a value already exists, it is overwritten'''
        Utils.internal_merge_dictionary(self.config, ldict)

    def merge_cmd_line_params(self, args):
        '''Merges the command line arguments into the 
           existing configuration.'''
        ldicts = CmdLineParams.create_dicts(args)

        TOTALER UNSINN:
        HIER MUSS IN JEDEM LDICT IN configuration.json NACHGESEHEN
        WERDEN UND JSON ANGEWANT WERDEN
        WEITERHIN MUSS NOCH IN configuration.deprecated.config_file
        DAS FILE GEPARSED WERDEN.

        VIELLEICHT IST ES VIEL EINFACHER ZWEI RÜCKGABEWERTE ZU ERHALTEN
        EINEN ALS DICT (FÜR DAS ALTE) UND EINEN ALS LISTE VON JSON
        BESCHREIBUNGEN FÜR DAS NEUE.

        for ldict in ldicts:
            print("Processing ldict [%s]" % ldict)
            if ldict == None:
                continue
            if type(ldict) == StringType and ldict.startswith("file://"):
                self.merge_json_file(ldict)
            elif type(ldict) == StringType and ldict.startswith("json:"):
                self.merge_json_str(ldict)
            else:
                assert(type(ldict) == DictType)
                self.merge_dictionary(ldict)

    @staticmethod
    def internal_parse_key_string(key):
        '''Parses the given string and splits it up for using with
           the configuration dictionary'''
        return key.split('.')

    @staticmethod
    def internal_get_value(key, ldict):
        '''Returns the key from the given dictionary.
           If this is not the last part of the key, this method
           is called recursively.'''
        assert(type(ldict) == DictType)
        assert(len(key) > 0)
        if key[0] not in ldict:
            raise CfgEx("(Sub-)Key [%s] not found." % key[0])
        val = ldict[key[0]]
        # No more keys to go for.
        if len(key) == 1:
            return val
        if type(val) != DictType:
            raise CfgEx("(Sub-)Type of configuration for key [%s] not a "
                        "dictionary " % key[0])
        return Cfg.internal_get_value(key[1:], val)

    def get_value(self, key):
        '''Returns the value of the given key.
           If key is not found a CfgEx is thrown.'''
        # If the type is a string, this must first be parsed.
        if type(key) == StringType:
            key = self.internal_parse_key_string(key)
        return Cfg.internal_get_value(key, self.config)

