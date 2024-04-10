import secretflow as sf
import jax.numpy as jnp
import spu

cluster_config = {
    "parties": {
        "alice": {
            # replace with alice's real address.
            "address": "202.112.47.76:40001",
        },
        "bob": {
            # replace with bob's real address.
            "address": "202.112.47.77:40001",
        },
    },
    "self_party": "bob",
}

cluster_def = {
    "nodes": [
        {
            "party": "alice",
            "address": "202.112.47.76:40002",
        },
        {
            "party": "bob",
            "address": "202.112.47.77:40002",
        },
    ],
    "runtime_config": {
        "protocol": spu.spu_pb2.SEMI2K,
        "field": spu.spu_pb2.FM128,
    },
}

sf.init(address="202.112.47.77:40000", cluster_config=cluster_config)

alice, bob = sf.PYU("alice"), sf.PYU("bob")
spu = sf.SPU(cluster_def=cluster_def)


def compare(a, b):
    return a > b


def get_alice_data():
    return 2


def get_bob_data():
    return 11


# Pass data to PYU
data_alice = alice(get_alice_data)()
data_bob = bob(get_bob_data)()

# Perform privacy computation on SPU
result = spu(compare)(data_alice, data_bob)

# Reveal results
revealed_result = sf.reveal(result)

# Print revealed result
print(f"Result: {revealed_result}")

# Clean environment
sf.shutdown()
