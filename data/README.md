# HelixDrive

**Cloud-based DNA data storage — synthetic biology meets cold-storage economics.**

HelixDrive is a working software simulation of a DNA-based data storage pipeline: encoding arbitrary digital data into synthetic DNA base sequences, protecting it with error-correcting codes, simulating real-world degradation (mutation noise), and reconstructing the original data with byte-perfect accuracy.

This repository contains a functional MVP of the core encode → protect → mutate → decode pipeline, built to validate the technical feasibility of the approach ahead of production hardware/wet-lab integration.

---

## Why DNA Storage

Global data generation is outpacing the density and durability of magnetic and flash storage. DNA offers:

- **Extreme density** — theoretical limits around 1 exabyte per gram
- **Multi-century durability** — intact DNA has been recovered from remains tens of thousands of years old, far outlasting tape or disk
- **No format obsolescence** — DNA sequencing will remain relevant as long as biology does; unlike tape drives or optical formats, the "reader" isn't going anywhere

The bottleneck isn't the storage medium — it's building a **reliable, software-defined pipeline** to get data in and out cleanly. That's what HelixDrive solves.

---

## Pipeline Architecture

```
 Input Text/Data
       │
       ▼
 ┌─────────────────┐
 │   Encoder        │  text → UTF-8 bytes
 └─────────────────┘
       │
       ▼
 ┌─────────────────┐
 │ Error Correction │  Reed-Solomon parity bytes appended
 │   (reedsolo)     │
 └─────────────────┘
       │
       ▼
 ┌─────────────────┐
 │   Base Mapping   │  2-bit chunks → {A, C, G, T}
 └─────────────────┘
       │
       ▼
   DNA Sequence  ──────►  [ Simulated synthesis / storage / sequencing noise ]
       │
       ▼
 ┌─────────────────┐
 │  Decoder         │  DNA → 2-bit chunks → bytes
 └─────────────────┘
       │
       ▼
 ┌─────────────────┐
 │ RS Repair        │  detects & corrects corrupted bytes
 └─────────────────┘
       │
       ▼
 Recovered Text/Data  (byte-identical to input)
```

### Base Mapping Scheme

| Bits | Base |
|------|------|
| 00   | A    |
| 01   | C    |
| 10   | G    |
| 11   | T    |

Each byte of (RS-protected) data maps to exactly 4 DNA bases.

### Error Correction

Reed-Solomon coding (`reedsolo` library) is applied to the raw bytes **before** DNA conversion, not after — meaning the redundancy is baked into the DNA sequence itself, mirroring how a real synthesis/sequencing pipeline would need to protect data before it's physically written into DNA.

- Configurable parity byte count (`PARITY_BYTES` in `error_correction.py`)
- Each parity byte added increases correctable mutation capacity by roughly 0.5 corrupted bytes
- Verified empirically: 10 parity bytes reliably corrected up to 5 simulated mutations; doubling to 20 parity bytes raised that ceiling to 10 mutations — a direct, tunable tradeoff between storage overhead and fault tolerance

This tunability is the core product lever: customers with higher-value/lower-redundancy-budget data can select their own point on the density-vs-durability curve.

---

## Repository Structure

```
HelixDrive/
├── encoder.py           # Text/bytes → DNA sequence (with RS protection)
├── decoder.py           # DNA sequence → repaired bytes → original text
├── error_correction.py  # Reed-Solomon encode/repair logic
├── main.py              # Interactive CLI demo / test runner
├── data/
│   ├── input/            # Sample input files (optional, for batch testing)
│   └── output/           # Decoded output files (optional, for batch testing)
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone <your-repo-url>
cd HelixDrive
python -m venv venv

# Activate the virtual environment
source venv/bin/activate        # Mac/Linux
venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
```

---

## Usage

Run the interactive demo:

```bash
python main.py
```

You'll be prompted to:
1. Enter a message to encode into DNA
2. Specify how many random mutations to simulate (representing physical degradation, synthesis errors, or sequencing errors)
3. Watch the pipeline attempt to decode and self-heal the corrupted sequence

**Example run:**

```
Enter a message to store as DNA: Hi
[1] Encoded to DNA (48 bases):
    CAGACGGCTGTTTGCCACCTCGGGTGACCCATGCAGAGTGACTCCACC

How many random mutations to simulate? (try 1-5): 2
[2] Simulated 2 mutation(s) at position(s): [5, 31]
    CAGACAGCTGTTTGCCACCTCGGGTAACCCATGCAGAGTGACTCCACC

[3] Attempting to decode and self-heal...
    Recovered message: "Hi"
------------------------------------------------------------
✅ SUCCESS — Data integrity preserved despite mutation noise.
------------------------------------------------------------
```

### Running Individual Modules

Each module also runs standalone for isolated testing:

```bash
python encoder.py            # Test encoding logic only
python error_correction.py   # Test RS protection + repair only
python decoder.py            # Test full round trip + DNA-level corruption
```

---

## Known Limitations (MVP Scope)

Being transparent about current scope, since this is a simulation built to validate pipeline logic — not yet a production system:

- **Noise model is substitution-only.** Real DNA synthesis/sequencing errors are frequently insertions/deletions (indels) rather than pure base substitutions, and are biased toward specific motifs (e.g., homopolymer runs like `AAAA`). Production would require indel-tolerant coding (fountain codes, or substitution + indel hybrid schemes as used in published DNA storage research).
- **No biological sequence constraints yet.** Production encoding needs to avoid problematic motifs (long homopolymers, extreme GC-content imbalance, secondary structure formation) that cause real synthesis/sequencing failures — this MVP maps bits to bases directly without those constraints.
- **No physical synthesis/sequencing integration.** This is a software simulation of the logical pipeline; a production system integrates with DNA synthesis providers (e.g., Twist Bioscience) and sequencing platforms (e.g., Oxford Nanopore, Illumina) on the physical read/write side.
- **Single-file scale only.** No chunking/indexing strategy yet for large files split across many DNA strands, which is required at real storage scale.

## Roadmap

- [ ] Indel-tolerant error correction (fountain codes / LT codes)
- [ ] Biologically-constrained encoding (GC-content balancing, homopolymer avoidance)
- [ ] File chunking + strand indexing for large-file support
- [ ] Web-based demo interface
- [ ] Integration with a real DNA synthesis API for end-to-end physical proof-of-concept

---

## Tech Stack

- **Python 3** — core pipeline logic
- **[reedsolo](https://pypi.org/project/reedsolo/)** — Reed-Solomon error correction

---

## License

TBD