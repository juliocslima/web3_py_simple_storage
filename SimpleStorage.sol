// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // this will get initialized to 0!
    uint256 public favoriteNumber;

    bool favoriteBool = false;
    string favoriteString = "String";
    int256 favoriteInt = -5;
    address favoriteAddress = 0x02686E30B8f2226f9090Fe35f42e282FCc7c1cE7;
    bytes32 favoriteBytes = "cat";

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;

    mapping(string => uint256) public nameToFavoriteNumber;

    People public person = People({favoriteNumber: 2, name: "Julio"});

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));

        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
