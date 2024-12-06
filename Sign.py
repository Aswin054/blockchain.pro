import matplotlib.pyplot as plt
import numpy as np
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
import webbrowser
import time

# Convert hex to binary for visualization
hex_data = bytes.fromhex("30450221009c185e79a9af94089c321cfc7bed36f00b5b3fa06d830fc40f4edb529e6d94a302206ee800f2a79d77afe16506bffee98895571d122b525486865377fac307c6747f01")
binary_data = np.unpackbits(np.frombuffer(hex_data, dtype=np.uint8))

# Plot as image
plt.imshow(binary_data.reshape(-1, 8), cmap="binary")
plt.title("Binary Visualization of Signature")
plt.show()

# Public key in compressed format (replace with actual public key if needed)
public_key_hex = "0381d31725526b08f59afe0725aded229d4f34d2b2902c1035ff5b454c3e6b00f9"
public_key_bytes = bytes.fromhex(public_key_hex)

# Load the ECC public key
public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), public_key_bytes)

# Example message to verify (replace with actual message that was signed)
message = b"Your original message here"

# Verify the signature
try:
    public_key.verify(
        hex_data,
        message,
        ec.ECDSA(hashes.SHA256())
    )
    print("Signature is valid.")
    
    # Add a slight delay before redirection to ensure the message is printed first
    time.sleep(2)
    
    # Redirect to a valid URL
    webbrowser.open('http://example.com')  # Redirect to your desired URL
except Exception as e:
    print(f"Signature verification failed: {e}")
    
    # Add a slight delay before redirection to ensure the error is printed first
    time.sleep(2)
    
    # Redirect to an error URL
    webbrowser.open('http://example.com/fail')  # Redirect to an error URL
