import os

env = Environment()
env.VariantDir('build', 'src')

def export_font(source, export_format):
    converter = env.Command(
        'build/${SOURCE.dir}/${SOURCE.filebase}.%s' % (export_format,),
        source,
        'bin/export-font --format %s --output $TARGET $SOURCE' % (export_format,)
    )
    return converter

def export_html(source, export_format='html'):
    if export_format == 'index.html':
        target = 'build/${SOURCE.dir}/${SOURCE.filebase}/index.html'
    else:
        target = 'build/${SOURCE.dir}/${SOURCE.filebase}.html',
    converter = env.Command(
        target,
        source,
        'bin/export-html --output $TARGET $SOURCE',
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
        'bin/export-png  --output $TARGET %s $SOURCE' % (extra,)
    )
    return converter


def compress(source):
    return env.Command(
        '${SOURCE}.gz',
        source,
        'gzip -c ${SOURCE} > ${TARGET}',
    )

export_html(Glob('font'), 'index.html')
for collection in Glob('font/*'):
    export_html(collection, 'index.html')
    for vendor in Glob(str(collection) + '/*'):
        export_html(vendor, 'index.html')

for font in Glob('font/*/*/*.yml'):
    export_font(font, 'bin')
    export_font(font, 'hex')
    export_font(font, 'psf')
    export_html(font, 'html')
    export_png(font, 'back', scale=5)
    export_png(font, 'char', columns=16)
    export_png(font, 'text', text=None)
