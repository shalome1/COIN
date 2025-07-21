# pip install --user eth-keys eth-utils eth-hash[pycryptodome] tqdm

from eth_keys import keys
from eth_utils import keccak
from tqdm import tqdm
import os
import time

def generate_eth_keypair():
    private_key_bytes = os.urandom(32)
    private_key = keys.PrivateKey(private_key_bytes)
    public_key = private_key.public_key
    address_bytes = keccak(public_key.to_bytes())[-20:]
    address = '0x' + address_bytes.hex()
    return private_key.to_hex()[2:], address

def write_to_files(pairs, keys_file, addresses_file):
    with open(keys_file, 'a') as kf, open(addresses_file, 'a') as af:
        for priv_key, address in pairs:
            kf.write(f"{priv_key},{address}\n")
            af.write(f"{address}\n")

def generate_and_save_all(num_keys, batch_size, keys_file, addresses_file):
    total_batches = num_keys // batch_size
    remaining = num_keys % batch_size

    print(f"⏳ Generating {num_keys} Ethereum addresses in batches of {batch_size}...")

    start = time.time()

    with tqdm(total=total_batches + (1 if remaining else 0), desc="🔨 Progress", unit="batch") as pbar:
        for _ in range(total_batches):
            pairs = [generate_eth_keypair() for _ in range(batch_size)]
            write_to_files(pairs, keys_file, addresses_file)
            pbar.update(1)

        if remaining:
            pairs = [generate_eth_keypair() for _ in range(remaining)]
            write_to_files(pairs, keys_file, addresses_file)
            pbar.update(1)

    print(f"\n✅ Done. Generated {num_keys} Ethereum addresses.")
    print(f"🕒 Time taken: {time.time() - start:.2f} seconds.")

if __name__ == "__main__":
    keys_file = "eth_main.txt"
    addresses_file = "eth.txt"

    try:
        num_keys = int(input("How many Ethereum addresses to generate? "))
        batch_size = 200  # Reduce to avoid memory issues on PythonAnywhere free tier
        generate_and_save_all(num_keys, batch_size, keys_file, addresses_file)
    except ValueError:
        print("❌ Please enter a valid number.")
