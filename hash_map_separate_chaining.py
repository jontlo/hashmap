# Name: Jonathan Louangrath
# OSU Email: louangrj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hashmap Implementation
# Due Date: 9 August 2022 (two free days used)
# Description: This program uses a dynamic array to store a hash table.
# It resolves collisions by chaining through singly linked list.
# Functions include put, get, remove, contains_key, clear, empty_buckets,
# resize_table, table_load, get_keys, and find_mode.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def change_size(self, size: int) -> None:
        """Change size of hash map"""
        self._size += size

    def get_buckets(self) -> DynamicArray:
        """Getter method for dynamic array
        :return: DynamicArray object for buckets"""
        return self._buckets

    def get_hash(self, key: str) -> int:
        """Hash a key
        :param key: string of key to hash
        :return: int of index"""
        return self._hash_function(key)

    def get_linked_list(self, key: str) -> LinkedList:
        """Get linked list at key
        :param key: string of key to hash
        :param return: LinkedList object at that index"""

        index = self.get_hash(key) % self.get_buckets().length()
        return self.get_buckets().get_at_index(index)

    def put(self, key: str, value: object) -> None:
        """
        Update key/value pair in hash map
        :param key: key of new element
        :param value: value of new element
        """

        # Initialize array size and index
        array_size = self.get_buckets().length()
        index = self.get_hash(key) % array_size

        # Get linked list object at that dynamic array index
        linked_list = self.get_buckets().get_at_index(index)
        # Find if value already exists at that key
        if linked_list.contains(key) is not None:
            # Replace value
            linked_list.contains(key).value = value
            return

        # If key is not in hash map, add new key/value pair
        else:
            linked_list.insert(key, value)
            self.change_size(1)

    def empty_buckets(self) -> int:
        """
        Return number of empty buckets in hash table
        :return: int of empty buckets
        """

        # Initialize array size and return variable
        array_size = self.get_buckets().length()
        empty = 0

        # Iterate through dynamic array
        # If linked list length is 0, increment return variable
        for x in range(array_size):
            if self.get_buckets().get_at_index(x).length() == 0:
                empty += 1

        return empty

    def table_load(self) -> float:
        """
        Return current hash table factor
        :return: float of hash table factor
        """

        # Initialize hash map size and dynamic array size
        hash_size = self.get_size()
        array_size = self.get_buckets().length()

        return hash_size / array_size

    def clear(self) -> None:
        """
        Clear contents of hash map without changing capacity
        """
        # Initialize array size
        array_size = self.get_buckets().length()

        # Iterate through dynamic array. Check if there are non-empty linked lists
        for x in range(array_size):
            linked_list_length = self.get_buckets().get_at_index(x).length()
            if linked_list_length != 0:
                # Decrement size and clear linked list
                self.change_size(-1 * linked_list_length)
                self.get_buckets().set_at_index(x, LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity of hash table
        :param new_capacity: int of new hash table capacity
        """

        # Check if new_capacity is less than 1
        if new_capacity < 1:
            return

        # Check if new_capacity is prime
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # Create new dynamic array with desired capacity
        resized_array = DynamicArray()
        for x in range(new_capacity):
            resized_array.append(LinkedList())

        # Populate new dynamic array with items
        array_length = self.get_buckets().length()

        for x in range(array_length):
            linked_list = self.get_buckets().get_at_index(x)
            if linked_list.length() != 0:

                # Rehash hash table links
                for node in linked_list:
                    key = node.key
                    index = self.get_hash(key) % resized_array.length()

                    # Insert node into rehashed key index
                    resized_array.get_at_index(index).insert(key, node.value)

        # Reassign hashmap's data
        self._buckets = resized_array
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        Return value associated with key
        :param key: key to find value
        :return: key's value
        """

        # Get linked list at index
        linked_list = self.get_linked_list(key)

        # If key matches, return the element's value
        for link in linked_list:
            if link.key == key:
                return link.value

        # If key not in hash map, return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Return True if key is in hash map, otherwise return False
        :param key: key to find
        :return: bool whether key is present
        """

        # Get linked list at index
        linked_list = self.get_linked_list(key)

        # If key matches, return True
        for link in linked_list:
            if link.key == key:
                return True

        # If key not in hash map, return False
        return False

    def remove(self, key: str) -> None:
        """
        Remove given key and value from hash map
        :param key: key of element to remove
        """

        # Get linked list at index
        linked_list = self.get_linked_list(key)

        # If key matches, remove
        for link in linked_list:
            if link.key == key:
                linked_list.remove(key)

                # Decrement hash map size
                self.change_size(-1)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return Dynamic Array where each index has a tuple of pair stored there
        :return: dynamic array object
        """

        # Create keys and values array
        keys_and_values = DynamicArray()

        # Check if nodes exist at each index
        for x in range(self.get_buckets().length()):

            # If the linked list is non-empty, append each key and value to new dynamic array
            if self.get_buckets().get_at_index(x).length != 0:
                linked_list = self.get_buckets().get_at_index(x)
                for link in linked_list:
                    keys_and_values.append((link.key, link.value))

        # Return new dynamic array
        return keys_and_values


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Find mode in dynamic array
    :param da: dynamic array to find mode(s)
    :return: tuple consisting of (dynamic array with mode, int with its frequency)
    """

    # Initialize length of dynamic array and create new HashMap
    length = da.length()
    map = HashMap(length // 2)

    # Iterate through dynamic array
    for ele in range(length):

        # Get hash map index of each dynamic array element
        index = map.get_hash(da[ele]) % map.get_buckets().length()

        # Check if element is already logged
        if map.get_buckets().get_at_index(index).length() != 0:
            linked_list = map.get_buckets().get_at_index(index)

            # Check if another key has the same index
            # If so, create new node with that element's value as 1
            if linked_list.contains(da[ele]) is None:
                map.put(da[ele], 1)

            # If key is already logged, increase frequency (value) by 1
            else:
                freq = linked_list.contains(da[ele]).value + 1
                map.put(da[ele], freq)

        # If element is unique, create new node with that element's frequency (value) as 1
        else:
            map.put(da[ele], 1)

    # Find keys and values
    keys_and_values = map.get_keys_and_values()
    keys_values_length = keys_and_values.length()

    # Create new dynamic array for modes
    modes = DynamicArray()
    mode_freq = 1

    # Iterate through keys_and_values dynamic array
    for pair in range(keys_values_length):

        # Compare each element's frequency to existing mode_freq
        if keys_and_values.get_at_index(pair)[1] > mode_freq:
            mode_freq = keys_and_values.get_at_index(pair)[1]

            # Clear current modes array and append new mode
            modes = DynamicArray()
            modes.append(keys_and_values.get_at_index(pair)[0])

        # Append competing modes
        elif keys_and_values.get_at_index(pair)[1] == mode_freq:
            modes.append(keys_and_values.get_at_index(pair)[0])

    return modes, mode_freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
