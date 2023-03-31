"""Math functions"""

from math import ceil
from random import randint


class list:
    def __init__(self, item: list, show: bool = False, ignore_errors: bool = False, obj_ret: bool = False, error: list = []):
        if isinstance(item, list):
            if ignore_errors:
                pass
            else:
                raise ValueError("item must be a list")
        self.error = error
        self.item = item
        self.show = show
        self.ignore_errors = ignore_errors
        self.obj_ret = obj_ret

    def get_ratio(self):
        """
        The get_ratio function takes a list of two numbers, multiplies the first number by an increasing integer starting at 1,
        and compares the difference between that product and the original number to 0.0000001. If this condition is met,
        the function returns a list with two integers: [original_number * multiplier for multiplier in range(0, 99999), 1].
        If not met before 99999 iterations (99999^2 = 99999999), then it returns [0, 0].

        :param self: Refer to the object instance
        :return: A list of two integers: [original_number * multiplier for multiplier in range(0, 99999), 1]
        """
        if isinstance(self.item, list):
            if self.ignore_errors:
                return "item must be a list"
            else:
                raise ValueError("item must be a list")
        for i in range(1, 99999):
            if float(ceil(float(self.item[0]*i)) - float(self.item[0]*i)) < 0.0000001:
                ratio = [int(self.item[0]*i), int(self.item[1]*i)]
                break
        else:
            if self.show:
                print([0, 0])
            return [0, 0]
        if self.show:
            print(ratio)
        self.item = ratio
        if self.obj_ret:
            return self
        return ratio

    def divide(self):
        """
        The divide function divides the first item in a list by all other items in that list.
            If there are no items, it returns 0.

            Parameters:
                self (object): The object being passed to the function.

            Returns: 
                result (int or float): The result of dividing all numbers together.

        :param self: Refer to the object itself
        :return: The result of the division
        """
        if isinstance(self.item, list):
            if not isinstance(self.item, tuple):
                pass
            elif self.ignore_errors:
                return "item must be a list"
            else:
                raise ValueError("item must be a list")
        if len(self.item) == 0:
            self.item = 0
            if self.ignore_errors:
                self.error.append('No object found; ignoring')
            else:
                raise ValueError("No object found")
            if self.show:
                print(0)
            if self.obj_ret:
                return self
            return 0
        result = self.item[0]
        for i in range(1, len(self.item)):
            result = result/self.item[i]
        self.item = result
        if self.show:
            print(result)
        if self.obj_ret:
            return self
        return result


def get_id(long: int = 10) -> int:
    id = ''
    for i in range(long):
        id += str(randint(0, 9))
    return id
