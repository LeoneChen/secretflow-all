import secretflow as sf

cluster_config = {
    'parties': {
        'alice': {'address': '0.0.0.0:20001'},
        'bob': {'address': '0.0.0.0:30001'},
        'carol': {'address': '0.0.0.0:40001'},
    },
    'self_party': 'bob',
}

party_key_pair = {
    'alice': {'private_key': './private_key.pem', 'public_key': './public_key.pem'}
}


auth_manager_config = {
    'host': '0.0.0.0:8835',
    'mr_enclave': '4c1c23a3dd87a407035b81e147e4ca64057bac51d06df71ec90ba5378ee1c62f',
}

# Connect to Alice's ray
sf.init(
    address='local',
    cluster_config=cluster_config,
    party_key_pair=party_key_pair,
    auth_manager_config=auth_manager_config,
    tee_simulation=False,
)


import numpy as np

def average(data):
    return np.average(data, axis=1)

from secretflow.device import TEEU

alice = sf.PYU('alice')
bob = sf.PYU('bob')
teeu = TEEU('carol', mr_enclave='111658e7b79442531907dc24a9aec040a06078a350393dcf53f5f32a8d8f83b6')

a = alice(lambda: np.random.rand(4, 3))()
b = bob(lambda: np.random.rand(4, 3))()
a_teeu = a.to(teeu, allow_funcs=average)
b_teeu = b.to(teeu, allow_funcs=average)

avg_val = teeu(average)([a_teeu, b_teeu])
print(sf.reveal(avg_val))


a = sf.reveal(a)
b = sf.reveal(b)
np.testing.assert_equal(avg_val, average([a, b]) )