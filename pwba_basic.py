def find_unicode(text):
    unicode_chars = []
    for char in text:
        char_unicode = ord(char)
        if unicodedata.category(char_unicode) == 'So':
            unicode_chars.append(char)
    return unicode_chars