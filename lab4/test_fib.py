import pytest

from gen_fib import fib_coroutine, my_genn, my_genn_1

def test_fib_1():
    my_gen = fib_coroutine(my_genn)
    gen = my_gen()
    assert gen.send(3) == [0, 1, 1], "Тривиальный случай n = 3, список [0, 1, 1]"


def test_fib_2():
    my_gen = fib_coroutine(my_genn)
    gen = my_gen()
    assert gen.send(5) == [0, 1, 1, 2, 3], "Пять первых членов ряда"

def test_fib_3():
    with pytest.raises(ValueError):
        my_gen = fib_coroutine(my_genn)
        gen = my_gen()
        gen.send(-1)

def test_fib_4():
    with pytest.raises(TypeError):
        my_gen = fib_coroutine(my_genn)
        gen = my_gen()
        gen.send("ы")

def test_fib_5():
    my_gen = fib_coroutine(my_genn_1)
    gen = my_gen()
    assert gen.send(52) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]