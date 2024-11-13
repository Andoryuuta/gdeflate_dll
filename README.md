# gdeflate_dll

This is a fork of the https://github.com/microsoft/DirectStorage/ repo, extended with a small shared library to wrap/expose the reference implementation of GDeflate.

## Interface
The DLL wrapper exports the three following functions:
```c
// Calculates the uncompressed size of the provided raw gdeflate-compressed blob.
// Returns true on success. 
bool gdeflate_get_uncompressed_size(
    uint8_t* input,
    uint64_t input_size,
    uint64_t* uncompressed_size);

// Decompresses the provided input.
// The output buffer size should be the uncompressed size (from gdeflate_get_uncompressed_size) at minimum.
// Returns true on success. 
bool gdeflate_decompress(
    uint8_t* output,
    uint64_t output_size,
    uint8_t* input,
    uint64_t input_size,
    uint32_t num_workers);

// Compresses the provided input.
// Returns true on success.
bool gdeflate_compress(
    uint8_t* output,
    uint64_t* output_size,
    uint8_t* input,
    uint64_t input_size,
    uint32_t level,
    uint32_t flags);
```