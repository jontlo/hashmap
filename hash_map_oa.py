# Name: Jonathan Louangrath
# OSU Email: louangrj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hashmap Implementation
# Due Date: 9 August 2022 (two free days used)
# Description: This program uses a dynamic array to store a hash table.
# It resolves collisions by chaining through open addressing and quadratic probing.
# Functions include put, get, remove, contains_key, clear,
# empty_buckets, resize_table, table_load, and get_keys.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

    def get_array(self) -> DynamicArray:
        """Get the hash map
        :return: DynamicArray of hash map"""

        return self._buckets

    def get_hash(self, key: str) -> int:
        """Run the hash function
        :param key: key to hash
        :return: int of new index"""

        return self._hash_function(key)

    def probe(self, arr: DynamicArray, hash_index: int, key: str, value: object) -> bool:
        """Probe for an empty spot in the array
        :param arr: DynamicArray to probe
        :param hash_index: first index calculated with hash
        :param key: key of inserted element
        :param value: value of inserted element
        :return: True if inserted, False if replaced or otherwise"""

        # If key already exists in hash map, replace with new value
        if arr.get_at_index(hash_index) is not None and arr.get_at_index(hash_index).key == key:
            tombstone = arr.get_at_index(hash_index).is_tombstone
            arr.set_at_index(hash_index, HashEntry(key, value))
            if tombstone is True:
                return True
            return False

        # If initial index is empty, insert element there
        elif arr.get_at_index(hash_index) is None:
            arr.set_at_index(hash_index, HashEntry(key, value))
            return True

        # Otherwise, probe for index
        else:
            number_buckets = arr.length()

            for j in range(1, number_buckets):
                probed_index = (hash_index + (j * j)) % number_buckets

                # Check if replacing at key which already exists
                if arr.get_at_index(probed_index) is not None and arr.get_at_index(probed_index).key == key:
                    tombstone = arr.get_at_index(probed_index).is_tombstone
                    arr.set_at_index(probed_index, HashEntry(key, value))
                    if tombstone is True:
                        return True
                    return False

                # Check if insertion at empty index is possible
                elif arr.get_at_index(probed_index) is None:
                    arr.set_at_index(probed_index, HashEntry(key, value))
                    return True

                # Check if insertion at tombstone is possible
                elif arr.get_at_index(probed_index).is_tombstone is True:
                    arr.set_at_index(probed_index, HashEntry(key, value))
                    return True

            # Otherwise, return False
            return False

    def put(self, key: str, value: object) -> None:
        """
        Update key/value pair in hash map
        :param key: key to update
        :param value: value to update
        """

        # Check load factor more than or equal to 0.5
        if self.table_load() >= 0.5:
            # Resize table to double current size
            length = self.get_array().length()
            self.resize_table(length * 2)

        # Get hash for element's key. Compute hash index. Probe and insert.
        hashed = self.get_hash(key)
        hash_index = hashed % self.get_array().length()
        inserted = self.probe(self.get_array(), hash_index, key, value)

        # Check if element was inserted or swapped. Increment size if inserted.
        if inserted is True:
            self._size += 1
            return
        return

    def table_load(self) -> float:
        """
        Return current hash table load factor
        :return: float of load factor
        """

        elements = self.get_size()
        buckets = self.get_array().length()

        return elements / buckets

    def empty_buckets(self) -> int:
        """
        Return number of empty buckets
        :return: int of empty buckets
        """

        # Initialize array size and return variable
        array_size = self.get_array().length()
        empty = 0

        # Iterate through dynamic array
        # If array element is None, increment return variable
        for x in range(array_size):
            if self.get_array().get_at_index(x) is None:
                empty += 1

        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity of hash table and rehash if necessary
        :param new_capacity: int of new capacity
        """
        # remember to rehash non-deleted entries into new table

        # Check if new_capacity is less than number of elements
        if new_capacity < self.get_size():
            return

        # Check if new_capacity is prime. If not, reassign it next prime
        if self._is_prime(new_capacity) is not True:
            new_capacity = self._next_prime(new_capacity)

        # Create new dynamic array with desired capacity
        resized_array = DynamicArray()

        # Populate new dynamic array with None
        for _ in range(new_capacity):
            resized_array.append(None)

        # Store old buckets. Reassign buckets, capacity, and size
        old_data = self._buckets
        self._buckets = resized_array
        self._capacity = new_capacity
        self._size = 0

        # Begin rehashing elements from old array
        array_length = old_data.length()
        for x in range(array_length):
            old_element = old_data.get_at_index(x)

            # Put the old element in the new array
            if old_element is not None and old_element.is_tombstone is False:
                self.put(old_element.key, old_element.value)

    def get(self, key: str) -> object:
        """
        Return value associated with key
        :param key: key to find value
        :return: object of value found
        """

        # Get hash of key. Find hash index. Store initial element
        hashed = self.get_hash(key)
        hash_index = hashed % self.get_array().length()
        initial_element = self.get_array().get_at_index(hash_index)

        # Check if element exists
        if initial_element is None:
            return None

        # Check if element is tombstone
        elif initial_element is not None and initial_element.is_tombstone is True:
            return None

        # Check if element exists and key matches
        elif initial_element is not None and initial_element.key == key:
            if initial_element.is_tombstone is False:
                return initial_element.value

        # Otherwise, continue probing until key is found
        else:
            number_buckets = self.get_array().length()

            for j in range(1, number_buckets):
                probed_index = (hash_index + (j * j)) % number_buckets
                probed_element = self.get_array().get_at_index(probed_index)

                # Check if key exists at probed element and is tombstone
                if probed_element is not None and probed_element.key == key:
                    if probed_element.is_tombstone is False:
                        return probed_element.value
                elif probed_element is not None and probed_element.is_tombstone is True:
                    return None
            return None

    def contains_key(self, key: str) -> bool:
        """
        Return True if key is in hash map. Otherwise return False
        :param key: key to search for
        :return: bool if key is present
        """

        # Check if map is empty
        if self.get_array().length() == 0:
            return False

        # Get hash of key. Find hash index. Store initial element
        hashed = self.get_hash(key)
        hash_index = hashed % self.get_array().length()
        initial_element = self.get_array().get_at_index(hash_index)

        # Check if element exists and key matches
        if initial_element is not None and initial_element.key == key:
            return True

        # Otherwise, continue probing until key is found
        else:
            number_buckets = self.get_array().length()

            for j in range(1, number_buckets):
                probed_index = (hash_index + (j * j)) % number_buckets
                probed_element = self.get_array().get_at_index(probed_index)

                # Check if key exists at probed element
                if probed_element is not None and probed_element.key == key:
                    return True

            # Otherwise, the key was not found
            return False

    def remove(self, key: str) -> None:
        """
        Removes given key and value from hash map
        :param key: key of element to remove
        """

        # Get hash of key. Find hash index. Store initial element
        hashed = self.get_hash(key)
        hash_index = hashed % self.get_array().length()
        initial_element = self.get_array().get_at_index(hash_index)

        # Check if initial_element does not exist
        if initial_element is None:
            return

        # Check if initial_element exists and key matches. If so, remove element
        if initial_element is not None and initial_element.key == key:
            if initial_element.is_tombstone is False:
                initial_element.is_tombstone = True
                self._size -= 1
            return

        # Otherwise, continue probing until key is found
        else:
            number_buckets = self.get_array().length()

            for j in range(1, number_buckets):
                probed_index = (hash_index + (j * j)) % number_buckets
                probed_element = self.get_array().get_at_index(probed_index)

                # Check if probed_element does not exist
                if probed_element is None:
                    return

                # If key found, remove element at probed_index
                elif probed_element is not None and probed_element.key == key:
                    if probed_element.is_tombstone is False:
                        self.get_array().get_at_index(probed_index).is_tombstone = True
                        self._size -= 1
                    return

    def clear(self) -> None:
        """
        Clear contents of hash map. Does not change capacity.
        """

        array_length = self.get_array().length()

        # Set None for each element
        for x in range(array_length):
            self.get_array().set_at_index(x, None)

        # Decrement size
        self._size -= self.get_size()

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return DynamicArray where each index is a tuple of a key/value pair
        :return: DynamicArray object of key/value tuples
        """

        array_length = self.get_array().length()

        # Create return array
        keys_values = DynamicArray()

        # For each element in hash map, append tuple of its key and value to keys_values
        for x in range(array_length):
            element = self.get_array().get_at_index(x)
            if element is not None and element.is_tombstone is False:
                keys_values.append((element.key, element.value))

        return keys_values


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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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

    print("\nPDF - get example 1.5")
    print("-------------------")
    print(m.get('key235'))

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
