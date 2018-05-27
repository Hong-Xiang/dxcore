import logging


class SimpleInMemoryBackend:
    def __init__(self):
        self.messages = []

    def format(self, level, message):
        def level_name(level):
            if level == logging.INFO:
                return 'INFO'
            raise ValueError("Unknown level.")

        return '[{}] {}'.format(level_name(level), message)

    def info(self, message):
        self.messages.append(self.format(logging.INFO, message))

    def content(self):
        return '\n'.join(self.messages)

    def __len__(self):
        return len(self.messages)