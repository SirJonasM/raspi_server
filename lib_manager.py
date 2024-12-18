import ctypes
dilithium2_lib = ctypes.CDLL('./build/crypto_sign/libdilithium2.so')
dilithium3_lib = ctypes.CDLL('./build/crypto_sign/libdilithium3.so')
dilithium5_lib = ctypes.CDLL('./build/crypto_sign/libdilithium5.so')
falcon_512_lib = ctypes.CDLL('./build/crypto_sign/libfalcon-512.so')
falcon_1024_lib = ctypes.CDLL('./build/crypto_sign/libfalcon-1024.so')
rainbowIclassic_lib = ctypes.CDLL('./build/crypto_sign/librainbowI-classic.so')
rainbowIIIclassic_lib = ctypes.CDLL('./build/crypto_sign/librainbowIII-classic.so')
rainbowVclassic_lib = ctypes.CDLL('./build/crypto_sign/librainbowV-classic.so')
