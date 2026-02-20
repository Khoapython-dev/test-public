#!/usr/bin/env python3
"""
Test script cho game turn-based
"""

import subprocess
import time

def test_game():
    """Test complete game flow"""
    test_input = """1
TestPlayer
1
1
1
1
1
1
1
1
1
1
4
2
3
2
TestPlayer
1
1
2
4
3
"""
    
    process = subprocess.Popen(
        ['python', 'src/main.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd='/workspaces/game',
        text=True,
        bufsize=1
    )
    
    stdout, stderr = process.communicate(input=test_input, timeout=120)
    
    print("=== STDOUT ===")
    print(stdout)
    print("\n=== STDERR ===")
    print(stderr)
    print("\n=== RETURN CODE ===")
    print(process.returncode)

if __name__ == "__main__":
    test_game()
