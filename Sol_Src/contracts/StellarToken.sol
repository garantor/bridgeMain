// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StellarToken {
    string _name = "TELLAR";
    string _symbol = "TLR";
    uint8 _decimal = 18;
    uint256 _totalSupply;
    address private minter_owner;
    mapping(address => uint256) _balances;
    mapping(address => mapping(address => uint256)) private _allowances;


    event Transfer(
        address indexed _from, 
        address indexed _to, 
        uint256 _value
    );

    event Approval(address indexed owner, address indexed spender, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor(){
        minter_owner = msg.sender;
    }


    function name() public view returns(string memory) {
        return _name;
    }
    function symbol() public view returns(string memory) {
        return _symbol;
    }

    function decimals() public view returns (uint8) {
        return _decimal;
    }
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }
    function balanceOf(address _acct) public view returns(uint256 balance) {
        return _balances[_acct];
    }

    function owner() public view returns (address) {
        return minter_owner;
    }

    function transfer(address _to, uint256 _value ) public returns(bool) {
        _transfer(msg.sender, _to, _value);
        return true;
        
    }

    function _transfer(address _from, address _to,  uint256 _value) internal {
        require(_from != address(0), "ERC20: transfer from the zero address");
        require(_to != address(0), "ERC20: transfer to the zero address");
        uint _fromBalance = _balances[_from];
        require( _fromBalance >= _value, "Transfer Amount More that Sending Value");

        unchecked {
            _balances[_from] = _fromBalance - _value;
        }
        _balances[_to] += _value;

        emit Transfer(_from, _to, _value);
    }

    function transferFrom(address _from, uint256 _value, address _to) public returns(bool) {
        _transfer(_to, _from, _value);

        uint256 currentAllowance = _allowances[_from][msg.sender];
        require(currentAllowance >= _value, "ERC20: transfer amount exceeds allowance");
        unchecked {
            approve(_from, msg.sender, currentAllowance - _value);
        }

        return true;
        
    }

    function approve(address owner_add, address spender, uint256 amount) internal {
        require(owner_add != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[owner_add][spender] = amount;
        emit Approval(owner_add, spender, amount);
    }

    function allowance(address _owner, address spender) public view  returns (uint256) {
        return _allowances[_owner][spender];

    }


    function burn(address account, uint256 amount) public {
        require(account != address(0), "ERC20: burn from the zero address");


        uint256 accountBalance = _balances[account];
        require(accountBalance >= amount, "ERC20: burn amount exceeds balance");
        unchecked {
            _balances[account] = accountBalance - amount;
        }
        _totalSupply -= amount;

        emit Transfer(account, address(0), amount);
    }

    modifier onlyOwner() {
            require(owner() == msg.sender, "Ownable: caller is not the owner");
            _;
        }

    function renounceOwnership() public onlyOwner {
        _setOwner(address(0));
    }

    function transferOwnership(address newOwner) public  onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _setOwner(newOwner);
    }

    function _setOwner(address newOwner) private {
        address oldOwner = minter_owner;
        minter_owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }
    function mint(address to, uint256 _amt) public {
        require(msg.sender == minter_owner, "must have minter role to mint");
        _mint(to, _amt);
    }
    function _mint(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: mint to the zero address");


        _totalSupply += amount;
        _balances[account] += amount;
        emit Transfer(address(0), account, amount);
    }

}
