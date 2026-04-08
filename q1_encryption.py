# Function to encrypt the text (logic will be added later)
def encrypt(text, shift1, shift2):
    return text


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