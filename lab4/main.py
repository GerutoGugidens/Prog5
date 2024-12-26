class FibonacciList:
    def __init__(self, lst):
        from gen_fib import fib_coroutine, my_genn, my_genn_1, fib_elem_gen
        my_gen = fib_coroutine(my_genn_1)
        gen = my_gen()
        self.lst = lst
        self.index = 0
        x = gen.send(max(lst))
        print(x)
        self.fibonacci_numbers = set(x)


    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.lst):
            value = self.lst[self.index]
            self.index += 1
            if value in self.fibonacci_numbers:
                return value
        raise StopIteration


# Пример использования
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 2, 13, 14, 15, 55, 55, 43, 56]
fib_lst = FibonacciList(lst)
new_lst = [x for x in fib_lst]
print(new_lst)
