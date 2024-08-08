import random
from itertools import product
from bip_utils import Bip39SeedGenerator
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import multiprocessing
import os

def load_wordlist(filename):
    with open(filename, 'r') as file:
        return [word.strip() for word in file]

def load_addresses(filename):
    with open(filename, 'r') as file:
        return [address.strip().lower() for address in file]

def generate_mnemonic(words):
    # Converts the list of words into a space-separated string
    mnemonic = ' '.join(words)
    return mnemonic

def mnemonic_to_keypair(mnemonic):
    # Generates a keypair from the mnemonic using bip_utils
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    keypair = Keypair.from_seed(seed_bytes[:32])
    return keypair

def keypair_to_private_key(keypair):
    # Access the private key bytes directly from the keypair
    private_key_bytes = keypair.secret()
    return private_key_bytes.hex()

def keypair_to_public_key(keypair):
    # Generate a public key from the keypair using solders
    public_key = str(keypair.pubkey())  # Converts Pubkey to base58 string
    return public_key.lower()

def is_valid_sol_address(address):
    try:
        Pubkey.from_string(address)
        return True
    except Exception as e:
        #print(f"Invalid Solana address: {address} (Error: {e})")
        return False

def save_discovery(mnemonic, private_key, public_key):
    # Save discovery details to file
    with open('discovery.txt', 'a') as file:  # Use 'a' to append instead of 'w' to overwrite
        file.write(f"Mnemonic: {mnemonic}\n")
        file.write(f"Private key: {private_key}\n")
        file.write(f"Public key: {public_key}\n")

def check_combinations(words, wordlist, addresses, word_index, progress, total_combinations, lock, discovered_keys):
    for word in wordlist:
        # Replace the word at word_index with a word from the wordlist
        temp_words = words[:]
        temp_words[word_index] = word

        # Generate mnemonic
        mnemonic = generate_mnemonic(temp_words)

        try:
            # Generate keypair from mnemonic
            keypair = mnemonic_to_keypair(mnemonic)

            # Generate private key from keypair
            private_key = keypair_to_private_key(keypair)

            # Generate public key from keypair
            public_key = keypair_to_public_key(keypair)

            # Validate public key
            if not is_valid_sol_address(public_key):
                continue

            # Add public key to discovered_keys
            with lock:
                discovered_keys.append(public_key)

            # Check if the generated public key matches any in the file
            if public_key in addresses:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n\nMatch found!\n")
                print("Public key:", public_key)
                print("Mnemonic:", mnemonic)
                print("Private key:", private_key)
                print("Details saved to discovery.txt \nIf you are finished, feel free to close the window, or let the program continue if you have multiple addresses.")
                # Save discovery details to file
                save_discovery(mnemonic, private_key, public_key)
                return True
        except Exception as e:
            # Ignore the error and continue with the next combination
            pass
        finally:
            with lock:
                progress.value += 1
                print(f"{progress.value}/{total_combinations} mnemonic combinations tried.", end='\r')
    return False

if __name__ == '__main__':
    # Input number of cores
    os.system('cls' if os.name == 'nt' else 'clear')
    num_cores = int(input("Enter the number of CPU cores to use (0 for all available cores): "))
    if num_cores == 0:
        num_cores = multiprocessing.cpu_count()

    # Input 24 words as a single string
    os.system('cls' if os.name == 'nt' else 'clear')
    words_string = input("Enter the 24-word seed phrase with spaces: ")
    words = words_string.strip().lower().split()

    if len(words) != 24:
        raise ValueError("Seed phrase must contain exactly 24 words.")

    # Load wordlist
    wordlist = load_wordlist('words.txt')

    # Load public keys from file
    addresses = load_addresses('addresses.txt')

    # Calculate the number of possible combinations
    total_combinations = 2048 * 24
    print(f"\nTotal possible combinations: {total_combinations}")

    manager = multiprocessing.Manager()
    progress = manager.Value('i', 0)
    lock = manager.Lock()
    discovered_keys = manager.list()

    for word_index in range(24):
        print(f"\nBruteforcing word position {word_index + 1}...")

        chunks = [(words, wordlist, addresses, word_index, progress, total_combinations, lock, discovered_keys)]

        with multiprocessing.Pool(processes=num_cores) as pool:
            results = pool.starmap(check_combinations, chunks)

        if any(results):
            break

    if not any(results):
        print("\nNo match found.")

    # Print and write all discovered public keys to a file
    print("\nDiscovered public keys:")
    with open('discovered_keys.txt', 'a') as file:
        for key in discovered_keys:
            print(key)
            file.write(key + '\n')
