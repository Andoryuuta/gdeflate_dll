import ctypes
from ctypes import c_bool, c_uint8, c_uint32, c_uint64, POINTER, byref
from pathlib import Path
from typing import Union, Optional
from enum import IntEnum

class GDeflateCompressionLevel(IntEnum):
    """
    GDeflate compression levels that map to DirectStorage compression levels.
    """
    FASTEST = 1     # Maps to DSTORAGE_COMPRESSION_FASTEST
    DEFAULT = 9     # Maps to DSTORAGE_COMPRESSION_DEFAULT
    BEST_RATIO = 12 # Maps to DSTORAGE_COMPRESSION_BEST_RATIO

class GDeflateError(Exception):
    """Custom exception for GDeflate-related errors"""
    pass

class GDeflate:
    """
    A python interface for the GDeflate wrapper library.
    
    Args:
        dll_path (Union[str, Path], optional): Path to the GDeflate DLL. 
            Defaults to "GDeflateWrapper-x86_64.dll" in the current directory.
    
    Raises:
        GDeflateError: If the DLL cannot be loaded or if compression/decompression fails
    """
    
    # Expose compression levels as class attributes
    FASTEST = GDeflateCompressionLevel.FASTEST
    DEFAULT = GDeflateCompressionLevel.DEFAULT
    BEST_RATIO = GDeflateCompressionLevel.BEST_RATIO
    
    def __init__(self, dll_path: Union[str, Path] = "./GDeflateWrapper-x86_64.dll"):
        try:
            self._dll = ctypes.CDLL(str(dll_path))
        except OSError as e:
            raise GDeflateError(f"Failed to load GDeflate DLL: {e}")
        
        # bool gdeflate_get_uncompressed_size(
        #     uint8_t* input,
        #     uint64_t input_size,
        #     uint64_t* uncompressed_size);
        self._get_uncompressed_size_func = self._dll.gdeflate_get_uncompressed_size
        self._get_uncompressed_size_func.argtypes = [
            POINTER(c_uint8),  # input
            c_uint64,          # input_size
            POINTER(c_uint64)  # uncompressed_size
        ]
        self._get_uncompressed_size_func.restype = c_bool

        # bool gdeflate_decompress(
        #     uint8_t* output,
        #     uint64_t output_size,
        #     uint8_t* input,
        #     uint64_t input_size,
        #     uint32_t num_workers);
        self._decompress_func = self._dll.gdeflate_decompress
        self._decompress_func.argtypes = [
            POINTER(c_uint8),  # output
            c_uint64,          # output_size
            POINTER(c_uint8),  # input
            c_uint64,          # input_size
            c_uint32           # num_workers
        ]
        self._decompress_func.restype = c_bool

        # bool gdeflate_compress(
        #     uint8_t* output,
        #     uint64_t* output_size,
        #     uint8_t* input,
        #     uint64_t input_size,
        #     uint32_t level,
        #     uint32_t flags);
        self._compress_func = self._dll.gdeflate_compress
        self._compress_func.argtypes = [
            POINTER(c_uint8),  # output
            POINTER(c_uint64), # output_size
            POINTER(c_uint8),  # input
            c_uint64,          # input_size
            c_uint32,          # level
            c_uint32           # flags
        ]
        self._compress_func.restype = c_bool
    
    def get_uncompressed_size(self, compressed_data: Union[bytes, bytearray]) -> int:
        """
        Get the uncompressed size of compressed data.
        
        Args:
            compressed_data: The compressed data as bytes or bytearray
            
        Returns:
            int: The size of the data when uncompressed
            
        Raises:
            GDeflateError: If the size calculation fails
        """
        input_array = (c_uint8 * len(compressed_data))(*compressed_data)
        uncompressed_size = c_uint64(0)
        
        success = self._get_uncompressed_size_func(
            input_array,
            c_uint64(len(compressed_data)),
            byref(uncompressed_size)
        )
        
        if not success:
            raise GDeflateError("Failed to get uncompressed size")
        
        return uncompressed_size.value
    
    def decompress(self, 
                  compressed_data: Union[bytes, bytearray], 
                  num_workers: int = 1) -> bytes:
        """
        Decompress GDeflate-compressed data.
        
        Args:
            compressed_data: The compressed data as bytes or bytearray
            num_workers: Number of worker threads to use (default: 1)
            
        Returns:
            bytes: The decompressed data
            
        Raises:
            GDeflateError: If decompression fails
        """
        # Get the uncompressed size first
        output_size = self.get_uncompressed_size(compressed_data)
        
        # Prepare input and output buffers
        input_array = (c_uint8 * len(compressed_data))(*compressed_data)
        output_array = (c_uint8 * output_size)()
        
        success = self._decompress_func(
            output_array,
            c_uint64(output_size),
            input_array,
            c_uint64(len(compressed_data)),
            c_uint32(num_workers)
        )
        
        if not success:
            raise GDeflateError("Decompression failed")
        
        return bytes(output_array)
    
    def compress(self, 
                data: Union[bytes, bytearray], 
                level: Union[int, GDeflateCompressionLevel] = GDeflateCompressionLevel.DEFAULT, 
                flags: int = 0) -> bytes:
        """
        Compress data using GDeflate.
        
        Args:
            data: The data to compress as bytes or bytearray
            level: Compression level (default: DEFAULT). Use GDeflateCompressionLevel enum or class constants
            flags: Compression flags (default: 0)
            
        Returns:
            bytes: The compressed data
            
        Raises:
            GDeflateError: If compression fails
        """
        # Allocate output buffer (worst case: same size as input)
        output_size = c_uint64(len(data))
        output_array = (c_uint8 * len(data))()
        input_array = (c_uint8 * len(data))(*data)
        
        success = self._compress_func(
            output_array,
            byref(output_size),
            input_array,
            c_uint64(len(data)),
            c_uint32(int(level)),  # Convert enum to int if needed
            c_uint32(flags)
        )
        
        if not success:
            raise GDeflateError("Compression failed")
        
        # Return only the actual compressed bytes
        return bytes(output_array[:output_size.value])

# def main():
#     try:
#         # Initialize the wrapper
#         gdeflate = GDeflate()
        
#         # Example data
#         original_data = b"Hello, World!" * 1000
        
#         # Compress the data using different compression levels
#         compressed_fastest = gdeflate.compress(original_data, level=GDeflate.FASTEST)
#         print(f"Compressed size (fastest): {len(compressed_fastest)} bytes")
        
#         compressed_default = gdeflate.compress(original_data, level=GDeflate.DEFAULT)
#         print(f"Compressed size (default): {len(compressed_default)} bytes")
        
#         compressed_best = gdeflate.compress(original_data, level=GDeflate.BEST_RATIO)
#         print(f"Compressed size (best ratio): {len(compressed_best)} bytes")
        
#         uncompressed_size = gdeflate.get_uncompressed_size(compressed_best)
#         print(f"Uncompressed size: {uncompressed_size} bytes")

#         # Decompress and verify
#         decompressed = gdeflate.decompress(compressed_best, num_workers=4)
#         assert decompressed == original_data
#         print("Compression/decompression successful!")
        
#     except GDeflateError as e:
#         print(f"GDeflate error: {e}")
#     except Exception as e:
#         print(f"Unexpected error: {e}")

# if __name__ == "__main__":
#     main()