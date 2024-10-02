const Election = artifacts.require("Election");
const Migrations = artifacts.require("Migrations");

module.exports = function (deployer) {
  deployer.deploy(Migrations).then(() => {
    return deployer.deploy(Election);
  });
};
