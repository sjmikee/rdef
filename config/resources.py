from main import __working__directory__
import os
import logger.logger as logger

# Logger instance
logger_instance = logger.logger()


class resources():
    __url__blocked__template = 'url_blocked.html'
    __resources__directory__ = 'resources'
    path = os.path.join(__working__directory__, __resources__directory__)
    url_blocked_path = os.path.join(path, __url__blocked__template)

    def resources_dir(self):
        if(not os.path.isdir(self.path)):
            try:
                logger_instance.write_log(28, 1)
                os.mkdir(self.path)
            except Exception as e:
                logger_instance.write_log(128, 0, e)

    def is_blocked_template(self):
        self.resources_dir()
        print(self.url_blocked_path)
        if(not os.path.isfile(self.url_blocked_path)):
            try:
                logger_instance.write_log(29, 1)
                with open(self.url_blocked_path, 'w+') as f:
                    f.writelines('''<html>
<head>
    <title>MALICIOUS URL BLOCKED</title>
</head>
<body>
    <center>
        <h1>********* BLOCKED *********<br></h1>
        <h3>Realtime VirusTotal defender has blocked a malicious url<br>You are safe</h3>
    </center>
</body>
</html>''')
            except Exception as e:
                logger_instance.write_log(129, 0, e)

    def resources_path(self):
        return self.path

    def url_blocked_file(self):
        return self.url_blocked_path


if __name__ == "__main__":
    r = resources()
    r.is_blocked_template()
