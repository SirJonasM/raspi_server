= Introduction
In this project we explored the efficency of Post Quantum Cryptography (PQC) Algorithms on Microcontroller.
Therefore we build a benchmark that tests choosen algorithms with real data.
We also wanted to include a completly different implementation that is written in Rust instead of C.

In the beginning we tried to run these algorithms on very lightweight systems like an ESP32 or even an ESP8266. See (Doc) for further Information.

This document will set the Focus on what the results of the finished project accomplished.

After we realized that it wont be as easy as thought to run PQC algorithms on these very lightweight systems we decided to focus on the Raspberry Pi implementation.
The implementation of the benchmark changed alot over the time of this project but always had the goal to create a real scenerio on how a embedded system would publish its data to a server while this beeing Post Quantum safe. The Realisation section goes over some mid level implementations.

Broken down to the communication of the server and client we wanted to achieve a communication like in @communication:
#figure(image("../figures/Benchmark.svg"), caption:[Communication of Server and Client])<communication>

As implementations of the Cryptography algorithms we used the PQClean library. 
For the Rust implementation we used the library kyber from Argyle-Software.
#line()
PQClean is a library providing clean, portable, and secure implementations of post-quantum cryptographic algorithms. It focuses on quantum-resistant encryption, key exchange, and digital signatures, following strict coding guidelines for security and auditability. The library includes implementations of NIST PQC standardization candidates while ensuring resistance to side-channel attacks. Written in standard C, it is designed for portability and ease of integration into security-critical applications. PQClean serves as a trusted foundation for developing and benchmarking post-quantum cryptography. 
