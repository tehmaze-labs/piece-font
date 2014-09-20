import os

env = Environment()
env.VariantDir('build', 'src')

build_bin = []
build_hex = []
build_psf = []
fonts_bin = Glob('src/bin/*.bin')
fonts_fnt = Glob('src/fnt/*.fnt')
fonts_hex = Glob('src/hex/*.hex')
fonts_png = Glob('src/png/*.png')
build_dir = env.Command('build/{bin,hex,psf,map}', '', 'mkdir ${TARGET}')

def copy(source, ext):
    return env.Command(
        'build/html/download/%s/${SOURCE.file}' % (ext,),
        source,
        'cp $SOURCE $TARGET',
    )


def convert(source, src_ext, dst_ext, extra=''):
    converter = env.Command(
        'build/html/download/%s/${SOURCE.filebase}.%s' % (
            dst_ext,
            dst_ext,
        ),
        source,
        'bin/%s2%s %s -o $TARGET $SOURCE' % (
            src_ext,
            dst_ext,
            extra,
        )
    )
    Depends(converter, build_dir)
    return converter


def compress(source):
    return env.Command(
        '${SOURCE}.gz',
        source,
        'gzip -c ${SOURCE} > ${TARGET}',
    )

# from .bin to .hex, .psf
for font in fonts_bin:
    umap = str(font).replace('.bin', '.map')
    build_bin.extend(copy(font, 'bin'))
    for font_hex in convert(font, 'bin', 'hex'):
        build_hex.append(font_hex)
        for font_psf in convert(font_hex, 'hex', 'psf', '-m ' + umap):
            build_psf.append(font_psf)
            compress(font_psf)

# from .fnt to .bin, .hex, .psf
for font in fonts_fnt:
    umap = str(font).replace('.fnt', '.map')
    for font_bin in convert(font, 'fnt', 'bin'):
        build_bin.append(font_bin)
        for font_hex in convert(font_bin, 'bin', 'hex'):
            build_hex.append(font_hex)
            for font_psf in convert(font_hex, 'hex', 'psf', '-m ' + umap):
                build_psf.append(font_psf)
                compress(font_psf)

# from .hex to .bin, .psf
for font in fonts_hex:
    umap = str(font).replace('.hex', '.map')
    build_hex.extend(copy(font, 'hex'))
    build_bin.extend(convert(font, 'hex', 'bin'))
    for font_psf in convert(font, 'hex', 'psf', '-m ' + umap):
        build_psf.append(font_psf)
        compress(font_psf)

# from .png to .bin, .hex, .psf
for font in fonts_png:
    umap = str(font).replace('.png', '.map')
    for font_hex in convert(font, 'png', 'hex'):
        build_hex.append(font_hex)
        build_bin.extend(convert(font_hex, 'hex', 'bin'))
        for font_psf in convert(font_hex, 'hex', 'psf', '-m ' + umap):
            build_psf.append(font_psf)
            compress(font_psf)

# from .psf to .fnt
for font in build_psf:
    env.Command(
        'build/html/download/bdf/${SOURCE.filebase}.bdf',
        font,
        'psf2bdf $SOURCE $TARGET',
    )
    env.Command(
        'build/html/download/fnt/${SOURCE.filebase}.fnt',
        font,
        'psf2fnt $SOURCE $TARGET',
    )

# from .psf to .html
env.Command('build/html/preview', '', 'mkdir -p ${TARGET}')
for font in build_psf:
    font_png_preview = env.Command(
        'build/html/preview/${SOURCE.filebase}.png',
        font,
        'bin/psf2png '
        '-o ${TARGET} '
        '${SOURCE}',
    )
    font_html = env.Command(
        'build/html/${SOURCE.filebase}.html',
        font,
        'mkdir -p build/html && '
        'bin/psf2html '
        '-o ${TARGET} '
        '${SOURCE}',
    )
    Depends(font_html, font_png_preview)

# Validate results
if 'test' in COMMAND_LINE_TARGETS:
    def scan(variant):
        return set([
            os.path.splitext(os.path.basename(filename))[0]
            for filename in os.listdir(os.path.join('build', variant))
            if not filename.endswith('.gz')
        ])
    scan_bin = scan('bin')
    scan_hex = scan('hex')
    scan_psf = scan('psf')
    scan_all = scan_bin | scan_hex | scan_psf
    print '%-32s bin hex psf' % ('font',)
    for item in sorted(scan_all):
        print '%-32s %s   %s   %s' % (
            item,
            '+' if item in scan_bin else '-',
            '+' if item in scan_hex else '-',
            '+' if item in scan_psf else '-',
        )
