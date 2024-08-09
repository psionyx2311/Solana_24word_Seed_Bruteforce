import os
import multiprocessing
from solders.keypair import Keypair
from bip_utils import Bip39SeedGenerator

def generate_sol_address(seed_phrase, derivation_path):
    try:
        seed_generator = Bip39SeedGenerator(seed_phrase)
        seed = seed_generator.Generate()
        
        if len(seed) != 64:
            raise ValueError("Seed must be 64 bytes in length.")
        
        keypair = Keypair.from_seed_and_derivation_path(seed, derivation_path)
        pubkey = keypair.pubkey()
        return pubkey
    except Exception as e:
        #print(f"Error: {e}")
        return None

def load_wordlist(filename):
    with open(filename, 'r') as file:
        return [word.strip() for word in file]

def load_addresses(filename):
    with open(filename, 'r') as file:
        return [address.strip().lower() for address in file]

def save_discovery(mnemonic, public_key):
    with open('discovery.txt', 'a') as file:
        file.write(f"Mnemonic: {mnemonic}\n")
        file.write(f"Public key: {public_key}\n")

def check_combinations(words, wordlist, addresses, word_index, progress, total_combinations, lock, discovered_keys, derivation_path):
    for word in wordlist:
        temp_words = words[:]
        temp_words[word_index] = word
        mnemonic = ' '.join(temp_words)

        try:
            pubkey = generate_sol_address(mnemonic, derivation_path)

            if not pubkey:
                continue

            pubkey_str = str(pubkey)

            # Debugging output
            #print(f"Trying mnemonic: {mnemonic}")
            #print(f"Generated public key: {pubkey_str}")

            # Save the generated public key
            with lock:
                discovered_keys.append(pubkey_str)

            if pubkey_str.lower() in addresses:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n\nMatch found!\n")
                print("Public key:", pubkey_str)
                print("Mnemonic:", mnemonic)
                print("Details saved to discovery.txt")
                save_discovery(mnemonic, pubkey_str)
                return True
        except Exception as e:
            print(f"Error: {e}")
        finally:
            with lock:
                progress.value += 1
                print(f"{progress.value}/{total_combinations} mnemonic combinations tried.", end='\r')
    return False

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    num_cores = int(input("Enter the number of CPU cores to use (0 for all available cores): "))
    if num_cores == 0:
        num_cores = multiprocessing.cpu_count()

    os.system('cls' if os.name == 'nt' else 'clear')
    words_string = input("Enter the 24-word seed phrase with spaces: ")
    words = words_string.strip().lower().split()

    if len(words) != 24:
        raise ValueError("Seed phrase must contain exactly 24 words.")

    wordlist = load_wordlist('words.txt')
    addresses = load_addresses('addresses.txt')

    derivation_path = "m/44'/501'/0'/0'"

    total_combinations = len(wordlist) * 24
    print(f"\nTotal possible combinations: {total_combinations}")

    manager = multiprocessing.Manager()
    progress = manager.Value('i', 0)
    lock = manager.Lock()
    discovered_keys = manager.list()

    for word_index in range(24):
        print(f"\nBruteforcing word position {word_index + 1}...")

        chunks = [(words, wordlist, addresses, word_index, progress, total_combinations, lock, discovered_keys, derivation_path)]

        with multiprocessing.Pool(processes=num_cores) as pool:
            results = pool.starmap(check_combinations, chunks)

        if any(results):
            break

    if not any(results):
        print("\nNo match found.")

    print("\nDiscovered public keys:")
    with open('discovered_keys.txt', 'a') as file:
        for key in discovered_keys:
            print(key)
            file.write(key + '\n')
