const StellarToken = artifacts.require("StellarToken");

module.exports = function (deployer) {
  deployer.deploy(StellarToken);
};
