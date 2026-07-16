# main.py
# Milestone 5: CLI Test Runner — the live demo entry point for HelixDrive

import random
from encoder import encode_text_to_protected_dna
from decoder import decode_dna_to_text

DNA_BASES = ["A", "C", "T", "G"]

def simulate_mutation_noise(dna_sequence: str, num_mutations: int) -> str:
    """
    Randomly flips `num_mutations` bases in the DNA sequence to simulate
    real-world synthesis/sequencing errors or physical degradation.
    """
    dna_list = list(dna_sequence)
    sequence_length = len(dna_list)

    # Pick unique random positions to mutate
    positions_to_mutate = random.sample(range(sequence_length), min(num_mutations, sequence_length))

    for pos in positions_to_mutate:
        original_base = dna_list[pos]
        # Pick a different base than the original, to guarantee a real mutation
        new_base = random.choice([b for b in DNA_BASES if b != original_base])
        dna_list[pos] = new_base

    return "".join(dna_list), positions_to_mutate

def print_divider():
    print("-" * 60)

def run_demo():
    print_divider()
    print("HelixDrive — DNA Data Storage Pipeline Simulator (MVP)")
    print_divider()

    user_message = input("\nEnter a message to store as DNA: ")

    if not user_message:
        print("No message entered. Exiting.")
        return

    # --- ENCODE ---
    dna_sequence = encode_text_to_protected_dna(user_message)
    print(f"\n[1] Encoded to DNA ({len(dna_sequence)} bases):")
    print(f"    {dna_sequence}")

    # --- SIMULATE NOISE ---
    try:
        num_mutations = int(input("\nHow many random mutations to simulate? (try 1-5): "))
    except ValueError:
        num_mutations = 1
        print("Invalid input, defaulting to 1 mutation.")

    mutated_dna, mutated_positions = simulate_mutation_noise(dna_sequence, num_mutations)
    print(f"\n[2] Simulated {num_mutations} mutation(s) at position(s): {mutated_positions}")
    print(f"    {mutated_dna}")

    # --- DECODE + REPAIR ---
    print("\n[3] Attempting to decode and self-heal...")
    try:
        recovered_message = decode_dna_to_text(mutated_dna)
        print(f"    Recovered message: \"{recovered_message}\"")

        print_divider()
        if recovered_message == user_message:
            print("✅ SUCCESS — Data integrity preserved despite mutation noise.")
        else:
            print("⚠️  WARNING — Data decoded but does NOT match original. Silent corruption.")
        print_divider()

    except Exception as error:
        print_divider()
        print(f"❌ FAILURE — Mutation noise exceeded error-correction capacity.")
        print(f"    Error detail: {error}")
        print("    This means the redundancy layer needs to be strengthened for this")
        print("    level of noise (increase PARITY_BYTES in error_correction.py).")
        print_divider()


if __name__ == "__main__":
    run_demo()