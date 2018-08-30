__all__ = ['GlobalContext', 'clear_all']

globals = {}


class GlobalContext:
    @classmethod
    def set(cls, o):
        globals[cls] = o

    @classmethod
    def get(cls):
        return globals.get(cls)

    @classmethod
    def clear(cls):
        if cls in globals:
            del globals[cls]


def clear_all():
    globals.clear()
