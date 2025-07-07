//SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Election {

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    bool public goingon = true; // Thêm public để dễ kiểm tra từ bên ngoài
    address public owner;

    mapping(address => bool) public voters;
    // Đây là một mảng động (dynamic array), không phải mapping
    Candidate[] public candidates; 
    
    // không cần biến candidatesCount nữa, vì mảng đã có thuộc tính .length
    uint public totalVote = 0;

constructor () {
    owner = msg.sender;
    candidates.push(Candidate(0, "De 1", 0));
    candidates.push(Candidate(1, "De 2", 0));
    candidates.push(Candidate(2, "De 3", 0));
}

    // Không cần hàm addCandidate riêng nữa nếu chỉ khởi tạo trong constructor

    function end () public {
        require(msg.sender == owner , "ONLY OWNER CAN END");
        goingon = false;
    }

    // _candidateId bây giờ là chỉ số của mảng (0, 1, hoặc 2)
    function vote (uint _candidateId) public {
        require(!voters[msg.sender], "Already voted");

        // Kiểm tra xem chỉ số có hợp lệ không (phải nhỏ hơn độ dài mảng)
        require(_candidateId < candidates.length, "Invalid candidate");

        require(goingon, "Election ended");

        voters[msg.sender] = true;

        candidates[_candidateId].voteCount++;
        totalVote++;
    }

    // Hàm tiện ích để lấy số lượng ứng viên
    function getCandidatesCount() public view returns (uint) {
        return candidates.length;
    }
}