# Messages logger


class messages_handling():
    '''Class containing classification function working with logger class,
       Will return success and error definitions codes'''

    def success_codes(self, code):
        '''Switcher with all success codes'''
        switcher = {
            1: "[OS] Windows OS version detected successfully.",
            20: "[SYSTEM] Directory Created.",
            21: "[SYSTEM] Config file was successfully created.",
            22: "[SYSTEM] Config file already exists.",
            23: "[SYSTEM] Creating Read Configuration file attempt.",
            24: "[SYSTEM] Configuration successfully read.",
            25: "[SYSTEM] Config file create section initialized.",
            26: "[SYSTEM] Writing Default config values.",
            27: "[SYSTEM] Writing Api config values.",
            28: "[SYSTEM] Creating resources directory.",
            29: "[SYSTEM] Creating url_blocked template file.",
            30: "[VT] credentials successfully read.",
            31: "[VT] website and API are alive.",
            32: "[VT] healthcheck success.",
            33: "[VT] set http request.",
            34: "[VT] get http response succeeded.",
            40: "[SQL] SQL Initialization Started.",
            41: "[SQL] DB file exists.",
            42: "[SQL] Started DB Tests.",
            43: "[SQL] Passed DB file Tests.",
            44: "[SQL] Creating DB file.",
            45: "[SQL] Trying to create First DB connection.",
            46: "[SQL] Connection to DB was successfully made.",
            47: "[SQL] Test DB was successfully passed.",
            48: "[SQL] Launch DB create architecture.",
            50: "[SERVER] Server started successfully.",
            60: "[SQL Repair] DB repair started.",
            61: "[SQL Repair] DB repair for urls initiated after found missing.",
            62: "[SQL Repair] DB repair for whitelist initiated after found missing.",
            63: "[SQL Repair] DB repair for blacklist initiated after found missing.",
            69: "[SQL Repair] DB repair finished successfully."
        }
        return "[{:<3s}]".format("OK") + switcher.get(code, "No success code Exists for code: [{}].".format(code))

    def error_codes(self, code):
        '''Swticher with all error codes'''
        switcher = {
            0: "[OS] Wrong OS detected, please init on windows",
            120: "[SYSTEM] Error creating directory.",
            121: "[SYSTEM] Error creating Config file.",
            122: "[SYSTEM] Error reading the Configuration file.",
            128: "[SYSTEM] creating resources directory.",
            129: "[SYSTEM] Failed creating url_blocked template file.",
            # May never occur
            130: "[VT] Error with reading the Configuration file, data returned is False.",
            131: "[VT] VirusTotal is down or API not functional at the moment.",
            132: "[VT] VirusTotal healthcheck failed.",
            134: "[VT] Error getting VirusTotal http request.",
            140: "[SQL] SQL initialization failed.",
            141: "[SQL] DB file does not exist.",
            144: "[SQL] Error creating DB file.",
            146: "[SQL] DB connection failed.",
            147: "[SQL] Test DB failed, creating repairDB.",
            150: "[SERVER] Server failed to start.",
            169: "[SQL Repair] DB repair failed."
        }
        return "[{:<3s}]".format("ERR") + switcher.get(code, "No error code Exists for code: [{}].".format(code))

    def vt_codes(self, code):
        '''Swticher with all error codes'''
        switcher = {
            90: "[DETECTED] Detected malicious URL request *********"
        }
        return "[{:<3s}]".format("VT") + switcher.get(code, "No error code Exists for code: [{}].".format(code))

    def classify(self, flag, code, data=''):
        '''Function to classify what logging flag we have, [OK] or [ERR]'''
        if(flag == 2):
            return (self.vt_codes(code))
        elif(flag == 1):
            return (self.success_codes(code))
        elif(flag == 0):
            return (self.error_codes(code)) + ' [Exception data]: {}.'.format(data)
