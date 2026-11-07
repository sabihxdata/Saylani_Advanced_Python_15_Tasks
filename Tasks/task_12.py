'''Task 12 | Custom Iterable Range Toolkit
Concepts: Iterators, generators, dunder methods
Problem: Create a ReversibleRange(start,stop,step) class supporting iteration, reversed iteration, len(), and membership tests without constructing a list.
Requirements: Match Python range stop-exclusive semantics for positive and negative nonzero steps. Implement __iter__, __reversed__, __len__, and __contains__.
Sample / expected behavior: ReversibleRange(2,11,3) -> [2,5,8]; reversed -> [8,5,2]; 5 in object -> True. '''



class ReversibleRange:
    def __init__(self, start, stop, step=1):
        if not all(isinstance(value, int) and not isinstance(value, bool)
                   for value in (start, stop, step)):
            raise TypeError("Start, stop, and step must be integers")

        if step == 0:
            raise ValueError("Step cannot be zero")

        self.start = start
        self.stop = stop
        self.step = step

    def __len__(self):
        if self.step > 0:
            if self.start >= self.stop:
                return 0
            return (self.stop - self.start - 1) // self.step + 1

        else:
            if self.start <= self.stop:
                return 0
            return (self.start - self.stop - 1) // (-self.step) + 1

    def __iter__(self):
        current = self.start

        if self.step > 0:
            while current < self.stop:
                yield current
                current += self.step

        else:
            while current > self.stop:
                yield current
                current += self.step

    def __reversed__(self):
        length = len(self)

        if length == 0:
            return iter(())

        last_value = self.start + (length - 1) * self.step
        current = last_value

        def reverse_generator():
            nonlocal current

            for _ in range(length):
                yield current
                current -= self.step

        return reverse_generator()

    def __contains__(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            return False

        if len(self) == 0:
            return False

        difference = value - self.start

        if difference % self.step != 0:
            return False

        index = difference // self.step

        return 0 <= index < len(self)



print("TEST 1: NORMAL ITERATION")
numbers = ReversibleRange(1, 10, 2)
print(list(numbers))



print("\nTEST 2: REVERSE ITERATION")
print(list(reversed(numbers)))



print("\nTEST 3: LENGTH")
print("Length:", len(numbers))


print("\nTEST 4: MEMBERSHIP")
print("5 in range:", 5 in numbers)
print("6 in range:", 6 in numbers)
print("10 in range:", 10 in numbers)



print("\nTEST 5: NEGATIVE STEP")
descending = ReversibleRange(10, 0, -2)
print("Normal:", list(descending))
print("Reverse:", list(reversed(descending)))
print("Length:", len(descending))



print("\nTEST 6: EMPTY RANGE")
empty = ReversibleRange(5, 5, 1)
print("Values:", list(empty))
print("Length:", len(empty))



print("\nTEST 7: ERROR HANDLING")
try:
    invalid = ReversibleRange(1, 10, 0)
except ValueError as error:
    print(error)
