#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import signal
import atexit

def cleanup(xvfb_proc=None):
    """Clean up processes on exit."""
    try:
        # Kill Xvfb if it's running
        if xvfb_proc:
            xvfb_proc.terminate()
            xvfb_proc.wait()
        
        # Kill any remaining Xvfb processes
        subprocess.run(['pkill', 'Xvfb'], stderr=subprocess.DEVNULL)
    except:
        pass

def start_xvfb():
    """Start Xvfb display server."""
    try:
        # Kill any existing Xvfb processes
        subprocess.run(['pkill', 'Xvfb'], stderr=subprocess.DEVNULL)
        time.sleep(1)
        
        # Start Xvfb with specific options for better stability
        display_num = 99
        xvfb_cmd = [
            'Xvfb', 
            f':{display_num}', 
            '-screen', '0', '1024x768x24',
            '-ac',  # Disable access control
            '+extension', 'RANDR',
            '+render',
            '-noreset'
        ]
        
        # Start Xvfb and redirect output to /dev/null
        with open(os.devnull, 'w') as devnull:
            xvfb_proc = subprocess.Popen(
                xvfb_cmd,
                stdout=devnull,
                stderr=devnull
            )
        
        time.sleep(2)  # Wait for Xvfb to start
        
        # Test if Xvfb is running
        test_cmd = ['xdpyinfo', '-display', f':{display_num}']
        test_result = subprocess.run(test_cmd, capture_output=True)
        if test_result.returncode != 0:
            raise Exception("Failed to start Xvfb")
        
        # Register cleanup
        atexit.register(cleanup, xvfb_proc)
        
        return xvfb_proc, display_num
        
    except Exception as e:
        print(f"Error starting Xvfb: {e}")
        sys.exit(1)

def main():
    """Main entry point."""
    try:
        # Start Xvfb
        xvfb_proc, display_num = start_xvfb()
        
        # Set display
        os.environ['DISPLAY'] = f':{display_num}'
        
        # Run the application
        import main
        main.main()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup(xvfb_proc)

if __name__ == "__main__":
    main()
