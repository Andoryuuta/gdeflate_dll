#ifndef GDEFLATEWRAPPER_H
#define GDEFLATEWRAPPER_H

#include <stddef.h>
#include <stdint.h>

#if defined(_MSC_VER)
#ifdef GDEFLATE_EXPORTS
#define GDEFLATE_API __declspec(dllexport)
#else
#define GDEFLATE_API __declspec(dllimport)
#endif
#else
#define GDEFLATE_API __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C"
{
#endif

    GDEFLATE_API bool
    gdeflate_get_uncompressed_size(uint8_t* input, uint64_t input_size, uint64_t* uncompressed_size);

    GDEFLATE_API uint64_t gdeflate_get_compress_bound(uint64_t size);

    GDEFLATE_API bool gdeflate_decompress(
        uint8_t* output,
        uint64_t output_size,
        uint8_t* input,
        uint64_t input_size,
        uint32_t num_workers);

    GDEFLATE_API bool gdeflate_compress(
        uint8_t* output,
        uint64_t* output_size,
        uint8_t* input,
        uint64_t input_size,
        uint32_t level,
        uint32_t flags);

#ifdef __cplusplus
}
#endif

#endif // GDEFLATEWRAPPER_H