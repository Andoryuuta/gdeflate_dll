import argparse
from pathlib import Path
import sys
from typing import Optional

from gdeflate import GDeflate, GDeflateCompressionLevel, GDeflateError

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compress or decompress files using GDeflate")
    
    parser.add_argument("input", type=Path,
                      help="Input file path")
    parser.add_argument("output", type=Path,
                      help="Output file path")
    
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("-c", "--compress",
                          action="store_true",
                          help="Compress the input file")
    action_group.add_argument("-d", "--decompress",
                          action="store_true",
                          help="Decompress the input file")
    
    parser.add_argument("-l", "--level",
                      type=int,
                      choices=[1, 9, 12],
                      default=GDeflateCompressionLevel.DEFAULT,
                      help="Compression level (1=fastest, 9=default, 12=best)")
    
    parser.add_argument("-w", "--workers",
                      type=int,
                      default=1,
                      help="Number of worker threads for decompression")
    
    parser.add_argument("--dll",
                      type=Path,
                      default="./GDeflateWrapper-x86_64.dll",
                      help="Path to GDeflate DLL")
    
    return parser.parse_args()

def compress_file(gdeflate: GDeflate, 
                 input_path: Path, 
                 output_path: Path, 
                 level: int) -> None:
    """Compress a file using GDeflate"""
    try:
        with open(input_path, "rb") as f:
            input_data = f.read()
        
        compressed = gdeflate.compress(input_data, level=level)
        
        with open(output_path, "wb") as f:
            f.write(compressed)
            
        orig_size = len(input_data)
        comp_size = len(compressed)
        ratio = (comp_size / orig_size) * 100
        
        print(f"Compressed {input_path}")
        print(f"Original size: {orig_size:,} bytes")
        print(f"Compressed size: {comp_size:,} bytes")
        print(f"Compression ratio: {ratio:.1f}%")
        
    except IOError as e:
        print(f"Error accessing file: {e}", file=sys.stderr)
        sys.exit(1)

def decompress_file(gdeflate: GDeflate, 
                   input_path: Path, 
                   output_path: Path, 
                   num_workers: int) -> None:
    """Decompress a file using GDeflate"""
    try:
        with open(input_path, "rb") as f:
            input_data = f.read()
            
        decompressed = gdeflate.decompress(input_data, num_workers=num_workers)
        
        with open(output_path, "wb") as f:
            f.write(decompressed)
            
        comp_size = len(input_data)
        decomp_size = len(decompressed)
        ratio = (comp_size / decomp_size) * 100
        
        print(f"Decompressed {input_path}")
        print(f"Compressed size: {comp_size:,} bytes")
        print(f"Decompressed size: {decomp_size:,} bytes")
        print(f"Compression ratio was: {ratio:.1f}%")
        
    except IOError as e:
        print(f"Error accessing file: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    args = parse_args()
    
    try:
        gdeflate = GDeflate(args.dll)
        
        if args.compress:
            compress_file(gdeflate, args.input, args.output, args.level)
        else:
            decompress_file(gdeflate, args.input, args.output, args.workers)
            
    except GDeflateError as e:
        print(f"GDeflate error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()