import os
from datetime import datetime
from re import findall
from uuid import getnode
from socket import gethostname, gethostbyname
from platform import platform, architecture, processor
import configparser
import logger.logger as logger


class MainConfig():
    logger_instance = logger.logger()

    # Join paths to getcwd working environment
    def is_file_exist(self, file_name, __working__directory__):
        '''Following function will check whther file exists in working directory
        Can handle list or Str '''
        file_path = self.join_paths(file_name, __working__directory__)
        if(os.path.isfile(file_path)):
            return True
        return False

    def join_paths(self, path_to_join, config_dir):
        '''Function to join working directory path to file or list, 
        Note that last element in the list is a file ['a','b','c.txt']'''
        path_after_join = config_dir
        try:
            if(isinstance(path_to_join, list)):
                for element in path_to_join:
                    path_after_join = os.path.join(path_after_join, element)
            elif(isinstance(path_to_join, str)):
                path_after_join = os.path.join(
                    path_after_join, path_to_join)  # Will just join one line
            else:
                # Error please insert list or str
                pass
        except Exception as e:
            print(e)
            pass
        return path_after_join

    def create_configuration(self, __config__file__, __Version__, __config__path__, __working__directory__):
        '''The following function is aimed for creating a finger print
        Configuration file for initialized process that ran, this will be
        used in the long run for data science and identification through big networks'''
        if(not self.is_file_exist(__config__file__, __working__directory__)):
            # Configuration does not exist, creating config
            self.logger_instance.write_log(25, 1)
            config = configparser.ConfigParser()
            config.sections()
            # USER_CONFIG
            self.logger_instance.write_log(26, 1)
            config['DEFAULT'] = {'ComputerName':  gethostname(),  # Host-Name
                                 # Socket IP
                                 'Ipaddress': gethostbyname(gethostname()),
                                 'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date + Clock without micros
                                 'App_Version': __Version__,  # Predefined version in globals
                                 'Mac': ':'.join(findall('..', '%012x' % getnode())),
                                 'Win_ver': platform(),
                                 'CPU': processor()}  # Returns in 48bits, we could also do hex(uuid.getnode())
            # API_CONFIG
            self.logger_instance.write_log(27, 1)
            config['API'] = {}
            # API Key needs to be protected somehow with server etc..
            config['API']['api_key'] = '2a24732ab41b71b3a66db6e18595c189a37920067ce9e6f4095ebc5241062121'
            config['API']['api_url'] = 'https://www.virustotal.com/api/v3/'

            try:
                with open(__config__path__, 'w') as configfile:
                    config.write(configfile)
                    self.logger_instance.write_log(21, 1)  # success code
            except Exception as e:
                self.logger_instance.write_log(121, 0, e)  # data err code

        else:
            # Configuration exists, we will load the data via main
            self.logger_instance.write_log(22, 1)  # success code
            pass

    def read_configuration(self, __working__directory__, __config__file__):
        '''This function will read api_url and api_key from our 
        previously created configuration'''
        config = configparser.ConfigParser()
        config.sections()
        try:  # Trying to read the configuration file
            self.logger_instance.write_log(23, 1)  # Attempt
            config.read(os.path.join(__working__directory__, __config__file__))
            self.logger_instance.write_log(24, 1)  # Read
            api_url = config['API']['api_url']  # Set Vars
            api_key = config['API']['api_key']
            self.logger_instance.write_log(30, 1)
        except Exception as e:
            self.logger_instance.write_log(122, 0, e)
            return (False, False)
        return api_url, api_key
