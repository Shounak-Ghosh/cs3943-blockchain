import time
import matplotlib.pyplot as plt

def djb2_xor_hash(s: str) -> int:
    """Modified djb2 hash function using XOR instead of addition."""
    hash_value = 5381  # Initial hash value
    for char in s:
        hash_value = ((hash_value << 5) + hash_value) ^ ord(char)  # hash * 33 XOR char
    return hash_value

# ------------------ TESTS ------------------

def test_uniform_distribution(hash_function, num_samples=10000):
    """Test if the hash function distributes values evenly."""
    hashes = [hash_function(f"string_{i}") % num_samples for i in range(num_samples)]
    
    plt.hist(hashes, bins=50, edgecolor="black")
    plt.xlabel("Hash Value Modulo num_samples")
    plt.ylabel("Frequency")
    plt.title("Hash Function Distribution Test")
    plt.show(block=False)
    plt.pause(5)
    plt.close()

def test_collisions(hash_function, num_samples=10000):
    """Test how often the hash function produces collisions."""
    hash_set = set()
    collisions = 0
    
    for i in range(num_samples):
        h = hash_function(f"string_{i}")
        if h in hash_set:
            collisions += 1
        else:
            hash_set.add(h)
    
    print(f"Collisions: {collisions} / {num_samples}")

def test_avalanche(hash_function, input_str):
    """Test if a small change (one character modification) causes a large hash difference."""
    if len(input_str) < 2:
        print("Input string is too short for an effective avalanche test.")
        return

    # Compute original hash
    hash1 = hash_function(input_str)

    # Modify the middle character slightly
    mid_index = len(input_str) // 2
    modified_char = chr(ord(input_str[mid_index]) + 1)  # Increase ASCII value by 1
    modified_str = input_str[:mid_index] + modified_char + input_str[mid_index + 1:]

    # Compute hash for modified string
    hash2 = hash_function(modified_str)

    # Calculate bitwise difference
    bit_diff = bin(hash1 ^ hash2).count('1')

    print(f"Original String:  '{input_str}'")
    print(f"Modified String:  '{modified_str}'")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Bitwise Difference: {bit_diff} bits changed")

def test_speed(hash_function, num_samples=100000):
    """Measure execution time of the hash function."""
    start = time.time()
    for i in range(num_samples):
        hash_function(f"string_{i}")
    end = time.time()
    
    print(f"Time taken for {num_samples} hashes: {end - start:.5f} seconds")

# ------------------ RUN TESTS ------------------

if __name__ == "__main__":
    test_strings = ["hello", "world", "Hello", "hash", "function"]
    
    print("\n--- Testing Hash Function Outputs ---")
    for s in test_strings:
        print(f"Hash of '{s}': {djb2_xor_hash(s)}")
    
    print("\n--- Running Uniform Distribution Test ---")
    test_uniform_distribution(djb2_xor_hash)

    print("\n--- Running Collision Test ---")
    test_collisions(djb2_xor_hash)

    print("\n--- Running Avalanche Effect Test ---")
    test_avalanche(djb2_xor_hash, "hello")

    print("\n--- Running Speed Test ---")
    test_speed(djb2_xor_hash)
