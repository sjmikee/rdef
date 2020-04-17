from datetime import datetime
from socket import gethostname, gethostbyname
import os
import messages

# Globals
__logger__dir__ = 'logs'
__logger__file__ = 'logger.rdef'
__Version__ = '0.1'
__working__directory__ = os.getcwd()


class logger():
    '''The following class will create logger and insert releavant data to any event happened in the runtime'''
    message_instance = messages.messages_handling()
    timestamp = datetime.now().strftime("%Y-%m-%d")
    logger_file_today = timestamp + '.' + __logger__file__
    loggerfullpath = os.path.join(
        __working__directory__, __logger__dir__, logger_file_today)
    logger_directory_path = os.path.join(
        __working__directory__, __logger__dir__)

    def create_logger(self):
        '''This function will create logger directory and file
        Logs will be organized by date (%y %m %d)'''
        # Creating here the file
        if(not os.path.isdir(self.logger_directory_path)):
            try:
                os.mkdir(self.logger_directory_path)
            except OSError as dir_err:
                # We have an OS error, means logger was not created
                print(dir_err)

        if(not os.path.isfile(self.loggerfullpath)):
            try:
                with open(self.loggerfullpath, 'w') as f:
                    f.write("######################\n")
                    f.writelines('Logger File was created successfully by Hostname: {},\nVersion: {},\non: {}\n'.format(
                        gethostname(), __Version__, self.timestamp))
                    f.writelines("######################\n")
            except OSError as file_err:
                print(file_err)

    def write_log(self, code, flag, exception_data=''):
        '''The following functions inserts data to the log file that was previously created via init globals'''
        try:
            with open(self.loggerfullpath, 'a+') as log_file:
                log_file.write(
                    '[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + '[{:<3d}]'.format(code))
                log_file.write(self.message_instance.classify(
                    flag, code, exception_data) + '\n')
                log_file.close()
        except Exception as e:
            print(e)
