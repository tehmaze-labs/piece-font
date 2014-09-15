#!/usr/bin/env python2

from PIL import Image, ImageDraw
import struct


PSF1_MAGIC   = bytearray('\x36\x04')
PSF1_HEADER  = '<2sbb'
PSF1_MODE512 = 0x01

PSF2_MAGIC   = bytearray('\x72\xb5\x4a\x86')
PSF2_HEADER  = '<4sIIIIIII'


class Glyph(object):
    def __init__(self, size, data):
        self.size = size
        self.data = bytearray(data)

        self.x, self.y = self.size

        self.image = Image.new('1', self.size)
        for y in range(self.y):
            for x in range(self.x):
                if self.data[y] & (0x80 >> (x & 7)):
                    self.image.putpixel((x, y), 255)

    def __str__(self):
        output = []
        for y in range(self.y):
            for x in range(self.x):
                b = self.data[y] & (0x80 >> (x & 7))
                output.append('#' if b else ' ')
            output.append('\n')
        return ''.join(output)

    def paste(self, target, x, y):
        target.paste(self.image, (x, y, x + self.x, y + self.y))


class PSF(object):
    def __init__(self, filename):
        self.data = file(filename).read()

        if bytearray(self.data[:len(PSF1_MAGIC)]) == PSF1_MAGIC:
            self.parse_psf1()
        elif bytearray(self.data[:len(PSF2_MAGIC)]) == PSF2_MAGIC:
            self.parse_psf2()
        else:
            raise TypeError('{}: not a valid PSF file'.format(filename))

    def __getitem__(self, i):
        offset = self.glyphs_offset + (i * self.char_bytes)
        return Glyph(
            (self.char_width, self.char_height),
            self.data[offset:offset + self.char_bytes],
        )

    def __iter__(self):
        return iter([self[x] for x in range(len(self))])

    def __len__(self):
        return self.length

    def parse_psf1(self):
        self.version = 1
        self.magic, self.mode, self.charsize = struct.unpack(
            PSF1_HEADER,
            self.data[:struct.calcsize(PSF1_HEADER)],
        )

        self.char_width    = 8
        self.char_height   = self.charsize
        self.char_bytes    = self.char_width * self.char_height
        self.glyphs_offset = struct.calcsize(PSF1_HEADER)
        self.length        = [256, 512][self.mode & PSF1_MODE512]

    def parse_psf2(self):
        self.version = 2
        self.magic, self.version, self.headersize, self.flags, self.length, \
            self.charsize, self.char_height, self.char_width = struct.unpack(
            PSF2_HEADER,
            self.data[:struct.calcsize(PSF2_HEADER)],
        )

        self.char_bytes    = self.charsize
        self.glyphs_offset = self.headersize
