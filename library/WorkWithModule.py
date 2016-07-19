import os


class WorkWithModule():

    """
    @description: This class allows you to call external modules. If a call
    for an external module is detected by the parser then this class check
    the module's config file before extracting modules's parameter from the
    text you have pronounced
    """

    def __init__(self, module_name, text, linker, plus, PID):
        self.pid = PID

        try:
            sentence = text.lower()

            if sentence.count(linker) > 0:
                param = (sentence.split(linker, 1)[1])

                # we check whether the user wants to turn '' into +
                if plus == '1':
                    param = param.replace(' ', '+')
                # command that will be executed
                parent_dir = os.path.dirname(os.path.abspath(__file__)).strip(
                    'library')
                module_dir = os.path.join(parent_dir, 'modules')
                execute = 'python3 ' + module_dir + '/' + module_name + ' ' + param
                os.system(execute)
            else:
                message = "you didn't say the linking word"
                os.system(
                    'echo "' + message + '" > /tmp/mama/mama_error_' + self.pid)

        except IOError:
            message = 'args file missing'
            os.system('echo "'+message+'" > /tmp/mama/mama_error_'+self.pid)
            sys.exit(1)
