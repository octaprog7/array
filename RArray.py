#!/usr/bin/python

from functools import reduce


class RArray:
    """
    1D..3D array based on list
    """

    def _convert_coord(self, coord) -> tuple:
        """
        converts coordinates from multidimensional to linear
        return tuple
        """
        crd: tuple = self._get_coord(coord)
        if len(crd) != len(self.get_dimension()):
            raise ValueError
        for c, D in zip(crd, self.get_dimension()):
            if c >= D:
                raise StopIteration

        f = len(crd)

        if f == 1:
            return crd[0]
        a = crd[0] + crd[1] * self.dim[0]
        if f == 2:
            return a
        if f == 3:
            return a + crd[2] * self.dim[0] * self.dim[1]

    def _get_len(self) -> int:
        """returns the number of array elements"""
        return reduce(lambda a, b: a * b, self.dim)

    def _fill(self, value) -> None:
        """Fills sequence it with initial values"""
        delta = self._get_len() - len(self.array)
        for _ in range(delta):
            self.array.append(None)

        bseq = isinstance(value, (str, tuple, list))
        for index in range(len(self.array)):
            if bseq:
                self.array[index] = value[index]
            else:
                self.array[index] = value

    @staticmethod
    def _check_coord(coord):
        """checks coordinates for correctness"""
        if not isinstance(coord, (int, tuple)):
            raise ValueError

    def _get_coord(self, coord) -> tuple:
        """returns tuple coordinates"""
        self._check_coord(coord)
        if isinstance(coord, int):
            return (coord,)
        if isinstance(coord, tuple):
            if 1 <= len(coord) <= 3:
                return coord
            else:
                raise ValueError

    def __init__(self, **kwargs):
        """
        creates an array.
        named arguments:
        dimension - array dimension 1D-3D (12, (10, 5), (10, 15, 20)) - integer or tuple
        source - a one-dimensional sequence that will be copied to the array (string, tuple, list)
        initial_value - the value by which all elements of the array will be initialized (not taken into account
        if the source parameter is specified)
        """
        self.array = list()

        if "dimension" in kwargs:
            self.dim = self._get_coord(kwargs["dimension"])

            if "initial_value" in kwargs:
                self._fill(kwargs["initial_value"])
            else:
                self._fill(None)
            return

        if "source" in kwargs:
            seq = kwargs["source"]
            self.dim = (len(seq),)
            self._fill(seq)

    def __getitem__(self, index: int) -> object:
        """return item by index"""
        offset = self._convert_coord(index)
        return self.array[offset]

    def __setitem__(self, index: int, value: object):
        offset = self._convert_coord(index)
        self.array[offset] = value

    def get_dimension(self) -> tuple:
        """
        return dimension of array (tuple)
        """
        return self.dim

    def __len__(self) -> int:
        """returns the number of array elements (int)"""
        return self._get_len()

    def __repr__(self):
        return "RArray at {}. Dimensions: {}. Length: {}".format(hex(id(self)), self.dim, self._get_len())


class SeqIter:
    """Iterator for any sequence"""
    def __init__(self, sequence):
        self.seq = sequence
        self.offset = 0

    def __next__(self):
        if self.offset >= len(self.seq):
            raise StopIteration  # finalize iteration
        val = self.seq[self.offset]
        self.offset += 1
        return val


class GetSeqIterator:
    """"Proxy for iteration protocol"""
    def __init__(self, sequence):
        # print("GetSeqIterator.__init__\tcall")
        self.seq = sequence

    def __iter__(self):
        # print("GetSeqIterator.__iter__\tcall")
        return SeqIter(self.seq)


if __name__ == "__main__":
    X, Y = 10, 5
    RA = RArray(dimension=(X, Y))
    print(RA)
    # fill array
    for x in range(X):
        for y in range(Y):
            RA[x, y] = x + y * X

    for y in range(Y):
        print("")
        for x in range(X):
            print(RA[x, y], end=" ")
    print("\n")

    RB = RArray(source="Hello World")
    print(RB)
    # iteration via by index
    for i in range(len(RB)):
        print(RB[i], end=" ")

    print("\n")
    GSI = GetSeqIterator(RB)
    # iteration by iteration protocol
    for x in GSI:
        print("")
        for y in GSI:
            print(x+y, end=" ")
