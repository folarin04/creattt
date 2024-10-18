
import pexpect

# Configuration
credentials = {
    "ip": '192.168.56.101',
    "username": 'prne',
    "password": 'cisco123!',
    "enable_password": 'class123!'
}

# Ask for the connection type
protocol = input("Enter the connection protocol (ssh/telnet): ").strip().lower()

def handle_ssh(session):
    """Handle SSH connection."""
    if session.expect(['Password:', 'continue connecting (yes/no)?', pexpect.TIMEOUT, pexpect.EOF]) == 1:
        session.sendline('yes')
        session.expect('Password:')
    
    session.sendline(credentials["password"])
    if session.expect(['>', '#', pexpect.TIMEOUT, pexpect.EOF]) == 0:
        session.sendline('enable')
        if session.expect(['Password:', '#', pexpect.TIMEOUT, pexpect.EOF]) == 0:
            session.sendline(credentials["enable_password"])
            session.expect('#')
    
    configure_device(session)

def handle_telnet(session):
    """Handle Telnet connection."""
    session.expect('Username:')
    session.sendline(credentials["username"])
    session.expect('Password:')
    session.sendline(credentials["password"])
    
    if session.expect(['>', '#', pexpect.TIMEOUT, pexpect.EOF]) == 0:
        session.sendline('enable')
        if session.expect(['Password:', '#', pexpect.TIMEOUT, pexpect.EOF]) == 0:
            session.sendline(credentials["enable_password"])
            session.expect('#')
    
    configure_device(session)

def configure_device(session):
    """Configure the device by setting the hostname."""
    session.sendline('configure terminal')
    session.expect(r'\(config\)#')
    session.sendline('hostname R1')
    session.expect(r'R1\(config\)#')
    session.sendline('exit')
    session.sendline('exit')
    session.close()
    print_success(protocol)

def print_success(protocol):
    """Print a success message."""
    print('---------------------------------------------')
    print(f'--- Success! {protocol.upper()} connection established to {credentials["ip"]}')
    print(f'    Username: {credentials["username"]}')
    print('---------------------------------------------')

# Main logic
if protocol == 'ssh':
    session = pexpect.spawn(f'ssh {credentials["username"]}@{credentials["ip"]}', encoding='utf-8', timeout=30)
    if session.expect(['Password:', 'continue connecting (yes/no)?', pexpect.TIMEOUT, pexpect.EOF]) not in [0, 1]:
        print(f'--- FAILURE! creating SSH session for {credentials["ip"]}. Error: {session.before}')
        exit()
    handle_ssh(session)

elif protocol == 'telnet':
    session = pexpect.spawn(f'telnet {credentials["ip"]}', encoding='utf-8', timeout=30)
    if session.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF]) != 0:
        print(f'--- FAILURE! creating Telnet session for {credentials["ip"]}. Error: {session.before}')
        exit()
    handle_telnet(session)

else:
    print("Invalid protocol selected. Please choose 'ssh' or 'telnet'.")
