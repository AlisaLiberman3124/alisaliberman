def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    if len(keyword) <= len(plaintext):
        new_keyword = ""
        for i in range(len(plaintext)):
            new_keyword += keyword[i % len(keyword)]
    else:
        new_keyword = keyword

    for index in range(len(plaintext)):
        symbol = plaintext[index]
        shiftsymbol = new_keyword[index]
        if shiftsymbol.isupper():
            shift = ord(shiftsymbol) - 65
        else:
            shift = ord(shiftsymbol) - 97

        if symbol.isalpha():
            if symbol.isupper():
                new_symbol = chr((ord(symbol) + shift - 65) % 26 + 65)
            else:
                new_symbol = chr((ord(symbol) + shift - 97) % 26 + 97)
            ciphertext += new_symbol
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    if len(keyword) <= len(ciphertext):
        new_keyword = ""
        for i in range(len(ciphertext)):
            new_keyword += keyword[i % len(keyword)]
    else:
        new_keyword = keyword

    for index in range(len(ciphertext)):
        symbol = ciphertext[index]

        shiftsymbol = new_keyword[index]
        if shiftsymbol.isupper():
            shift = ord(shiftsymbol) - 65
        else:
            shift = ord(shiftsymbol) - 97

        if symbol.isalpha():
            if symbol.isupper():
                new_symbol = chr((ord(symbol) - shift - 65) % 26 + 65)
            else:
                new_symbol = chr((ord(symbol) - shift - 97) % 26 + 97)
            plaintext += new_symbol
        else:
            plaintext += symbol
    return plaintext
