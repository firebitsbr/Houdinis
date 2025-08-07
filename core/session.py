"""
# Houdinis Framework - Session management for Houdinis.
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT

Handles active sessions from successful exploits and connections.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class Session:
    """Represents an active session."""
    id: int
    session_type: str
    target: str
    status: str
    created_at: datetime
    data: Dict[str, Any]
    
    def __post_init__(self):
        """Initialize session after creation."""
        if self.status == "":
            self.status = "active"


class SessionManager:
    """
    Manages active sessions from successful exploits.
    """
    
    def __init__(self):
        """Initialize session manager."""
        self.sessions: Dict[int, Session] = {}
        self.next_id = 1
    
    def create_session(
        self, 
        session_type: str, 
        target: str, 
        data: Dict[str, Any]
    ) -> Session:
        """
        Create a new session.
        
        Args:
            session_type: Type of session (e.g., 'quantum_exploit', 'shell', 'crypto_break')
            target: Target host/service
            data: Session-specific data
            
        Returns:
            Created session object
        """
        session = Session(
            id=self.next_id,
            session_type=session_type,
            target=target,
            status="active",
            created_at=datetime.now(),
            data=data
        )
        
        self.sessions[self.next_id] = session
        self.next_id += 1
        
        return session
    
    def get_session(self, session_id: int) -> Optional[Session]:
        """
        Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session object or None if not found
        """
        return self.sessions.get(session_id)
    
    def get_sessions(self) -> List[Session]:
        """
        Get all active sessions.
        
        Returns:
            List of all sessions
        """
        return list(self.sessions.values())
    
    def kill_session(self, session_id: int) -> bool:
        """
        Kill/remove a session.
        
        Args:
            session_id: Session ID to kill
            
        Returns:
            True if session was killed, False if not found
        """
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.status = "killed"
            del self.sessions[session_id]
            return True
        return False
    
    def update_session_status(self, session_id: int, status: str) -> bool:
        """
        Update session status.
        
        Args:
            session_id: Session ID
            status: New status
            
        Returns:
            True if updated, False if session not found
        """
        if session_id in self.sessions:
            self.sessions[session_id].status = status
            return True
        return False
    
    def get_sessions_by_type(self, session_type: str) -> List[Session]:
        """
        Get sessions by type.
        
        Args:
            session_type: Type of sessions to retrieve
            
        Returns:
            List of matching sessions
        """
        return [
            session for session in self.sessions.values()
            if session.session_type == session_type
        ]
    
    def clear_all_sessions(self):
        """Clear all sessions."""
        self.sessions.clear()
        self.next_id = 1
