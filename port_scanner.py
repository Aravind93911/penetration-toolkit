import click
import socket
from .modules.port_scanner import scan_ports
from .modules.brute_force import run_brute_force

# --- Main Command Group using Click ---

@click.group()
def cli():
    """
    PyTestKit: A Modular Penetration Testing Toolkit.
    
    Use 'pytestkit [COMMAND] --help' for command-specific options.
    """
    pass

# --- 1. Port Scanner Command ---

@cli.command(name='scan')
@click.option('--target', required=True, help='The target IP address or hostname to scan.')
@click.option('--start', default=1, type=int, help='The starting port number (inclusive).')
@click.option('--end', default=1024, type=int, help='The ending port number (inclusive).')
def scan_command(target, start, end):
    """
    Scans a range of TCP ports on the specified target.
    """
    if start < 1 or end > 65535 or start > end:
        click.echo(" [!] Error: Invalid port range. Ports must be between 1 and 65535, and START must be <= END.")
        return
        
    try:
        scan_ports(target, start, end)
    except Exception as e:
        click.echo(f" [!] An unexpected error occurred during scan: {e}")


# --- 2. Brute Force Command ---

@cli.command(name='brute')
@click.option('--user', required=True, help='The target username for the brute force simulation.')
@click.option('--wordlist', required=True, help='Path to the password dictionary file.')
def brute_command(user, wordlist):
    """
    Simulates a password brute force attack using a wordlist.
    (Note: Uses a safe, mock login function for demonstration.)
    """
    try:
        run_brute_force(user, wordlist)
    except Exception as e:
        click.echo(f" [!] An unexpected error occurred during brute force simulation: {e}")


# --- Toolkit Initialization ---

if __name__ == '__main__':
    # To run the CLI, execute 'python pentoolkit/main.py' 
    # and pass the desired commands and options.
    cli()
# Placeholder for port_scanner.py
