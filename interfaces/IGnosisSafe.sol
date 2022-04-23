// SPDX-License-Identifier: LGPL-3.0-only
pragma solidity >=0.7.0 <0.9.0;

import "@safe-global/contracts/base/ModuleManager.sol";
import "@safe-global/contracts/base/OwnerManager.sol";
import "@safe-global/contracts/base/FallbackManager.sol";
import "@safe-global/contracts/base/GuardManager.sol";
import "@safe-global/contracts/common/EtherPaymentFallback.sol";
import "@safe-global/contracts/common/Singleton.sol";
import "@safe-global/contracts/common/SignatureDecoder.sol";
import "@safe-global/contracts/common/SecuredTokenTransfer.sol";
import "@safe-global/contracts/common/StorageAccessible.sol";
import "@safe-global/contracts/interfaces/ISignatureValidator.sol";
import "@safe-global/contracts/external/GnosisSafeMath.sol";

interface IGnosisSafe {
    function setup(
        address[] calldata _owners,
        uint256 _threshold,
        address to,
        bytes calldata data,
        address fallbackHandler,
        address paymentToken,
        uint256 payment,
        address payable paymentReceiver
    ) external;
}
