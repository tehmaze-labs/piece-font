import os

env = Environment()
env.VariantDir('build', 'src')

fonts = Glob('font/*/*/*.yml')

def export(source, export_format):
    converter = env.Command(
        'build/${SOURCE.dir}/${SOURCE.filebase}.%s' % (export_format,),
        source,
        'bin/export-%s -o $TARGET $SOURCE' % (export_format,)
    )
    return converter

def export_png(source, export_format, **flags):
    extra = ' '.join([
        '--%s=%s' % (k, str(v)) if v else '--%s' % (k,)
        for k, v in flags.iteritems()
    ])
    converter = env.Command(
        'build/${SOURCE.dir}/${SOURCE.filebase}.%s.png' % (export_format,),
        source,
        'bin/export-png -o $TARGET %s $SOURCE' % (extra,)
    )
    return converter


def compress(source):
    return env.Command(
        '${SOURCE}.gz',
        source,
        'gzip -c ${SOURCE} > ${TARGET}',
    )

for font in fonts:
    export(font, 'hex')
    export(font, 'psf')

    export(font, 'html')
    export_png(font, 'back', scale=5)
    export_png(font, 'char', columns=16)
    export_png(font, 'text', text=None)
