require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28", // Đảm bảo phiên bản này khớp với pragma của bạn
  networks: {
    // Mạng này sẽ được sử dụng khi bạn chạy 'npx hardhat node'
    hardhat: {
      chainId: 1337 // ID chuỗi tiêu chuẩn cho mạng local
    }
  },
  paths: {
    artifacts: './build' // Chỉ cho Hardhat lưu artifacts vào thư mục 'build' giống Truffle
  }
};