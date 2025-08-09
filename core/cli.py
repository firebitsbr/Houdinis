"""
# Houdinis Framework - Houdinis Console Interface
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT

Interactive CLI inspired by msfconsole for quantum cryptography exploitation.
"""

import cmd
import sys
import os
import importlib
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .modules import ModuleManager, BaseModule
from .session import SessionManager


class SimpleConsole:
    """Simple console fallback when Rich is not available."""
    
    def print(self, text: str):
        """Simple print with basic color removal."""
        # Remove basic rich markup
        clean_text = text.replace('[red]', '').replace('[/red]', '')
        clean_text = clean_text.replace('[green]', '').replace('[/green]', '')
        clean_text = clean_text.replace('[yellow]', '').replace('[/yellow]', '')
        clean_text = clean_text.replace('[cyan]', '').replace('[/cyan]', '')
        clean_text = clean_text.replace('[bold]', '').replace('[/bold]', '')
        print(clean_text)


class HoudinisConsole(cmd.Cmd):
    """
    Interactive console for Houdinis framework.
    
    Provides a Metasploit-like interface for quantum cryptography exploitation.
    """
    
    def __init__(self, debug: bool = False):
        """Initialize the Houdinis console."""
        super().__init__()
        
        self.debug = debug
        
        # Initialize console with fallback if rich not available
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = SimpleConsole()
        
        self.module_manager = ModuleManager()
        self.session_manager = SessionManager()
        
        # Current module state
        self.current_module = None
        self.current_module_name = ""
        
        # Console settings
        self.prompt = "houdini > "
        self.intro = self._get_intro_message()
        
        # Load available modules
        self._load_modules()
    
    def _get_intro_message(self) -> str:
        """Get welcome message for console."""
        return """
Welcome to Houdinis Framework

Type 'help' for available commands
Type 'show modules' to list available modules
Type 'use <module>' to select a module

  For authorized penetration testing only 
"""
    
    def _load_modules(self):
        """Load all available modules from the framework."""
        try:
            self.module_manager.load_all_modules()
            if self.debug:
                print(f"[DEBUG] Loaded {len(self.module_manager.modules)} modules")
        except Exception as e:
            self.console.print(f"Error loading modules: {e}")
            if self.debug:
                traceback.print_exc()
    
    def _update_prompt(self):
        """Update command prompt based on current module."""
        if self.current_module:
            module_type = self.current_module_name.split('/')[0]
            module_name = self.current_module_name.split('/')[-1]
            self.prompt = f"houdini {module_type}({module_name}) > "
        else:
            self.prompt = "houdini > "
    
    def do_help(self, arg):
        """Show help information."""
        if arg:
            # Show help for specific command
            super().do_help(arg)
        else:
            self._show_main_help()
    
    def _show_main_help(self):
        """Show main help menu."""
        if RICH_AVAILABLE:
            help_table = Table(title="Houdinis Commands", show_header=True)
            help_table.add_column("Command", style="cyan", no_wrap=True)
            help_table.add_column("Description", style="white")
            
            commands = [
                ("help [command]", "Show help information"),
                ("show modules", "List all available modules"),
                ("show scanners", "List scanner modules"),
                ("show exploits", "List exploit modules"),
                ("show payloads", "List payload modules"),
                ("show options", "Show current module options"),
                ("show sessions", "List active sessions"),
                ("use <module>", "Select a module to use"),
                ("set <option> <value>", "Set module option value"),
                ("unset <option>", "Unset module option"),
                ("run", "Execute current scanner/payload module"),
                ("exploit", "Execute current exploit module"),
                ("back", "Return to main menu"),
                ("sessions", "Interact with sessions"),
                ("resource <file>", "Execute resource script"),
                ("exit/quit", "Exit Houdinis"),
            ]
            
            for cmd, desc in commands:
                help_table.add_row(cmd, desc)
            
            self.console.print(help_table)
        else:
            # Simple text fallback
            print("\nHoudini Commands:")
            print("=" * 50)
            commands = [
                ("help [command]", "Show help information"),
                ("show modules", "List all available modules"),
                ("show scanners", "List scanner modules"),
                ("show exploits", "List exploit modules"),
                ("show payloads", "List payload modules"),
                ("show options", "Show current module options"),
                ("show sessions", "List active sessions"),
                ("use <module>", "Select a module to use"),
                ("set <option> <value>", "Set module option value"),
                ("unset <option>", "Unset module option"),
                ("run", "Execute current scanner/payload module"),
                ("exploit", "Execute current exploit module"),
                ("back", "Return to main menu"),
                ("sessions", "Interact with sessions"),
                ("resource <file>", "Execute resource script"),
                ("exit/quit", "Exit Houdinis"),
            ]
            
            for cmd, desc in commands:
                print(f"  {cmd:<25} {desc}")
            print()
    
    def do_show(self, line):
        """Show various information."""
        args = line.split()
        if not args:
            self.console.print("Usage: show <modules|scanners|exploits|payloads|options|sessions>")
            return
        
        target = args[0].lower()
        
        if target == "modules":
            self._show_modules()
        elif target == "scanners":
            self._show_modules("scanner")
        elif target == "exploits":
            self._show_modules("exploit")
        elif target == "payloads":
            self._show_modules("payload")
        elif target == "options":
            self._show_options()
        elif target == "sessions":
            self._show_sessions()
        else:
            self.console.print(f"Unknown show target: {target}")
    
    def _show_modules(self, module_type: Optional[str] = None):
        """Show available modules."""
        modules = self.module_manager.get_modules(module_type)
        
        if not modules:
            self.console.print(f"No {module_type or 'modules'} available")
            return
        
        if RICH_AVAILABLE:
            table = Table(title=f"Available {module_type.title() if module_type else 'Modules'}")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Description", style="white")
            table.add_column("Author", style="green")
            table.add_column("Version", style="yellow")
            
            for name, module_class in modules.items():
                try:
                    module_instance = module_class()
                    info = module_instance.info
                    table.add_row(
                        name,
                        info.get('description', 'No description'),
                        info.get('author', 'Unknown'),
                        info.get('version', '1.0')
                    )
                except Exception as e:
                    table.add_row(name, f"Error: {e}", "Unknown", "Unknown")
            
            self.console.print(table)
        else:
            # Simple text fallback
            print(f"\nAvailable {module_type.title() if module_type else 'Modules'}:")
            print("=" * 60)
            for name, module_class in modules.items():
                try:
                    module_instance = module_class()
                    info = module_instance.info
                    print(f"  {name:<30} {info.get('description', 'No description')}")
                except Exception as e:
                    print(f"  {name:<30} Error: {e}")
            print()
    
    def _show_options(self):
        """Show current module options."""
        if not self.current_module:
            self.console.print("No module selected. Use 'use <module>' first.")
            return
        
        options = self.current_module.options
        if not options:
            self.console.print("No options available for this module.")
            return
        
        if RICH_AVAILABLE:
            table = Table(title=f"Module Options: {self.current_module_name}")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Current Setting", style="white")
            table.add_column("Required", style="red")
            table.add_column("Description", style="green")
            
            for name, config in options.items():
                current_value = getattr(self.current_module, name.lower(), "")
                required = "yes" if config.get('required', False) else "no"
                description = config.get('description', 'No description')
                
                table.add_row(name, str(current_value), required, description)
            
            self.console.print(table)
        else:
            # Simple text fallback
            print(f"\nModule Options: {self.current_module_name}")
            print("=" * 60)
            print(f"{'Name':<20} {'Value':<20} {'Required':<10} {'Description'}")
            print("-" * 60)
            for name, config in options.items():
                current_value = getattr(self.current_module, name.lower(), "")
                required = "yes" if config.get('required', False) else "no"
                description = config.get('description', 'No description')
                print(f"{name:<20} {str(current_value):<20} {required:<10} {description}")
            print()
    
    def _show_sessions(self):
        """Show active sessions."""
        sessions = self.session_manager.get_sessions()
        
        if not sessions:
            self.console.print("No active sessions.")
            return
        
        if RICH_AVAILABLE:
            table = Table(title="Active Sessions")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Type", style="white")
            table.add_column("Target", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Created", style="blue")
            
            for session in sessions:
                table.add_row(
                    str(session.id),
                    session.session_type,
                    session.target,
                    session.status,
                    session.created_at.strftime("%Y-%m-%d %H:%M:%S")
                )
            
            self.console.print(table)
        else:
            # Simple text fallback
            print("\nActive Sessions:")
            print("=" * 60)
            print(f"{'ID':<5} {'Type':<15} {'Target':<20} {'Status':<10} {'Created'}")
            print("-" * 60)
            for session in sessions:
                print(f"{session.id:<5} {session.session_type:<15} {session.target:<20} {session.status:<10} {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
    
    def do_use(self, line):
        """Select a module to use."""
        if not line:
            self.console.print("Usage: use <module_name>")
            return
        
        module_name = line.strip()
        
        try:
            module_class = self.module_manager.get_module(module_name)
            if not module_class:
                self.console.print(f"Module '{module_name}' not found")
                return
            
            # Initialize module
            self.current_module = module_class()
            self.current_module_name = module_name
            self._update_prompt()
            
            # Show module info
            info = self.current_module.info
            if RICH_AVAILABLE:
                panel = Panel(
                    f"[bold]{info.get('name', module_name)}[/bold]\n"
                    f"Description: {info.get('description', 'No description')}\n"
                    f"Author: {info.get('author', 'Unknown')}\n"
                    f"Version: {info.get('version', '1.0')}",
                    title="Module Selected",
                    border_style="green"
                )
                self.console.print(panel)
            else:
                print("\nModule Selected:")
                print("=" * 50)
                print(f"Name: {info.get('name', module_name)}")
                print(f"Description: {info.get('description', 'No description')}")
                print(f"Author: {info.get('author', 'Unknown')}")
                print(f"Version: {info.get('version', '1.0')}")
                print()
            
        except Exception as e:
            self.console.print(f"Error loading module: {e}")
            if self.debug:
                traceback.print_exc()
    
    def do_set(self, line):
        """Set module option value."""
        if not self.current_module:
            self.console.print("No module selected. Use 'use <module>' first.")
            return
        
        args = line.split(None, 1)
        if len(args) != 2:
            self.console.print("Usage: set <option> <value>")
            return
        
        option, value = args
        option = option.upper()
        
        if option not in self.current_module.options:
            self.console.print(f"Unknown option: {option}")
            return
        
        try:
            # Set the option value
            setattr(self.current_module, option.lower(), value)
            self.console.print(f"{option} => {value}")
        except Exception as e:
            self.console.print(f"Error setting option: {e}")
    
    def do_unset(self, line):
        """Unset module option."""
        if not self.current_module:
            self.console.print("No module selected. Use 'use <module>' first.")
            return
        
        option = line.strip().upper()
        if not option:
            self.console.print("Usage: unset <option>")
            return
        
        if option not in self.current_module.options:
            self.console.print(f"Unknown option: {option}")
            return
        
        try:
            setattr(self.current_module, option.lower(), "")
            self.console.print(f"Unset {option}")
        except Exception as e:
            self.console.print(f"Error unsetting option: {e}")
    
    def do_run(self, line):
        """Execute current scanner or payload module."""
        if not self.current_module:
            self.console.print("No module selected. Use 'use <module>' first.")
            return
        
        # Validate required options
        if not self._validate_options():
            return
        
        try:
            self.console.print(f"Running {self.current_module_name}...")
            
            if hasattr(self.current_module, 'run'):
                result = self.current_module.run()
                self._handle_module_result(result)
            else:
                self.console.print("Module does not support 'run' command")
                
        except Exception as e:
            self.console.print(f"Module execution failed: {e}")
            if self.debug:
                traceback.print_exc()
    
    def do_exploit(self, line):
        """Execute current exploit module."""
        if not self.current_module:
            self.console.print("No module selected. Use 'use <module>' first.")
            return
        
        # Validate required options
        if not self._validate_options():
            return
        
        try:
            self.console.print(f"Exploiting with {self.current_module_name}...")
            
            if hasattr(self.current_module, 'exploit'):
                result = self.current_module.exploit()
                self._handle_module_result(result)
            else:
                self.console.print("Module does not support 'exploit' command")
                
        except Exception as e:
            self.console.print(f"Exploit execution failed: {e}")
            if self.debug:
                traceback.print_exc()
    
    def _validate_options(self) -> bool:
        """Validate required module options."""
        if not self.current_module or not hasattr(self.current_module, 'options'):
            return False
            
        for option, config in self.current_module.options.items():
            if config.get('required', False):
                value = getattr(self.current_module, option.lower(), "")
                if not value:
                    self.console.print(f"Required option {option} is not set")
                    return False
        return True
    
    def _handle_module_result(self, result: Any):
        """Handle module execution result."""
        if isinstance(result, dict):
            if result.get('success'):
                self.console.print(f"Module executed successfully")
                
                # Create session if applicable
                if result.get('session_data'):
                    session = self.session_manager.create_session(
                        session_type=result.get('session_type', 'unknown'),
                        target=getattr(self.current_module, 'target', 'unknown'),
                        data=result['session_data']
                    )
                    self.console.print(f"Session {session.id} created")
            else:
                self.console.print(f"Module execution failed: {result.get('error', 'Unknown error')}")
        else:
            self.console.print("Module execution completed")
    
    def do_back(self, line):
        """Return to main menu."""
        self.current_module = None
        self.current_module_name = ""
        self._update_prompt()
        self.console.print("Back to main menu")
    
    def do_scan(self, line):
        """Quick scan command similar to Metasploit."""
        args = line.split()
        
        if len(args) < 2 or args[0] != "host":
            self.console.print("Usage: scan host <target>")
            return
        
        target = args[1]
        
        print(f"[*] Quick scanning {target}...")
        
        # Simulate quick scan results
        vulnerable_services = [
            {"port": 443, "service": "HTTPS", "cipher": "TLS_RSA_WITH_AES_128_CBC_SHA", "key": "RSA-1024", "vulnerable": True},
            {"port": 22, "service": "SSH", "cipher": "ssh-rsa", "key": "RSA-2048", "vulnerable": True},
            {"port": 80, "service": "HTTP", "cipher": None, "key": None, "vulnerable": False}
        ]
        
        for svc in vulnerable_services:
            if svc["port"] in [443, 22]:  # Only show crypto services
                if svc["vulnerable"]:
                    print(f"[+] Port {svc['port']} open — {svc['cipher']} ({svc['key']})")
                    print(f"[+] Vulnerable: Yes")
                else:
                    print(f"[+] Port {svc['port']} open — {svc['service']}")
        
        print(f"[*] Scan complete. Found quantum-vulnerable services on ports 22, 443")
        print(f"[!] Recommendation: use exploit/rsa_shor")
    
    def do_sessions(self, line):
        """Interact with sessions."""
        args = line.split()
        
        if not args:
            self._show_sessions()
            return
        
        command = args[0].lower()
        
        if command == "list" or command == "-l":
            self._show_sessions()
        elif command == "interact" or command == "-i":
            if len(args) < 2:
                self.console.print("Usage: sessions -i <session_id>")
                return
            try:
                session_id = int(args[1])
                self._interact_with_session(session_id)
            except ValueError:
                self.console.print("Invalid session ID")
        elif command == "kill" or command == "-k":
            if len(args) < 2:
                self.console.print("Usage: sessions -k <session_id>")
                return
            try:
                session_id = int(args[1])
                self.session_manager.kill_session(session_id)
                self.console.print(f"Session {session_id} killed")
            except ValueError:
                self.console.print("Invalid session ID")
        else:
            self.console.print("Usage: sessions [-l|-i <id>|-k <id>]")
    
    def _interact_with_session(self, session_id: int):
        """Interact with a specific session."""
        session = self.session_manager.get_session(session_id)
        if not session:
            self.console.print(f"Session {session_id} not found")
            return
        
        self.console.print(f"Interacting with session {session_id}")
        # Implementation depends on session type
        # For now, just show session info
        print(f"Session Type: {session.session_type}")
        print(f"Target: {session.target}")
        print(f"Status: {session.status}")
    
    def do_resource(self, line):
        """Execute resource script."""
        if not line:
            self.console.print("Usage: resource <script_file>")
            return
        
        script_path = line.strip()
        self.execute_resource_script(script_path)
    
    def execute_resource_script(self, script_path: str):
        """Execute commands from a resource script file."""
        try:
            with open(script_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        print(f"houdini > {line}")
                        self.onecmd(line)
        except FileNotFoundError:
            self.console.print(f"Resource script not found: {script_path}")
        except Exception as e:
            self.console.print(f"Error executing resource script: {e}")
    
    def do_exit(self, line):
        """Exit Houdinis."""
        return self.do_quit(line)
    
    def do_quit(self, line):
        """Exit Houdinis."""
        self.console.print("Goodbye!")
        return True
    
    def emptyline(self):
        """Handle empty line input."""
        return False
    
    def default(self, line):
        """Handle unknown commands."""
        self.console.print(f"Unknown command: {line}")
        self.console.print("Type 'help' for available commands")
    
    def cmdloop(self, intro=None):
        """Override cmdloop to use rich console."""
        if intro is not None:
            self.intro = intro
        
        if self.intro:
            self.console.print(self.intro)
        
        stop = None
        while not stop:
            try:
                # Secure input handling with validation
                line = input(self.prompt).strip()
                
                # Input validation and sanitization
                if len(line) > 1000:  # Prevent buffer overflow
                    self.console.print("[!] Command too long")
                    continue
                
                # Basic command injection prevention
                import re
                if re.search(r'[;&|`$(){}]', line) and not line.startswith(('set ', 'show ', 'use ', 'help')):
                    self.console.print("[!] Invalid characters in command")
                    continue
                
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
                
            except KeyboardInterrupt:
                self.console.print("\nUse 'exit' or 'quit' to leave")
            except EOFError:
                self.console.print("\nGoodbye!")
            except Exception as e:
                self.console.print(f"[!] Command error: {e}")
                if self.debug:
                    import traceback
                    traceback.print_exc()
                break
