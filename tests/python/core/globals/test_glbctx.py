from dxl.core.globals import GlobalContext


def test_set_and_get():
    class C(GlobalContext):
        pass

    C.set(1)
    assert C.get() == 1
    C.clear()


def test_clear():
    class C(GlobalContext):
        pass

    C.set(1)
    C.clear()
    assert C.get() is None


def test_clear_with_no_context():
    class C(GlobalContext):
        pass

    C.clear()
