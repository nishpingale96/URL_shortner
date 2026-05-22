import string

class Base62Converter:
    # 1. Define the alphabet: 0-9, a-z, A-Z (62 characters total)
    # The order remains immutable to maintain consistent mathematical mappings.
    ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
    BASE = len(ALPHABET)

    @classmethod
    def encode(cls, num: int) -> str:
        """
        Converts an auto-incremented base-10 integer into a Base62 string string.
        """
        if num == 0:
            return cls.ALPHABET[0]

        arr = []
        while num > 0:
            num, rem = divmod(num, cls.BASE)
            arr.append(cls.ALPHABET[rem])
        
        # Reverse the array because the last remainder calculated is the most significant digit
        return "".join(reversed(arr))

    @classmethod
    def decode(cls, b62_str: str) -> int:
        """
        Converts a Base62 string code back into its original base-10 integer ID.
        """
        num = 0
        for char in b62_str:
            # Reconstruct the base-10 number based on character positional weight
            num = num * cls.BASE + cls.ALPHABET.index(char)
        return num


# --- Verification & Testing Suite ---
if __name__ == "__main__":
    print("--- Running Base62 Verification Suite ---")

    # Test cases representing low, mid, and high auto-incrementing DB IDs
    test_ids = [1, 61, 62,72, 134,1000123, 9999999999,]

    for original_id in test_ids:
        # Step A: Encode the integer ID to a short code
        short_code = Base62Converter.encode(original_id)
        
        # Step B: Decode the short code back to an integer ID
        decoded_id = Base62Converter.decode(short_code)
        
        print(f"ID: {original_id:<12} -> Short Code: {short_code:<8} -> Decoded ID: {decoded_id}")
        
        # Operational Check
        assert original_id == decoded_id, f"Mismatch found! Original: {original_id}, Decoded: {decoded_id}"

    print("\n✓ Verification successful. Mathematical consistency confirmed.")