# Hill-Climbing-Algorithm-for-breaching-Diffie-Hellman-key-exchange
This script is used for breaching Diffie-Hellman key exchange using stochastic hill climbing with random restarts. The algorithm actually tries to solve the NP-Complete problem (for small enough parameters) of the discrete logarithm, on which Diffie-Hellman key exchange (and also a vast majority of the public key cryptographic algorithms) are based.
The set of public parameters (**p** - prime modulus, **g** - primitive root modulo p, **A** - Alice's public key, **B** - Bob's public key) are stored in **dh_values.csv**.
The algorithm is then used to break the cipher and obtain **a** (private key of Alice) and **b** (private key of Bob).
