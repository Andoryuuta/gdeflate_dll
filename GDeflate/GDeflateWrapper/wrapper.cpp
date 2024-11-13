#include "wrapper.h"

#include <GDeflate.h>
#include <TileStream.h>

extern "C"
{

    bool gdeflate_get_uncompressed_size(uint8_t* input, uint64_t input_size, uint64_t* uncompressed_size)
    {
        if (input_size < sizeof(GDeflate::TileStream))
        {
            *uncompressed_size = 0;
            return false;
        }

        auto ts_header = reinterpret_cast<const GDeflate::TileStream*>(input);
        *uncompressed_size = ts_header->GetUncompressedSize();
        return true;
    }

    bool gdeflate_decompress(
        uint8_t* output,
        uint64_t output_size,
        uint8_t* input,
        uint64_t input_size,
        uint32_t num_workers)
    {
        return GDeflate::Decompress(output, output_size, input, input_size, num_workers);
    }

    bool gdeflate_compress(
        uint8_t* output,
        uint64_t* output_size,
        uint8_t* input,
        uint64_t input_size,
        uint32_t level,
        uint32_t flags)
    {
        return GDeflate::Compress(output, output_size, input, input_size, level, flags);
    }
}