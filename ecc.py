from nacl.signing import SigningKey
from nacl.signing import VerifyKey
import hashlib


def hashing_function(entity):
        h = hashlib.sha256()
        h.update(str(entity).encode())
        return h.hexdigest()
    
def generate_signature(ckp_msg):
    sig_key = SigningKey.generate()
    sig_ckp = sig_key.sign(str(ckp_msg).encode())
    verify_key = sig_key.verify_key
    public_key = verify_key.encode()
    rckp_msg = sig_ckp +(b'split')+  public_key
    return rckp_msg

def generate_verfiy(public_key,recv_msg):
    verify_key = VerifyKey(public_key)
    msg_recv  = verify_key.verify(recv_msg).decode()
    return msg_recv
    
    