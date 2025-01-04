import { buildPoseidonOpt } from "circomlibjs";

// TODO: Poseidon implementation from circomlibjs seems to differ from the one from circomlib.
// Although parameters are the same, the order of operation is slightly different.
async function buildMerkleTree(leaves, depth) {
  const poseidonOpt = await buildPoseidonOpt();
  const poseidonHash = (left, right) => poseidonOpt([left, right]);

  const tree = [leaves.map(BigInt)];
  for (let level = 0; level < depth; level++) {
    const prevLayer = tree[level];
    const nextLayer = [];
    for (let i = 0; i < prevLayer.length; i += 2) {
      const left = prevLayer[i];
      const right = i + 1 < prevLayer.length ? prevLayer[i + 1] : left;
      nextLayer.push(poseidonHash(left, right));
    }
    tree.push(nextLayer);
  }
  return tree;
}

function generateMerkleProof(leafIndex, tree) {
  const proof = {
    pathElements: [],
    pathIndices: [],
    root: null,
  };

  let index = leafIndex;

  for (let level = 0; level < tree.length - 1; level++) {
    const layer = tree[level];
    const siblingIndex = index % 2 === 0 ? index + 1 : index - 1;

    let sibling = layer[siblingIndex] ?? layer[index];
    if (sibling instanceof Uint8Array) {
      sibling = bytesToBigInt(sibling);
    }

    proof.pathElements.push(sibling);
    proof.pathIndices.push(index % 2 === 0 ? 0 : 1);
    index = Math.floor(index / 2);
  }

  const rootBytes = tree[tree.length - 1][0];
  proof.root = bytesToBigInt(rootBytes);
  return proof;
}

function bytesToBigInt(bytes) {
  return BigInt(
    "0x" +
    Array.from(bytes)
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("")
  );
}

(async () => {
  const leaves = [1, 2, 3, 4];
  const depth = 2;
  const tree = await buildMerkleTree(leaves, depth);

  const leafIndex = 0;
  const proof = generateMerkleProof(leafIndex, tree);

  console.log("Proof: ", proof);
})();

