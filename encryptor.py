import base64
import zlib
import re

SECRET = b"secret!"

def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def encrypt(plain_text: str) -> str:
    compressed = zlib.compress(plain_text.encode("utf-8"))
    encrypted = xor_bytes(compressed, SECRET)
    return base64.b64encode(encrypted).decode("utf-8")

def main():
    print("[*] Reading source file aegisdroid_source.py...")
    try:
        with open("aegisdroid_source.py", "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print("[-] Error: aegisdroid_source.py not found!")
        return

    print("[*] Encrypting source code payload...")
    new_blob = encrypt(source_code)

    print("[*] Reading template wrapper aegisdroid.py...")
    try:
        with open("aegisdroid.py", "r", encoding="utf-8") as f:
            wrapper_content = f.read()
    except FileNotFoundError:
        print("[-] Error: aegisdroid.py not found!")
        return

    print("[*] Updating BLOB in wrapper...")
    # Matches: BLOB = "ANY_CHARS"
    pattern = r'(BLOB\s*=\s*")[^"]+(")'
    replacement = rf'\g<1>{new_blob}\g<2>'
    
    updated_wrapper, count = re.subn(pattern, replacement, wrapper_content)
    if count == 0:
        print("[-] Error: BLOB variable not found in aegisdroid.py!")
        return

    # Fix typo in the wrapper banner if present
    updated_wrapper = updated_wrapper.replace("Use For Eduaction Purpose Only", "Use For Educational Purpose Only")

    print("[*] Saving updated wrapper file...")
    with open("aegisdroid.py", "w", encoding="utf-8") as f:
        f.write(updated_wrapper)

    print("[+] Successfully obfuscated and updated aegisdroid.py!")

if __name__ == "__main__":
    main()
