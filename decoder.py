# decoder.py
# Milestone 4: Converts a DNA sequence back into original text, repairing any corruption

from error_correction import repair_data

# Reverse of the encoder's BIT_TO_BASE table
BASE_TO_BIT = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11"
}

def dna_to_binary(dna_sequence: str) -> str:
    """
    Converts a DNA base sequence back into a binary string.
    """
    binary_string = ""
    for base in dna_sequence:
        binary_string += BASE_TO_BIT[base]
    return binary_string

def binary_to_bytes(binary_string: str) -> bytes:
    """
    Converts a binary string back into raw bytes.
    Any leftover bits shorter than 8 (from padding) are dropped.
    """
    byte_list = []
    for i in range(0, len(binary_string) - 7, 8):
        byte_chunk = binary_string[i:i+8]
        byte_list.append(int(byte_chunk, 2))
    return bytes(byte_list)

def decode_dna_to_text(dna_sequence: str) -> str:
    """
    Full pipeline: DNA -> binary -> bytes -> RS repair -> original text
    """
    binary_string = dna_to_binary(dna_sequence)
    protected_bytes = binary_to_bytes(binary_string)

    repaired_bytes = repair_data(protected_bytes)
    original_text = repaired_bytes.decode("utf-8")
    return original_text


# --- Quick standalone test: full round trip ---
if __name__ == "__main__":
    from encoder import encode_text_to_protected_dna

    original_message = "Hi"
    print(f"Original message: {original_message}")

    dna = encode_text_to_protected_dna(original_message)
    print(f"Encoded DNA:       {dna}")

    decoded_message = decode_dna_to_text(dna)
    print(f"Decoded message:   {decoded_message}")

    assert decoded_message == original_message, "Mismatch! Something broke."
    print("✅ Round trip successful — data matches perfectly.")

# Simulate DNA-level corruption (like a real mutation)
    corrupted_dna = list(dna)
    corrupted_dna[5] = "A" if corrupted_dna[5] != "A" else "T"  # flip one base
    corrupted_dna = "".join(corrupted_dna)

    print(f"\nCorrupted DNA:     {corrupted_dna}")
    repaired_message = decode_dna_to_text(corrupted_dna)
    print(f"Repaired message:  {repaired_message}")