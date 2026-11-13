
#kryptografi

#två halvor - 
# Asymetrisk kryptografi | Symmetrisk kryptografi
# Kryptering
# signering
# Nyckeluthytor

#Sym - båda känner till något

# Asym - envägskomm, känner inte varann i förhand men vill komm säkert
#   This is unexpected that it works
#   Skicka en nyckel

#   signering -> verifieringsnyckel. 
#   Nyckelutbyten, genemsam sätt att uhhhh ge varandra saker?


# # Kryptering 
# - görs inte så ofta. often elektriska kurvor. high tech shenanigans

# E skickas
# D(E(x)) = x

# RSA (man brukar röra sig bort från detta)
# - Nya algorithmer för kryptering.


# RSA:
# två primtal: p, q - dessa är hemliga. Bara vi kan beräkna inversen
# n = p * q, publish. Värden får n.
# e (often 3), publish

# E(x) = x**e (mod n)
# D(x) = x**d (mod n)

# idea: (x**e)**d = x -> x**(ed) = x

# #how to find d?
# -> euler sats
# 	- x**(k*(p-1)*(q-1)) = 1 (mod pq)

# x = x**(k*(p-1)*(q-1) + 1)

# - Omvandla meddelande till tal.

# Kvantdatorer skulle räkna detta snabbt. 


# # Signering.
# RSa också. Brukar använda RSA för detta.

# E(D(x)) = x
# Vi skickar ut E. till världen.

# Får x och D(x) 
# Bara den med private nyckeln kan dekryptera D(x)

# E - verifiering
# D - signering.

# # Nyckelutbyten




# Diffe-Hellman

# Idk what title...
# p, random stor primtal
# g - generator. g = 2
# g**1, g**2, g**3, ..., g**(p-1), g**p


# få g**y kan hitta g**xy
# få g**x kan hitta g**yx
# like a for loop through x resp. y?



# oftast är krypto combine algorithm.


# - MITM
# -  

# - replay attack
# -  Nån slump unique per convo.

# - performance
# -  försöka gå över till sym krypto asap

# - Banken blir hackad
# -  Banken history. Find all E and V.
# -    Possibly ny nickel all times. thats too expensive.
# -  Banken tell everyone they've been hacekd.
# -  Limited certifikat.


# Vill inte kryptera. Takes much
# Better with nyckelutbyten cause thats less performance hihi hoho.
# Then u can use the g**x then fidn the y hihi hoho




# # symmatrisk krypto

# AES [storlek]:

# put into a 4x4 grid do inverterbara actoins on it to crypt
# to uncrypt just do reverse actions (do order in reverse and things invers?)


# ECB - används highkey aldrig cause osäkert.

# CBC - XOR in column to column. (column by column?) hahah
# slumpmässig IV

# CTR - give each column a number? still XOR


# Usually best kryptobibliotek is the one that only has one kryptering thats safe and reliable.




#alltid kryptering + signering.
#hashfunktioner...

#256
hash()
#isnt has like 


# AES - GCM :: This is a recommended combination. 


# RNG - random number generator. I didnt know woah.