#! /bin/python

"""
Test multinode Iroha network with several mundane scenarios, with logging of outputs
This module assumes a fresh network, so make sure to run manage-network restart
Also note these tests are ordered. Some tests create objects that will be used by later tests
Do NOT employ pytest-random, as tests will fail. This is intended
"""
from binascii import hexlify
from operator import le
from IrohaUtils import *
from iroha import primitive_pb2
import pytest
import logging
import socket
import sys
import hashlib

def node_locations():
    return[
        (IROHA_HOST_ADDR_1, int(IROHA_PORT_1)),
        (IROHA_HOST_ADDR_2, int(IROHA_PORT_2)),
        (IROHA_HOST_ADDR_3, int(IROHA_PORT_3)),
        (IROHA_HOST_ADDR_4, int(IROHA_PORT_4)),
        (IROHA_HOST_ADDR_5, int(IROHA_PORT_5)),
    ]

@pytest.fixture(name="node_locations")
def node_locations_fixture():
    return node_locations()

def node_grpcs():
    return [net_1, net_2, net_3, net_4, net_5]

@pytest.fixture(name="node_grpcs")
def node_grpcs_fixture():
    return node_grpcs()

def test_node_reachable(node_locations):
    """
    Test that a node can be reached on the address:port specified
    """

    for i, location in enumerate(node_locations):
        logging.info(f"ATTEMPTING TO REACH NODE_{i+1}")
        logging.debug(f"Trying to reach location f{location}")
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a_socket.settimeout(5)
        conn_result = a_socket.connect_ex(location)
        a_socket.close()
        logging.debug(f"CONNECTION RESULT {conn_result}")
        assert conn_result == 0
        logging.info("\tCONNECTION SUCCESS")


def test_add_peer():
    """
    Test that a node with the necessary permissions can add a peer to the network
    """
    logging.info("ATTEMPTING TO ADD PEER")
    
    peer5 = primitive_pb2.Peer()
    peer5.address = '172.27.63.125:10005'
    peer5.peer_key = '1567a1dcdef946ee41fa456059b4f40652ffd5b104755862e7c80e938fd7795c'
    tx = iroha.transaction([
        iroha.command('AddPeer', peer=peer5)
    ], creator_account=ADMIN_ACCOUNT_ID, quorum=1)

    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("\tSUCCESSFULLY ADDED PEER")

def test_remove_peer():
    """
    Test that a node with the necessary permissions can remove a peer from the network
    """
    logging.info("ATTEMPTING TO REMOVE PEER")
    
    peer5 = primitive_pb2.Peer()
    peer5.address = '172.27.63.125:10005'
    peer5.peer_key = '1567a1dcdef946ee41fa456059b4f40652ffd5b104755862e7c80e938fd7795c'
    tx = iroha.transaction([
        iroha.command('RemovePeer', public_key=peer5.peer_key)
    ], creator_account=ADMIN_ACCOUNT_ID, quorum=1)

    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("\tSUCCESSFULLY REMOVED PEER")

def test_smart_contract():
    """
    Test that an admin can create a smart contract
    """
    logging.info("ATTEMPTING TO CREATE SMART CONTRACT")
    bytecode = ("608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550610632806100606000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c8063075461721461005157806327e235e31461006f57806340c10f191461009f578063d0679d34146100bb575b600080fd5b6100596100d7565b6040516100669190610398565b60405180910390f35b610089600480360381019061008491906103e4565b6100fb565b604051610096919061042a565b60405180910390f35b6100b960048036038101906100b49190610471565b610113565b005b6100d560048036038101906100d09190610471565b6101ea565b005b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60016020528060005260406000206000915090505481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161461016b57600080fd5b789f4f2726179a224501d762422c946590d91000000000000000811061019057600080fd5b80600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546101df91906104e0565b925050819055505050565b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205481111561026c576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161026390610571565b60405180910390fd5b80600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102bb9190610591565b9250508190555080600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825461031191906104e0565b925050819055507f3990db2d31862302a685e8086b5755072a6e2b5b780af1ee81ece35ee3cd334533838360405161034b939291906105c5565b60405180910390a15050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b600061038282610357565b9050919050565b61039281610377565b82525050565b60006020820190506103ad6000830184610389565b92915050565b600080fd5b6103c181610377565b81146103cc57600080fd5b50565b6000813590506103de816103b8565b92915050565b6000602082840312156103fa576103f96103b3565b5b6000610408848285016103cf565b91505092915050565b6000819050919050565b61042481610411565b82525050565b600060208201905061043f600083018461041b565b92915050565b61044e81610411565b811461045957600080fd5b50565b60008135905061046b81610445565b92915050565b60008060408385031215610488576104876103b3565b5b6000610496858286016103cf565b92505060206104a78582860161045c565b9150509250929050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b60006104eb82610411565b91506104f683610411565b925082820190508082111561050e5761050d6104b1565b5b92915050565b600082825260208201905092915050565b7f496e73756666696369656e742062616c616e63652e0000000000000000000000600082015250565b600061055b601583610514565b915061056682610525565b602082019050919050565b6000602082019050818103600083015261058a8161054e565b9050919050565b600061059c82610411565b91506105a783610411565b92508282039050818111156105bf576105be6104b1565b5b92915050565b60006060820190506105da6000830186610389565b6105e76020830185610389565b6105f4604083018461041b565b94935050505056fea264697066735822122053242a9225937cac6a5e8abe08967604680fb9461014726b932c737c53f0559b64736f6c63430008110033")
    tx = iroha.transaction([
        iroha.command('CallEngine', caller='admin@test', input=bytecode)
    ], creator_account=ADMIN_ACCOUNT_ID)
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("\tSUCCESSFULLY CREATED CONTRACT")

