import os
import subprocess
import json

nodes = 5

# genesis_block = {'config': {'chainId': 15, 'homesteadBlock': 0, 'eip150Block': 0, \
#   'eip155Block': 0, 'eip158Block': 0, 'byzantiumBlock': 0, 'constantinopleBlock': 0, \
#   'petersburgBlock': 0, 'ethash': {}}, \
#   'difficulty': '1', 'gasLimit': '8000000', \
#   'alloc': {'A0c21F3aC0b59e0C207eE9Bbc23364154075f54c': {'balance': '300000'}, \
#   }}

genesis_block = {
  "config": {
    "chainId": 15000,
    "homesteadBlock": 0,
    "eip150Block": 0,
    "eip155Block": 0,
    "eip158Block": 0,
    "byzantiumBlock": 0,
    "constantinopleBlock": 0,
    "petersburgBlock": 0,
    "clique": {
      "period": 5,
      "epoch": 30000
    }
  },
  "difficulty": "10",
  "gasLimit": "8000000",
  "extradata": "0x00000000000000000000000000000000000000000000000000000000000000007df9a875a174b3bc565e6424a0050ebc1b2d1d820000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  "alloc": {
    "7df9a875a174b3bc565e6424a0050ebc1b2d1d82": { "balance": "300000" }
    }
}

for i in range(nodes):
    print("======================> Creating node %d.."%(i,))
    datadir = "data%d"%(i, )
    os.mkdir(datadir)
    cmd = "geth account new --datadir %s --password password.txt"%(datadir,)
    subprocess.run(cmd.split(" "))
    keyfile = os.listdir(os.path.join(datadir, "keystore"))[0]
    with open(os.path.join(datadir, "keystore", keyfile)) as f:
        address = json.loads(f.read())["address"]
        print(address)
        genesis_block["alloc"][address] = {'balance': '300000'}
        if not i:
            # make first node as signer
            extradata = "0x0000000000000000000000000000000000000000000000000000000000000000%s0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"%(address, )
            genesis_block["extradata"] = extradata

print("========================> Writing Genesis block..")
print(genesis_block)
with open("genesis.json", "w") as f:
    f.write(json.dumps(genesis_block))

print("========================> Writing Data directories..")
# initialize data dir
for i in range(nodes):
    print("Creating node %d.."%(i,))
    datadir = "data%d"%(i, )
    cmd = "geth init --datadir %s genesis.json"%(datadir, )
    subprocess.run(cmd.split(" "))