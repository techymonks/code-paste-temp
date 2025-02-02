import itertools
import time
from mnemonic import Mnemonic
from eth_account import Account

# Known 6 words and their positions (you know the positions)
known_words = ["upper", "frown", "nest", "cause", "elegant", "banana"]
known_positions = [3, 6, 8, 9, 10, 11]  # The known positions of the 6 words (0-indexed)

# The total BIP39 word list
mnemonic = Mnemonic("english")
wordlist = mnemonic.wordlist

# Your exact Ethereum address that you're trying to match
target_address = "0x53a87bc7ec8c1e8baef57618b987e6aa40820927"  # Replace this with your actual Ethereum address

# Function to generate the full seed phrase and corresponding Ethereum address
def generate_eth_address(known_words, missing_positions):
    # Generate all combinations of the remaining positions
    missing_combinations = itertools.product(wordlist, repeat=len(missing_positions))
    
    for combo in missing_combinations:
        full_mnemonic = known_words[:]
        
        for pos, word in zip(missing_positions, combo):
            full_mnemonic.insert(pos, word)

        full_mnemonic_str = " ".join(full_mnemonic)
        private_key = mnemonic_to_private_key(full_mnemonic_str)

        # Generate the Ethereum address from the private key
        account = Account.privateKeyToAccount(private_key)
        address = account.address

        if address.lower() == target_address.lower():
            return full_mnemonic_str, private_key

    return None, None

# Function to convert mnemonic to private key
def mnemonic_to_private_key(mnemonic_str):
    seed = mnemonic.to_seed(mnemonic_str)
    private_key = Account.privateKeyToAccount(seed).privateKey
    return private_key

# Finding the missing words
missing_positions = [i for i in range(12) if i not in known_positions]

start_time = time.time()
mnemonic_str, private_key = generate_eth_address(known_words, missing_positions)

end_time = time.time()

if mnemonic_str:
    print(f"Found matching address! Seed phrase: {mnemonic_str}")
    print(f"Private Key: {private_key}")
else:
    print("No matching address found.")
    print(f"Total Time: {end_time - start_time} seconds")