def test_call_contract():

    k= hashlib.sha3_256()
    k.update(b'admin@test')
    address = hexlify(k.digest()[12:32]).zfill(64)

    params = ("40c10f19"                                                          # selector
          "000000000000000000000000f205c4a929072dd6e7fc081c2a78dbc79c76070b"  # address
          "00000000000000000000000000000000000000000000000000000000000003e8"  # amount
         )

    tx = iroha.transaction([
        iroha.command('CallEngine', caller="admin@test", callee="f205c4a929072dd6e7fc081c2a78dbc79c76070b", input=params)
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("\tSUCCESSFULLY USED MINT FUNCTION")

if __name__=="__main__":
    #logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("STARTING BASIC NETWORK TESTS")

    input(f"{bcolors.OKGREEN}Test if all nodes are reachable on Iroha ports{bcolors.ENDC}")
    test_node_reachable(node_locations())
    print(f"{'-'*80}\n\n")

    # input(f"{bcolors.OKGREEN}Test if node can add a peer{bcolors.ENDC}")
    # test_add_peer()
    # print(f"{'-'*80}\n\n")
    
    # input(f"{bcolors.OKGREEN}Test if node can remove a peer{bcolors.ENDC}")
    # test_remove_peer()
    # print(f"{'-'*80}\n\n")

    input(f"{bcolors.OKGREEN}Test create smart contract{bcolors.ENDC}")
    test_smart_contract()
    print(f"{'-'*80}\n\n")

    input(f"{bcolors.OKGREEN}Test cal smart contract{bcolors.ENDC}")
    test_call_contract()
    print(f"{'-'*80}\n\n")

    # input(f"{bcolors.OKGREEN}Test if admin can create a domain{bcolors.ENDC}")
    # test_create_domain()
    # print(f"{'-'*80}\n\n")

    # input(f"{bcolors.OKGREEN}Test if an admin can create an asset in the new domain{bcolors.ENDC}")
    # test_create_asset()
    # print(f"{'-'*80}\n\n")

    # input(f"{bcolors.OKGREEN}Test if an admin can add the new asset to their account{bcolors.ENDC}")
    # test_add_asset()
    # print(f"{'-'*80}\n\n")

    # input(f"{bcolors.OKGREEN}Test if an admin can create new users, using each node{bcolors.ENDC}")
    # test_create_users(node_grpcs())
    # print(f"{'-'*80}\n\n")

    # input(f"{bcolors.OKGREEN}Test if an admin can transfer the new asset to each new account{bcolors.ENDC}")
    # test_transfer_asset_to_users(node_grpcs())
    # print(f"{'-'*80}\n\n")

    # input(f"{bcolors.OKGREEN}Test if an admin can query the new asset on each node{bcolors.ENDC}")
    # test_query_on_asset(node_grpcs())
    # print(f"{'-'*80}\n\n")

    logging.debug("FINISHED BASIC NETWORK TESTS")
    logging.debug("SAVING LOGS TO network_testing DIRECTORY")

    logging.info("SAVE BLOCKCHAIN LOGS TO network_testing_logs/")
    for i, grpc in enumerate(node_grpcs()):
        logging.info(f"\tSAVING LOGS OF node{i+1}")
        log_all_blocks(grpc, f"node{i+1}.log", "network_testing_logs")
