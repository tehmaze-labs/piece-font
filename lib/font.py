#!/usr/bin/env python2


import os
import struct
import unicodedata
import yaml
from PIL import Image, ImageDraw, ImageOps


TEXT = [
    u'Zelda might fix the job growth',
    u'plans very quickly on Monday.,',
    u'A QUICK MOVEMENT OF THE ENEMY ',
    u'WILL JEOPARDIZE SIX GUNBOATS!?',
]
UNITEXT = [
    map(lambda c: unicodedata.name(c), row)
    for row in TEXT
]

PSF2_MAGIC       = bytearray('\x72\xb5\x4a\x86')
PSF2_HEADER      = '<IIIIIII'
PSF2_HAS_UNICODE = 0x01
PSF2_FLAGS       = 0x00000000
PSF2_VERSION     = 0x00000000
PSF2_SEPARATOR   = 0xff
PSF2_STARTSEQ    = 0xfe


class Glyph(object):
    def __init__(self, bitmap='', **kwargs):
        self.character = kwargs['unicode']
        self.bitmap_raw = bitmap

    def __str__(self):
        return self.character

    def load(self):
        self.bitmap_bin = bytearray()
        self.char_width = 0
        self.char_height = 0
        for row in self.bitmap_raw.splitlines():
            row = row.replace('#', '1').replace('-', '0')
            self.bitmap_bin.append(int(row, 2))
            self.char_width = max(self.char_width, len(row))
            self.char_height += 1

    def to_bin(self):
        return str(self.bitmap_bin)

    def to_hex(self):
        return self.to_bin().encode('hex')

    def to_image(self):
        size = (self.char_width, self.char_height)
        image = Image.new('RGB', size)
        if self.character is None:
            draw = ImageDraw.Draw(image)
            draw.rectangle(((0, 0), size), fill=(0x80, 0x00, 0x00))

        for y, row in enumerate(self.bitmap_raw.splitlines()):
            for x, pixel in enumerate(row):
                if pixel == '#':
                    image.putpixel((x, y), (0xff, 0xff, 0xff))

        return image

    def to_unicode(self):
        if self.character is None:
            return None
        elif self.character == 'NULL' or self.character == 0:
            return '\x00'
        else:
            try:
                return unicodedata.lookup(self.character)
            except TypeError:
                raise ValueError("Can't decode unicode name: {!r}"
                                 .format(self.character))


class Font(object):
    def __init__(self, filename, load_glyphs=True):
        self.filename = filename
        self.parse(load_glyphs=load_glyphs)

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    def __getitem__(self, index):
        if isinstance(index, (int, long)):
            try:
                return self.glyphs[index]
            except IndexError:
                return None
        else:
            for glyph in self:
                if glyph is None:
                    continue
                if glyph.character == index:
                    return glyph

    def __iter__(self):
        return iter(self.glyphs)

    def __len__(self):
        return len(self.glyphs)

    def __str__(self):
        return self.info['name']

    @property
    def char_width(self):
        return self.info.get('size', [8, 16])[0]

    @property
    def char_height(self):
        return self.info.get('size', [8, 16])[1]

    def parse(self, load_glyphs=True):
        with open(self.filename) as handle:
            font = yaml.load(handle)
            self.info = font['font']
            self.info['name'] = os.path.splitext(
                os.path.basename(self.filename)
            )[0]
            self.glyphs = [None] * len(font['characters'])
            for index, info in font['characters'].iteritems():
                if isinstance(index, basestring):
                    index = int(index, 16)
                while index >= len(self.glyphs):
                    self.glyphs.append(None)

                self.glyphs[index] = Glyph(**info)
                if load_glyphs:
                    self.glyphs[index].load()

    def to_bin(self):
        packed = bytearray()
        for i in range(len(self)):
            glyph = self.glyphs[i]
            if glyph is None:
                packed.extend('\x00' * self.char_height)
            else:
                packed.extend(glyph.to_bin())

        return str(packed)

    def to_hex(self):
        packed = []
        packed.append('# Width: {}'.format(self.char_width))
        packed.append('# Height: {}'.format(self.char_height))
        for i in range(len(self)):
            glyph = self.glyphs[i]
            if glyph is None:
                packed.append('%04x:%s' % (i, '00' * self.char_height))
            else:
                packed.append('%04x:%s' % (i, glyph.to_hex()))

        return '\n'.join(packed)

    def to_image(self, scale=1, columns=0, text=False):
        if text:
            size = (
                self.char_width * len(TEXT[0]),
                self.char_height * len(TEXT),
            )
            image = Image.new('RGB', size)
            for y in range(len(TEXT)):
                for x in range(len(TEXT[y])):
                    c = UNITEXT[y][x]
                    if self[c] is None:
                        continue
                    image.paste(
                        self[c].to_image(),
                        (
                            (x + 0) * self.char_width,
                            (y + 0) * self.char_height,
                            (x + 1) * self.char_width,
                            (y + 1) * self.char_height,
                        )
                    )

            alpha = []
            for data in image.getdata():
                if data[0] > 192:
                    alpha.append((0, 0, 0, 255))
                else:
                    alpha.append((255, 255, 255, 0))
            image = Image.new('RGBA', size)
            image.putdata(alpha)

        elif columns > 0:
            per_row = columns
            rows = (len(self) + (columns - 1)) // columns

            size = (
                self.char_width * columns,
                self.char_height * rows,
            )
            image = Image.new('RGB', size)

            for y in range(rows):
                for x in range(columns):
                    o = (y * columns) + x
                    if self[o] is None:
                        continue

                    image.paste(
                        self[o].to_image(),
                        (
                            (x + 0) * self.char_width,
                            (y + 0) * self.char_height,
                            (x + 1) * self.char_width,
                            (y + 1) * self.char_height,
                        )
                    )

        else:
            size = (
                self.char_width * len(self),
                self.char_height,
            )
            image = Image.new('RGB', size)

            for x, glyph in enumerate(self):
                if glyph is None:
                    continue

                glyph = glyph.to_image()
                xx = x * self.char_width
                yy = 0
                image.paste(
                    glyph,
                    (
                        xx,
                        yy,
                        xx + glyph.size[0],
                        yy + glyph.size[1],
                    )
                )

        if scale:
            size = (
                image.size[0] * scale,
                image.size[1] * scale,
            )
            image = image.resize(size, Image.NEAREST)

        return image

    def to_psf(self):
        packed = bytearray()
        packed.extend(PSF2_MAGIC)
        packed.extend(struct.pack(
            PSF2_HEADER,
            PSF2_VERSION,
            struct.calcsize(PSF2_HEADER) + len(PSF2_MAGIC),
            PSF2_HAS_UNICODE,
            len(self),
            self.char_height * ((self.char_width + 7) // 8),
            self.char_height,
            self.char_width,
        ))

        packed.extend(self.to_bin())
        for index, glyph in enumerate(self):
            if glyph is None or glyph.to_unicode() is None:
                packed.append('\x00')
            else:
                packed.extend(glyph.to_unicode().encode('utf-8'))
            packed.append(PSF2_SEPARATOR)

        return str(packed)
