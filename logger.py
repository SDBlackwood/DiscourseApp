
class Logger():

    @staticmethod
    def log(a, b):
        return str(a) + str(b)


class TestLogger(Logger):

    @staticmethod
    def p(func_name, to_convert):
        print ("{}: {}".format(func_name, to_convert))
        print ('')

class ApplicationLogger(Logger):
    
    @staticmethod
    def debug(string):
        print (string)