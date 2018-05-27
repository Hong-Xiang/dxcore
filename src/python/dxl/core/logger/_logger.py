class LoggerAspect:
    def info(self):
        pass


class BeforeAspect:
    def __init__(self, logger):
        self.logger = logger


class Logger:
    def __init__(self, name):
        pass

    def before(self):
        pass
