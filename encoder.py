from error_correction import add_error_correction
# encoder.py
# Milestone 2: Converts text/binary data into a DNA base sequence (A, C, T, G)

# Mapping table: every 2 bits maps to one DNA base
BIT_TO_BASE = {
    "00": "A",
    "01": "C",
    "10": "G",
    "11": "T"
}

def text_to_binary(text: str) -> str:
    """
    Converts a string into a binary string using UTF-8 byte encoding.
    Example: 'A' -> '01000001'
    """
    byte_data = text.encode("utf-8")
    binary_string = "".join(format(byte, "08b") for byte in byte_data)
    return binary_string

def binary_to_dna(binary_string: str) -> str:
    """
    Converts a binary string into a DNA base sequence.
    Pads with a trailing '0' if the binary string length is odd,
    so it can be cleanly split into 2-bit chunks.
    """
    if len(binary_string) % 2 != 0:
        binary_string += "0"  # padding to make it even length

    dna_sequence = ""
    for i in range(0, len(binary_string), 2):
        two_bits = binary_string[i:i+2]
        dna_sequence += BIT_TO_BASE[two_bits]

    return dna_sequence

def encode_text_to_dna(text: str) -> str:
    """
    Full pipeline: text -> binary -> DNA sequence
    """
    binary = text_to_binary(text)
    dna = binary_to_dna(binary)
    return dna


# --- Quick standalone test (only runs if you execute this file directly) ---
if __name__ == "__main__":
    sample_text = "Hi"
    print(f"Original text: {sample_text}")

    binary = text_to_binary(sample_text)
    print(f"Binary form:   {binary}")

    dna = binary_to_dna(binary)
    print(f"DNA sequence:  {dna}")




def encode_text_to_protected_dna(text: str) -> str:
    """
    Full protected pipeline: text -> bytes -> RS-protected bytes -> binary -> DNA
    """
    raw_bytes = text.encode("utf-8")
    protected_bytes = add_error_correction(raw_bytes)

    # Convert protected bytes into a binary string
    binary_string = "".join(format(byte, "08b") for byte in protected_bytes)

    dna = binary_to_dna(binary_string)
    return dna