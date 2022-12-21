# Import the necessary modules
from iroha import IrohaCrypto

# Generate the key pair
priv_key = IrohaCrypto.private_key()
pub_key = IrohaCrypto.derive_public_key(priv_key)

# # Encode the keys as multihash strings
# priv_key_multihash = IrohaCrypto.to_multihash(priv_key)
# pub_key_multihash = IrohaCrypto.to_multihash(pub_key)

# Print the keys
print("Private key (multihash):", priv_key)
print("Public key (multihash):", pub_key)