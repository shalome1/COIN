import os
from tqdm import tqdm

def load_target_addresses(file_path):
    """Load target addresses into a lowercase set for case-insensitive matching."""
    with open(file_path, 'r', encoding='utf-8') as f:
        targets = set(line.strip().lower() for line in f if line.strip())
    print(f"📦 Loaded {len(targets)} target addresses.")
    return targets

def process_files(address_file, key_file, target_file, found_folder, clear_after=True):
    os.makedirs(found_folder, exist_ok=True)
    target_addresses = load_target_addresses(target_file)

    loop_count = 0
    max_loops = 1000  # Failsafe

    while True:
        loop_count += 1
        if loop_count > max_loops:
            print("🛑 Max loop count reached. Exiting.")
            break

        # Load current data
        with open(address_file, 'r', encoding='utf-8') as af:
            addresses = [line.strip().lower() for line in af if line.strip()]
        with open(key_file, 'r', encoding='utf-8') as kf:
            keys_and_addresses = [line.strip() for line in kf if line.strip()]

        if not addresses:
            print("✅ All addresses processed. Nothing left to check.")
            break

        if len(addresses) != len(keys_and_addresses):
            print(f"❌ Line count mismatch:")
            print(f"eth.txt lines:        {len(addresses)}")
            print(f"eth_main.txt lines:   {len(keys_and_addresses)}")
            print("🛑 Aborting. Fix the files so each address has a matching key line.")
            break

        print(f"\n🔍 Loop {loop_count}: Checking {len(addresses)} addresses...")

        # Debug Preview: first 5 entries from both sources
        print("🔎 Sample from eth.txt:", addresses[:3])
        print("🔎 Sample from target file:", list(target_addresses)[:3])

        matches_found = 0

        for addr, key_line in tqdm(zip(addresses, keys_and_addresses), total=len(addresses), desc="🔎 Progress"):
            if addr in target_addresses:
                with open(os.path.join(found_folder, "found_match.txt"), 'a', encoding='utf-8') as f:
                    f.write(key_line + '\n')
                print(f"🎯 Match found: {addr}")
                matches_found += 1

        print(f"✅ Checked {len(addresses)} entries. Matches found this round: {matches_found}")

        if clear_after:
            open(address_file, 'w').close()
            open(key_file, 'w').close()
            print("🧹 Files cleared after check (set `clear_after=False` to disable).")

        if matches_found == 0:
            print("🚫 No matches found. Exiting.")
            break

if __name__ == "__main__":
    address_file = "eth.txt"
    key_file = "eth_main.txt"
    target_file = "toMatch.txt"
    found_folder = "found"

    process_files(address_file, key_file, target_file, found_folder, clear_after=True)