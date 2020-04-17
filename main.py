#! C:\Users\Kobi\AppData\Local\Programs\Python\Python38-32\python.exe
from platform import architecture
import sys
import requests
import base64
import os
import json
import argparse
import server.proxy as proxy
import server.vt_response_parser as vt_response_parser
import config.main_config as main_config
import logger.logger as logger

# Testing
###########################################
# Globals and definistions
# -> Code composers:
__Authors__ = 'Kobi, Michael, Aviv'
# -> Application:
__Version__ = '0.1'
__config__file__ = 'config.rdef'
__working__directory__ = os.getcwd()
__config__path__ = os.path.join(__working__directory__, __config__file__)
# -> Config data:
api_url = ''
api_key = ''
# -> Logger isntance
logger_instance = logger.logger()
logger_instance.create_logger()
# -> Vt response parser instance
vt_response_parser_instance = vt_response_parser.vt_response_parser()
# -> Proxy instance


def healthcheck(link, wait_for_completion=False):
    '''Function to set first connection to VirusTotal via V3 API,
       Validating via the last_analysis json attribute returned by the server.'''
    url = base64.urlsafe_b64encode(link.encode()).decode().strip("=")
    # Returning URL_Object#
    url_last = api_url + "urls/{}".format(url)
    parameters = {"x-apikey": api_key}
    logger_instance.write_log(33, 1)
    try:
        response = requests.get(url_last, headers=parameters)
        logger_instance.write_log(34, 1)
        if(response.status_code == 200):
            # Logging VT is alive
            logger_instance.write_log(31, 1)
            responseData = json.loads(response.text)
            # Virus total alive
            harmless, malicious, suspicious, timeout, undetected = vt_response_parser_instance.last_analysis_stats(
                responseData)
            if (isinstance(harmless, int)):
                logger_instance.write_log(32, 1)
            else:
                logger_instance.write_log(132, 0, '')
        else:
            # Virus total not alive
            logger_instance.write_log(131, 0, '')
    except Exception as e:
        logger_instance.write_log(134, 0, e)


def parse_args(self, argv=sys.argv[1:]):
    # Parsing arguments
    parser = argparse.ArgumentParser(
        description='Real time VirusTotal defender By Kobi Binner and Mike Korenskiy')
    parser.add_argument('--port', dest='port', type=int, default=9999,
                        help='serve server on specified port (default: 9999)')
    args = parser.parse_args(argv)
    return args


def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    '''Function to init all project'''
    if ('WindowsPE' in architecture()):  # Windows OS was detected
        logger_instance.write_log(1, 1)
        config = main_config.MainConfig()
        config.create_configuration(
            __config__file__, __Version__, __config__path__, __working__directory__)
        global api_url  # Accessing global identifiers
        global api_key
        try:
            # Trying to read configuration VT credentials
            api_url, api_key = config.read_configuration(
                __working__directory__, __config__file__)
            if ((api_url and api_key) == False):  # Double check
                print("There has been a problem setting VT credentials.")
                logger_instance.write_log(130, 0, '')
                from ctypes import windll
                # Gui ctypes
                windll.user32.MessageBoxW(
                    0, "Please check API credentials", "Error reading VirusTotal credentials", 1)
                exit()  # Exit
            else:
                # -> Virustotal_healthcheck for first request
                healthcheck('http://www.google.co.il')
        except Exception as e:
            logger_instance.write_log(122, 0, e)
    else:  # Linux/Mac load different program
        # Error no windows exit()
        logger_instance.write_log(0, 0)

    # Creating proxy instance
    proxy_server = proxy.Proxy()
    proxy_server.start_proxy(args.port, api_url, api_key)


if __name__ == "__main__":
    main()
