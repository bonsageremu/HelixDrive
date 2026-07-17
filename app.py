# app.py
# HelixDrive — Streamlit Web Demo
# Interactive browser-based version of the CLI pipeline demo

import streamlit as st
from encoder import encode_text_to_protected_dna
from decoder import decode_dna_to_text
from main import simulate_mutation_noise

# --- Page Configuration ---
st.set_page_config(
    page_title="HelixDrive — DNA Data Storage",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 HelixDrive")
st.caption("Cloud-based DNA data storage — live pipeline simulation")

st.markdown(
    "Type a message below. HelixDrive will encode it into synthetic DNA, "
    "protect it with Reed-Solomon error correction, simulate physical "
    "mutation noise, and attempt to recover your original message."
)

st.divider()

# --- Input Section ---
user_message = st.text_input("Enter a message to store as DNA:", value="Hello YC")

num_mutations = st.slider(
    "Number of simulated mutations (degradation events):",
    min_value=0,
    max_value=20,
    value=2,
    help="Higher values simulate more physical degradation, synthesis errors, or sequencing noise."
)

run_button = st.button("Run HelixDrive Pipeline", type="primary")

# --- Pipeline Execution ---
if run_button:
    if not user_message:
        st.warning("Please enter a message first.")
    else:
        # Step 1: Encode
        dna_sequence = encode_text_to_protected_dna(user_message)

        st.subheader("1. Encoded DNA Sequence")
        st.code(dna_sequence, language=None)
        st.caption(f"{len(dna_sequence)} bases generated from {len(user_message)} character(s)")

        # Step 2: Simulate mutation noise
        mutated_dna, mutated_positions = simulate_mutation_noise(dna_sequence, num_mutations)

        st.subheader("2. Simulated Mutation Noise")

        # Build a visual diff: highlight mutated positions in red
        highlighted = ""
        for i, base in enumerate(mutated_dna):
            if i in mutated_positions:
                highlighted += f":red[**{base}**]"
            else:
                highlighted += base
        st.markdown(highlighted)
        st.caption(f"{num_mutations} mutation(s) simulated at position(s): {mutated_positions}")

        # Step 3: Decode + Repair
        st.subheader("3. Decode & Self-Heal")

        try:
            recovered_message = decode_dna_to_text(mutated_dna)

            if recovered_message == user_message:
                st.success(f"✅ SUCCESS — Recovered message: \"{recovered_message}\"")
                st.markdown("Data integrity preserved despite mutation noise.")
            else:
                st.warning(f"⚠️ Decoded but does NOT match original: \"{recovered_message}\"")
                st.markdown("This indicates silent corruption slipped past error correction.")

        except Exception as error:
            st.error("❌ FAILURE — Mutation noise exceeded error-correction capacity.")
            st.code(str(error))
            st.markdown(
                "This means the redundancy layer needs to be strengthened for this "
                "noise level — increase `PARITY_BYTES` in `error_correction.py`."
            )

st.divider()
st.caption("HelixDrive MVP — built to validate the technical feasibility of a software-defined DNA storage pipeline.")