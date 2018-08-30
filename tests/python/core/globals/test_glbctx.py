from dxl.core.globals import GlobalContext


def test_basic():
    class C(GlobalContext):
        pass

    C.set(1)
    assert C.get() == 1
    C.clear()
    assert C.get() is None
