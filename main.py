#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT

A quantum cryptography exploitation framework.

MIT License

Copyright (c) 2025 Mauro Risonho de Paula Assumpção aka firebitsbr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Usage:
    python main.py
    python main.py --resource script.rc
    python main.py --console
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.cli import HoudinisConsole
from utils.banner import print_banner


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Houdinis Framework - Quantum Cryptography Exploitation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start interactive console
  python main.py --resource init.rc # Run resource script
  python main.py --quiet            # Start without banner
        """
    )
    
    parser.add_argument('--resource', '-r',
                       help='Resource script file to execute on startup')
    parser.add_argument('--console', '-c', action='store_true',
                       help='Force console mode (default)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress banner and startup messages')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    parser.add_argument('--version', action='version', version='Houdinis 1.0.0')
    
    return parser.parse_args()


def main():
    """Main entry point for Houdinis framework."""
    args = parse_arguments()
    
    try:
        # Display banner unless quiet mode
        if not args.quiet:
            print_banner()
        
        # Initialize console
        console = HoudinisConsole(debug=args.debug)
        
        # Execute resource script if provided
        if args.resource:
            console.execute_resource_script(args.resource)
        
        # Start interactive console
        console.cmdloop()
        
    except KeyboardInterrupt:
        print("\n[*] Houdinis terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Critical error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
