def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    last = ord("Z")
    first = ord("A")
    letters = last - first + 1

    for a in plaintext:
        if not a.isalpha():
            ciphertext += a
            continue

        first = ord("a") if a.islower() is True else ord("A")
        new_pos = ord(a) - first + shift
        ciphertext += chr(first + new_pos % letters)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    last = ord("Z")
    first = ord("A")
    letters = last - first + 1
    for a in ciphertext:
        if not a.isalpha():
            plaintext += a
            continue

        last = ord("z") if a.islower() else ord("Z")
        new_pos = last - ord(a) + shift
        plaintext += chr(last - new_pos % letters)
    return plaintext
