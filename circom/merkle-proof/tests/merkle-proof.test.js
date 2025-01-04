import { Circomkit } from "circomkit";

describe("MerkleProof Circuit", function() {
  let circuit;

  before(async function() {
    const circomkit = new Circomkit();
    circuit = await circomkit.WitnessTester("MerkleProof", {
      file: "MerkleProof",
      template: "MerkleProof",
      params: [2],
    });
  });

  it("should correctly verify a valid Merkle path", async function() {
    const input = {
      leaf: 1n,
      root: BigInt("39953118817961288012830084854690778208484492054656773438522855405320771733761"),
      pathElements: [BigInt(1), BigInt("38469288157622981154441112836102256380519124992171477510678100300226603366940")],
      pathIndices: [1, 0],
    };

    const output = {};
    await circuit.expectPass(input, output);
  });
});
