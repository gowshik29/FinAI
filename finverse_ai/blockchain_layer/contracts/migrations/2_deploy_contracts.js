const FinanceLedger = artifacts.require("FinanceLedger");

module.exports = function (deployer) {
  deployer.deploy(FinanceLedger);
};
