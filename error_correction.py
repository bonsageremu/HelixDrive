# error_correction.py
# Milestone 3: Adds Reed-Solomon error correction to protect data from simulated noise/mutation

from reedsolo import RSCodec

# How many "parity" (repair) bytes to add.
# More parity bytes = more resilience to corruption, but larger DNA output.
# 10 is a reasonable MVP default — it can correct up to 5 corrupted bytes.
PARITY_BYTES = 20

rsc = RSCodec(PARITY_BYTES)

def add_error_correction(data_bytes: bytes) -> bytes:
    """
    Takes raw bytes and returns bytes with Reed-Solomon parity data appended.
    """
    encoded = rsc.encode(data_bytes)
    return encoded

def repair_data(received_bytes: bytes) -> bytes:
    """
    Attempts to detect and repair corrupted bytes using Reed-Solomon.
    Returns the original clean data (parity bytes stripped off).
    """
    decoded_msg, decoded_full, errata_pos = rsc.decode(received_bytes)
    return decoded_msg


# --- Quick standalone test ---
if __name__ == "__main__":
    original_text = "Hi"
    original_bytes = original_text.encode("utf-8")
    print(f"Original bytes:      {original_bytes}")

    protected = add_error_correction(original_bytes)
    print(f"With RS parity:      {protected}")
    print(f"Length grew from {len(original_bytes)} to {len(protected)} bytes")

    # Simulate corruption: flip one byte in the middle
    corrupted = bytearray(protected)
    corrupted[2] = 0xFF  # simulate a "mutation"
    corrupted = bytes(corrupted)
    print(f"Corrupted version:   {corrupted}")

    repaired = repair_data(corrupted)
    print(f"Repaired data:       {repaired}")
    print(f"Repaired text:       {repaired.decode('utf-8')}")