# Function to encrypt the text
def encrypt(text, shift1, shift2):
    result = ""  # store encrypted text

    # loop through each character
    for char in text:
        if char.islower():  # check if lowercase letter

            if char >= 'a' and char <= 'm':
                # move forward by shift1 * shift2
                shift = shift1 * shift2
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                result += new_char

            elif char >= 'n' and char <= 'z':
                # move backward by shift1 + shift2
                shift = shift1 + shift2
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                result += new_char

        else:
            # keep non-lowercase characters unchanged
            result += char

    return result


# Function to decrypt the text (logic will be added later)
def decrypt(text, shift1, shift2):
    return text


# Function to verify if original and decrypted text are the same
def verify(original_text, decrypted_text):
    return original_text == decrypted_text


# Main function to control the program flow
def main():
    # take input values from user
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # read text from file
    with open("raw_text.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    # encrypt the text
    encrypted_text = encrypt(original_text, shift1, shift2)

    # save encrypted text into file
    with open("encrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(encrypted_text)

    # decrypt the text
    decrypted_text = decrypt(encrypted_text, shift1, shift2)

    # save decrypted text into file
    with open("decrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(decrypted_text)

    # check if decryption is correct
    if verify(original_text, decrypted_text):
        print("Verification successful: decrypted text matches original text.")
    else:
        print("Verification failed: decrypted text does not match original text.")


# run the program
main()