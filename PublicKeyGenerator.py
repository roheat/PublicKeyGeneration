Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 # The proven prime
Acurve = 0; Bcurve = 7 # These two defines the elliptic curve. y^2 = x^3 + Acurve * x + Bcurve
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
GPoint = (Gx,Gy) # Generator Point
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 # Number of points in the field
privKey = 0xA0DC65FFCA799873CBEA0AC274015B9526505DAAAED385155425F7337704883E # Replace with any private key

def modinv(a,b=Pcurve): #Extended Euclidean Algorithm/'division' in elliptic curves
    lm, hm = 1,0
    low, high = a%b,b
    while low > 1:
        ratio = high/low
        nm, new = hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % b

def ECAdd(a,b): # Point addition, invented for EC.
    LambdaAdd = ((b[1] - a[1]) * modinv(b[0] - a[0],Pcurve)) % Pcurve
    x = (LambdaAdd * LambdaAdd - a[0] - b[0]) % Pcurve
    y = (LambdaAdd * (a[0] - x) - a[1]) % Pcurve
    return (x,y)

def ECDouble(a): # Point Doubling, also invented for EC.
    LamdaDouble = ((3 * a[0] * a[0] + Acurve) * modinv((2 * a[1]), Pcurve)) % Pcurve
    x = (LamdaDouble * LamdaDouble - 2 * a[0]) % Pcurve
    y = (LamdaDouble * (a[0] - x) - a[1]) % Pcurve
    return (x,y)

def ECMultiply(GenPoint,privKeyHex): #Double & add. Not true multiplication
    if privKeyHex == 0 or privKeyHex >= N: raise Exception("Invalid Private Key")
    privKeyBin = str(bin(privKeyHex))[2:]
    Q=GenPoint
    for i in range (1, len(privKeyBin)):
        Q=ECDouble(Q);
        if privKeyBin[i] == "1":
            Q=ECAdd(Q,GenPoint);
    return (Q)

publicKey = ECMultiply(GPoint,privKey)
print "Private Key:";
print privKey; print
print "Public Key (uncompressed):";
print publicKey; print
print "Public Key (compressed):";
if publicKey[1] % 2 == 1: # If the Y coordinate of the Public Key is odd.
    print "03"+str(hex(publicKey[0])[2:-1]).zfill(64)
else: # If the Y coordinate is even.
    print "02"+str(hex(publicKey[0])[2:-1]).zfill(64)
