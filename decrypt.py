import operator
from argparse import ArgumentParser

P_I_ENGLISH = [0.082, 0.015, 0.028, 0.042, 0.127, 0.022, 0.020, 0.061, 0.070,
               0.001, 0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060,
               0.063, 0.090, 0.028, 0.001, 0.024, 0.002, 0.001, 0.001]
P_I_DUTCH = [0.0749, 0.0158, 0.0124, 0.0593, 0.1891, 0.0081, 0.03, 0.0238, 0.07,
             0.0146, 0.0225, 0.0357, 0.0221, 0.1003, 0.0606, 0.0157, 0.00009,
             0.0641, 0.0373, 0.0679, 0.0199, 0.0285, 0.0152, 0.000, 0.00035, 0.0139]
P_I_2_ENGLISH = 0.065
P_I_2_DUTCH = 0.080

Specials = dict[int, str]

def decrypt(ciphertext: str, *, min_length=2, max_length=12):

    ciphertext_clean, specials = remove_specials(ciphertext)

    key_length = find_key_length(ciphertext_clean, min_length=min_length, max_length=max_length)

    key_values = find_key(ciphertext_clean, key_length)
    key = "".join(chr(c + ord('a')) for c in key_values)

    plaintext_clean = decrypt_with_key(ciphertext_clean, key_values)
    plaintext = insert_specials(plaintext_clean, specials)
    return key, plaintext


def remove_specials(ciphertext: str) -> tuple[str, Specials]:
    """Removes all non alphabetical characters from string and saves them in a dict."""
    specials: Specials = {}
    clean_string = ""

    for i in range(len(ciphertext) - 1, -1, -1):
        char = ciphertext[i]

        if not char.isalpha():
            specials[i] = char

        else:
            clean_string += char

    return clean_string[::-1], specials


def insert_specials(clean_string, specials: Specials) -> str:
    output = ""

    clean_index = 0

    for i in range(len(specials) + len(clean_string)):
        if i in specials:
            output += specials[i]
        else:
            output += clean_string[clean_index]
            clean_index += 1

    return output


def find_key_length(cipher_array, *, min_length, max_length):
    # Difference between p_i^2 and q_i^2
    diff_pi2_qi2 = {}

    # Iterate over all possible keylengths
    for n in range(min_length, max_length + 1):
        # List for q_0 ... q_25
        hist = [0 for _ in range(26)]

        # Count all occurrences into hist
        for i in range(0, len(cipher_array), n):
            index = ord(cipher_array[i].lower()) - ord('a')
            hist[index] += 1

        total = sum(hist)

        q_i = [(i / total) for i in hist]
        q_i_2 = [i ** 2 for i in q_i]
        diff_pi2_qi2[n] = abs(P_I_2_ENGLISH - sum(q_i_2))

    # Return the keylength with the smallest difference between p_i^2 and q_i^2
    return min(diff_pi2_qi2.items(), key=operator.itemgetter(1))[0]


def find_key(ciphertext: str, key_length: int):
    key = [0 for _ in range(key_length)]

    # For every letter in key
    for i in range(key_length):
        sum_qi_pi = [0 for _ in range(26)]

        # Try all possible key values
        for key_value in range(26):
            q_i = [0 for _ in range(26)]

            # Count al letters within the i-th byte of the key
            for char_pos in range(i, len(ciphertext), key_length):
                letter = (ord(ciphertext[char_pos].lower()) - ord('a') - key_value) % 26

                q_i[letter] += 1

            qipi = [P_I_ENGLISH[letter_pos] * q_i[letter_pos]
                    for letter_pos in range(26)]

            sum_qi_pi[key_value] = sum(qipi)

        # Select the value with the highest p_i * q_i
        key[i] = sum_qi_pi.index(max(sum_qi_pi))

    return key


def decrypt_with_key(ciphertext, keyword) -> str:

    plaintext = ""

    key_index = 0

    for c in ciphertext:

        key = keyword[key_index]

        if c.isupper():
            plaintext += chr((ord(c) - ord('A') - key) % 26 + ord('A'))
        else:
            plaintext += chr((ord(c) - ord('a') - key) % 26 + ord('a'))

        key_index = (key_index + 1) % len(keyword)

    return plaintext


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("ciphertext", help="ciphertext to decrypt")
    args = parser.parse_args()

    key, plaintext = decrypt(args.ciphertext)
    print("Key      :", key)
    print("Plaintext:", plaintext)
