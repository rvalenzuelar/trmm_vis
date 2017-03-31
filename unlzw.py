# Source:
# Brandon Owen
# https://github.com/umeat/unlzw/blob/master/unlzw.py

def unlzw(data):
    # This function was adapted for Python from Mark Adler's C implementation
    # https://github.com/umeat/unlzw

    # Decompress compressed data generated by the Unix compress utility (LZW
    # compression, files with .Z suffix). Input can be given as any type which
    # can be 'converted' to a bytearray (e.g. string, or bytearray). Returns
    # decompressed data as string, or raises error.

    # Written by Brandon Owen, May 2016, brandon.owen@hotmail.com
    # Adapted from original work by Mark Adler - orginal copyright notice below

    # Copyright (C) 2014, 2015 Mark Adler
    # This software is provided 'as-is', without any express or implied
    # warranty.  In no event will the authors be held liable for any damages
    # arising from the use of this software.
    # Permission is granted to anyone to use this software for any purpose,
    # including commercial applications, and to alter it and redistribute it
    # freely, subject to the following restrictions:
    # 1. The origin of this software must not be misrepresented; you must not
    # claim that you wrote the original software. If you use this software
    # in a product, an acknowledgment in the product documentation would be
    # appreciated but is not required.
    # 2. Altered source versions must be plainly marked as such, and must not be
    # misrepresented as being the original software.
    # 3. This notice may not be removed or altered from any source distribution.
    # Mark Adler
    # madler@alumni.caltech.edu

    # Usage:
    #
    # f = open('file.Z', 'r')
    # compressed_data = f.read()
    # uncompressed_data = unlzw(compressed_data)


    # Convert input data stream to byte array, and get length of that array
    try:
        ba_in = bytearray(data)
    except ValueError:
        raise TypeError("Unable to convert inputted data to bytearray")

    inlen = len(ba_in)
    prefix = [None] * 65536  # index to LZW prefix string
    suffix = [None] * 65536  # one-character LZW suffix

    # Process header
    if inlen < 3:
        raise ValueError("Invalid Input: Length of input too short for processing")

    if (ba_in[0] != 0x1f) or (ba_in[1] != 0x9d):
        raise ValueError("Invalid Header Flags Byte: Incorrect magic bytes")

    flags = ba_in[2]
    if flags & 0x60:
        raise ValueError("Invalid Header Flags Byte: Flag byte contains invalid data")

    max_ = flags & 0x1f
    if (max_ < 9) or (max_ > 16):
        raise ValueError("Invalid Header Flags Byte: Max code size bits out of range")

    if (max_ == 9): max_ = 10  # 9 doesn't really mean 9
    flags &= 0x80  # true if block compressed

    # Clear table, start at nine bits per symbol
    bits = 9
    mask = 0x1ff
    end = 256 if flags else 255

    # Ensure stream is initially valid
    if inlen == 3: return 0  # zero-length input is permitted
    if inlen == 4:  # a partial code is not okay
        raise ValueError("Invalid Data: Stream ended in the middle of a code")

    # Set up: get the first 9-bit code, which is the first decompressed byte,
    # but don't create a table entry until the next code
    buf = ba_in[3]
    buf += ba_in[4] << 8
    final = prev = buf & mask  # code
    buf >>= bits
    left = 16 - bits
    if prev > 255:
        raise ValueError("Invalid Data: First code must be a literal")

    # We have output - allocate and set up an output buffer with first byte
    put = [final]

    # Decode codes
    mark = 3  # start of compressed data
    nxt = 5  # consumed five bytes so far
    while nxt < inlen:
        # If the table will be full after this, increment the code size
        if (end >= mask) and (bits < max_):
            # Flush unused input bits and bytes to next 8*bits bit boundary
            # (this is a vestigial aspect of the compressed data format
            # derived from an implementation that made use of a special VAX
            # machine instruction!)
            rem = (nxt - mark) % bits

            if (rem):
                rem = bits - rem
                if rem >= inlen - nxt:
                    break
                nxt += rem

            buf = 0
            left = 0

            # mark this new location for computing the next flush
            mark = nxt

            # increment the number of bits per symbol
            bits += 1
            mask <<= 1
            mask += 1

        # Get a code of bits bits
        buf += ba_in[nxt] << left
        nxt += 1
        left += 8
        if left < bits:
            if nxt == inlen:
                raise ValueError("Invalid Data: Stream ended in the middle of a code")
            buf += ba_in[nxt] << left
            nxt += 1
            left += 8
        code = buf & mask
        buf >>= bits
        left -= bits

        # process clear code (256)
        if (code == 256) and flags:
            # Flush unused input bits and bytes to next 8*bits bit boundary
            rem = (nxt - mark) % bits
            if rem:
                rem = bits - rem
                if rem > inlen - nxt:
                    break
                nxt += rem
            buf = 0
            left = 0

            # Mark this location for computing the next flush
            mark = nxt

            # Go back to nine bits per symbol
            bits = 9  # initialize bits and mask
            mask = 0x1ff
            end = 255  # empty table
            continue  # get next code

        # Process LZW code
        temp = code  # save the current code
        stack = []  # buffer for reversed match - empty stack

        # Special code to reuse last match
        if code > end:
            # Be picky on the allowed code here, and make sure that the
            # code we drop through (prev) will be a valid index so that
            # random input does not cause an exception
            if (code != end + 1) or (prev > end):
                raise ValueError("Invalid Data: Invalid code detected")
            stack.append(final)
            code = prev

        # Walk through linked list to generate output in reverse order
        while code >= 256:
            stack.append(suffix[code])
            code = prefix[code]

        stack.append(code)
        final = code

        # Link new table entry
        if end < mask:
            end += 1
            prefix[end] = prev
            suffix[end] = final

        # Set previous code for next iteration
        prev = temp

        # Write stack to output in forward order
        put += stack[::-1]

        # Return the decompressed data as string


    return bytes(bytearray(put))