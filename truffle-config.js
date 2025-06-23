module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,           // 👈 use 7545 instead of 8545
      network_id: "5777",      // Match any network ID
    },
  },
  contracts_build_directory: "./build/contracts",
  compilers: {
    solc: {
      version: "0.8.21",
    },
  },
};