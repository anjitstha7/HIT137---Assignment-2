# Function to shift a character inside its own group
def shift_within_group(char, group_start, group_size, shift, forward=True):
    # find the position of the character inside the group
    offset = ord(char) - ord(group_start)

    # move forward or backward inside the group
    if forward:
        new_offset = (offset + shift) % group_size
    else:
        new_offset = (offset - shift) % group_size

    # convert back to a character
    return chr(ord(group_start) + new_offset)


# Function to encrypt one character
def encrypt_char(char, shift1, shift2):

    # lowercase a-m
    if 'a' <= char <= 'm':
        return shift_within_group(char, 'a', 13, shift1 * shift2, forward=True)

    # lowercase n-z
    elif 'n' <= char <= 'z':
        return shift_within_group(char, 'n', 13, shift1 + shift2, forward=False)

    # uppercase A-M
    elif 'A' <= char <= 'M':
        return shift_within_group(char, 'A', 13, shift1, forward=False)

    # uppercase N-Z
    elif 'N' <= char <= 'Z':
        return shift_within_group(char, 'N', 13, shift2 * shift2, forward=True)

    # other characters stay the same
    return char


# Function to decrypt one character
def decrypt_char(char, shift1, shift2):

    # lowercase a-m
    if 'a' <= char <= 'm':
        return shift_within_group(char, 'a', 13, shift1 * shift2, forward=False)

    # lowercase n-z
    elif 'n' <= char <= 'z':
        return shift_within_group(char, 'n', 13, shift1 + shift2, forward=True)

    # uppercase A-M
    elif 'A' <= char <= 'M':
        return shift_within_group(char, 'A', 13, shift1, forward=True)

    # uppercase N-Z
    elif 'N' <= char <= 'Z':
        return shift_within_group(char, 'N', 13, shift2 * shift2, forward=False)

    # other characters stay the same
    return char


# Function to process the whole text
def transform_text(text, shift1, shift2, encrypt=True):
    result = ""

    # go through each character in the text
    for char in text:
        if encrypt:
            # encrypt each character
            result += encrypt_char(char, shift1, shift2)
        else:
            # decrypt each character
            result += decrypt_char(char, shift1, shift2)

    return result


# Function to encrypt the file
def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    encrypted_text = transform_text(original_text, shift1, shift2, encrypt=True)

    with open("encrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(encrypted_text)


# Function to decrypt the file
def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r", encoding="utf-8") as file:
        encrypted_text = file.read()

    decrypted_text = transform_text(encrypted_text, shift1, shift2, encrypt=False)

    with open("decrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(decrypted_text)


# Function to verify the result
def verify_decryption():
    with open("raw_text.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    with open("decrypted_text.txt", "r", encoding="utf-8") as file:
        decrypted_text = file.read()

    if original_text == decrypted_text:
        print("Verification successful: decrypted text matches original text.")
    else:
        print("Verification failed: decrypted text does not match original text.")


# Main function
def main():
    # take shift values from user
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # encrypt the original file
    encrypt_file(shift1, shift2)

    # decrypt the encrypted file
    decrypt_file(shift1, shift2)

    # check whether original and decrypted texts match
    verify_decryption()


# Run the program
if __name__ == "__main__":
    main()