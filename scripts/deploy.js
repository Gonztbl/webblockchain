async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);
  
  const election = await hre.ethers.deployContract("Election");

  await election.waitForDeployment();

  console.log(`Election contract deployed to ${election.target}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});