# -*- coding: utf-8 -*-

"""
This is the equivalent of what you find in morton.py except that these
functions do not use lookup tables to do the work and that you can
(de)interleave 3 integers together.

In theory, these functions could work regardless of the size of the
integers you pass in. This should come later, altough you should expect
them to be slower.
"""

from __future__ import division

from math import ceil


def part1by1(n):
    """
    Inserts one 0 bit between each bit in `n`.

    n: 16-bit integer
    """
    # This algorithm gradually spreads the bits of ‘n’ until there is
    # one 0 bit between every bit of the original integer.
    # Let n equal "················FEDCBA9876543210" where hex digits
    # are the index positions of the input integer and "·"s are 0s.
    # n will take the values
    # "········FEDCBA98········76543210",
    # "····FEDC····BA98····7654····3210",
    # "··FE··DC··BA··98··76··54··32··10",
    # "·F·E·D·C·B·A·9·8·7·6·5·4·3·2·1·0",
    # and this value is returned.
    n &= 0x0000FFFF

    n = (n | (n << 8)) & 0x00FF00FF
    n = (n | (n << 4)) & 0x0F0F0F0F
    n = (n | (n << 2)) & 0x33333333
    n = (n | (n << 1)) & 0x55555555

    return n


def part1by2(n):
    """
    Inserts two 0 bits between each bit in `n`.

    n: 16-bit integer
    """
    n &= 0x000003FFF

    n = (n ^ (n << 16)) & 0xFF0000FF
    n = (n ^ (n << 8)) & 0x0300F00F
    n = (n ^ (n << 4)) & 0x030C30C3
    n = (n ^ (n << 2)) & 0x09249249

    return n


def part1by3(n):
    """
    Inserts three 0 bits between each bit in ‘n’.

    n: 16-bit integer
    """
    n &= 0xFFFF

    n = (n ^ (n << 24)) & 0x000000FF000000FF
    n = (n ^ (n << 12)) & 0x000F000F000F000F
    n = (n ^ (n << 6)) & 0x0303030303030303
    n = (n ^ (n << 3)) & 0x1111111111111111

    return n


def unpart1by1(n):
    """
    Gets every other bits from `n`.

    n: 32-bit integer
    """
    n &= 0x55555555

    n = (n ^ (n >> 1)) & 0x33333333
    n = (n ^ (n >> 2)) & 0x0F0F0F0F
    n = (n ^ (n >> 4)) & 0x00FF00FF
    n = (n ^ (n >> 8)) & 0x0000FFFF

    return n


def unpart1by2(n):
    """
    Gets every third bits from `n`.

    n: 32-bit integer
    """
    n &= 0x09249249

    n = (n ^ (n >> 2)) & 0x030C30C3
    n = (n ^ (n >> 4)) & 0x0300F00F
    n = (n ^ (n >> 8)) & 0xFF0000FF
    n = (n ^ (n >> 16)) & 0x000003FF

    return n


def unpart1by3(n):
    """
    Gets every fourth bit from ‘n’.

    n: 64-bit integer
    """
    n &= 0x1111111111111111

    n = (n ^ (n >> 3)) & 0x0303030303030303
    n = (n ^ (n >> 6)) & 0x000F000F000F000F
    n = (n ^ (n >> 12)) & 0x000000FF000000FF
    n = (n ^ (n >> 24)) & 0x000000000000FFFF

    return n


def interleave2(x, y):
    """
    Interleaves two integers.
    """
    max_bits = max(x.bit_length(), y.bit_length())
    iterations = int(ceil(max_bits / 16))

    ret = 0
    for i in range(iterations):
        interleaved = part1by1(x & 0xFFFF) | \
                      (part1by1(y & 0xFFFF) << 1)
        ret |= (interleaved << (32 * i))

        x = x >> 16
        y = y >> 16
    return ret


def deinterleave2(n):
    """
    Deinterleaves an integer into two integers.
    """
    iterations = int(ceil(n.bit_length() / 32))

    x = y = 0
    for i in range(iterations):
        x |= unpart1by1(n) << (16 * i)
        y |= unpart1by1(n >> 1) << (16 * i)
        n = n >> 32

    return x, y


def interleave3(x, y, z):
    """
    Interleaves three integers.
    """
    return part1by2(x) | (part1by2(y) << 1) | (part1by2(z) << 2)


def deinterleave3(n):
    """
    Deinterleaves an integer into three integers.
    """
    return unpart1by2(n), unpart1by2(n >> 1), unpart1by2(n >> 2)


def interleave4(w, x, y, z):
    """
    Interleaves four integers.
    """
    # http://www.forceflow.be/2013/10/07/morton-encodingdecoding-through-bit-interleaving-implementations/
    # http://graphics.stanford.edu/~seander/bithacks.html#InterleaveTableObvious
    # https://en.wikipedia.org/wiki/Z-order_curve
    # https://stackoverflow.com/questions/1024754/how-to-compute-a-3d-morton-number-interleave-the-bits-of-3-ints
    return part1by3(w) | (part1by3(x) << 1) | (part1by3(y) << 2) | (part1by3(z) << 3)


def deinterleave4(n):
    """
    Deinterleaves an integer into four integers.
    """
    return unpart1by3(n), unpart1by3(n >> 1), unpart1by3(n >> 2), unpart1by3(n >> 3)
