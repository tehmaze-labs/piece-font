#!/usr/bin/env python2

CONTROL_ABBRS = (
    'NUL',      # 0x00 NULL
    'SOH',      # 0x01 Start Of Heading
    'STX',      # 0x02 Start Of Text
    'ETX',      # 0x03 End Of Text
    'EOT',      # 0x04 End Of Transmission
    'ENQ',      # 0x05 Enquiry
    'ACK',      # 0x06 Acknowledgement
    'BEL',      # 0x07 Bell
    'BS',       # 0x08 Back Space
    'HT',       # 0x09 Horizontal Tab
    'LF',       # 0x0a Line Feed
    'VT',       # 0x0b Vertical Tab
    'FF',       # 0x0c Form Feed
    'CR',       # 0x0d Carriage Return
    'SO',       # 0x0e Shift Out / X-On
    'SI',       # 0x0f Shift In / X-Off
    'DLE',      # 0x10 Data Line Escape
    'DC1',      # 0x11 Device Control 1 (oft. XON)
    'DC2',      # 0x12 Device Control 2
    'DC3',      # 0x13 Device Control 3 (oft. XOFF)
    'DC4',      # 0x14 Device Control 4
    'NAK',      # 0x15 Negative Acknowledgement
    'SYN',      # 0x16 Synchronous Idle
    'ETB',      # 0x17 End of Transmission Block
    'CAN',      # 0x18 Cancel
    'EM',       # 0x19 End of Medium
    'SUB',      # 0x1a Substitute
    'ESC',      # 0x1b Escape
    'FS',       # 0x1c File Separator
    'GS',       # 0x1d Group Separator
    'RS',       # 0x1e Record Separator
    'US',       # 0x1f Unit Separator
)

CONTROL_NAMES = (
    'NULL',
    'Start Of Heading',
    'Start Of Text',
    'End Of Text',
    'End Of Transmission',
    'Enquiry',
    'Acknowledgement',
    'Bell',
    'Back Space',
    'Horizontal Tab',
    'Line Feed',
    'Vertical Tab',
    'Form Feed',
    'Carriage Return',
    'Shift Out / X-On',
    'Shift In / X-Off',
    'Data Line Escape',
    'Device Control 1 (oft. XON)',
    'Device Control 2',
    'Device Control 3 (oft. XOFF)',
    'Device Control 4',
    'Negative Acknowledgement',
    'Synchronous Idle',
    'End of Transmission Block',
    'Cancel',
    'End of Medium',
    'Substitute',
    'Escape',
    'File Separator',
    'Group Separator',
    'Record Separator',
    'Unit Separator',
)

CONTROL_CHARS = {x: name for x, name in enumerate(CONTROL_ABBRS)}
CONTROL_CHARS[0x7f] = 'DEL'
CONTROL_SHORT = {name: x for x, name in enumerate(CONTROL_ABBRS)}
CONTROL_SHORT['DEL'] = 0x7f
CONTROL_WORDS = {x: word for x, word in enumerate(CONTROL_NAMES)}
CONTROL_WORDS[0x7f] = 'Delete'
