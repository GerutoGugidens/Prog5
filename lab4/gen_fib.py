import functools
from itertools import islice


def fib_elem_gen():
    """Генератор, возвращающий элементы ряда Фибоначчи"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def my_genn():
    """Сопрограмма для генерации ряда Фибоначчи."""
    while True:
        number_of_fib_elem = yield
        if number_of_fib_elem is None:
            continue
        if isinstance(number_of_fib_elem, str):
            raise TypeError("Кол-во элементов должно быть числом!")
        if number_of_fib_elem < 1:
            raise ValueError("Кол-во элементов должно быть больше 0.")
        print(f'Генерируем {number_of_fib_elem} элементов ряда Фибоначчи.')
        fib_gen = (x for x in islice(fib_elem_gen(), number_of_fib_elem))
        yield list(fib_gen)
def my_genn_1():
    """Сопрограмма для генерации ряда Фибоначчи."""
    while True:
        max_element = yield
        if max_element is None:
            continue
        if isinstance(max_element, str):
            raise TypeError("Число должно быть числом!")
        if max_element < 1:
            raise ValueError("Число должно быть больше 0.")
        print(f'Генерируем ряд Фибоначчи, макс. элемент которого >= {max_element}')
        fib_gen = []
        gen = fib_elem_gen()
        while True:
            x = next(gen)
            fib_gen.append(x)
            if x>=max_element: break
        max_element=None
        yield list(fib_gen)



def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen
    return inner


my_gen = fib_coroutine(my_genn)
gen = my_gen()
print(gen.send(21))
gen = my_gen()
print(gen.send(11))
