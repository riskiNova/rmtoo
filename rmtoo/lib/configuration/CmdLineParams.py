'''
 rmtoo
   Free and Open Source Requirements Management Tool

 Command line parameter handling.

 (c) 2011,2017 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''
from __future__ import unicode_literals

import distutils

from optparse import OptionParser

from rmtoo.lib.Encoding import Encoding


class CmdLineParams:
    '''Utility class for handling the old style command line
       parameters (like -f, -m and -c) as well as the new
       command line parameters.'''

    def __init__(self):
        '''Utility class with 'hidden' constructor'''
        assert False

    @staticmethod
    def initialize_parser():
        '''Initializases the command line parser.'''
        return OptionParser()

    @staticmethod
    def add_deprecated_parameters(parser):
        '''Add the deprecated parameters to the given option parser.'''
        parser.add_option("-f", "--file-config", dest="config_file",
                          help="Configuration file")
        parser.add_option("-m", "--modules-directory",
                          dest="modules_directory",
                          help="Directory with modules")
        parser.add_option("-c", "--create-makefile-dependencies",
                          dest="create_makefile_dependencies",
                          help="Create makefile dependencies")

    @staticmethod
    def add_deprecated_values(options):
        '''Add all the values to the dictionary which were specified
           with the help of the old and deprecated command line options.'''
        ldict = {}

        if options.config_file is not None:
            ldict['configuration'] \
                = {'deprecated':
                   {'config_file': Encoding.to_unicode(options.config_file)}}

        if options.modules_directory is not None:
            ldict['global'] \
                = {'modules': {'directories':
                               [Encoding.to_unicode(
                                   options.modules_directory)]}}
        else:
            # If there is no modules directory given, use the pyshared one.
            mod_dir = distutils.sysconfig.get_python_lib()
            ldict['global'] = {'modules':
                               {'directories':
                                [Encoding.to_unicode(mod_dir)]}}

        if options.create_makefile_dependencies is not None:
            ldict['actions'] \
                = {'create_makefile_dependencies':
                   Encoding.to_unicode(options.create_makefile_dependencies)}

        return ldict

    @staticmethod
    def add_parameters(parser):
        '''Add the command line parameters to the given parser.'''
        parser.add_option("-j", "--json", dest="json",
                          action="append",
                          help="JSON string or file which is merged into the "
                          "existing configuration. Can be specified multiple "
                          "times.")

    @staticmethod
    def add_values(options):
        '''Add all the new command line parameter values.'''
        if options.json is None:
            return {}

        jopts = []
        for jopt in options.json:
            ujopt = Encoding.to_unicode(jopt)
            if ujopt.startswith("file://") or ujopt.startswith("json:"):
                jopts.append(ujopt)
            else:
                jopts.append("json:" + ujopt)
        return {'configuration': {'json': jopts}}

    @staticmethod
    def add_args(args):
        '''Add the arguments to the configuration.'''
        if args is None or args == []:
            return {}
        return {'general': {'command_line_arguments': args}}

    @staticmethod
    def create_dicts(args):
        '''Creates a dictionary from all the command line parameters.'''
        parser = CmdLineParams.initialize_parser()
        CmdLineParams.add_deprecated_parameters(parser)
        CmdLineParams.add_parameters(parser)

        (options, args) = parser.parse_args(args=args)

        lresult = []
        lresult.append(CmdLineParams.add_args(args))
        lresult.append(CmdLineParams.add_deprecated_values(options))
        lresult.append(CmdLineParams.add_values(options))
        return lresult
