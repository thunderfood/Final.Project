# src/tools/storage.py

import json
import os
from datetime import datetime

class Storage:
    """Simple JSON storage for analysis history"""
    
    def __init__(self, filename="data/history.json"):
        self.filename = filename
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
    
    def save_analysis(self, analysis_type, report, analysis):
        """Save an analysis to history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': analysis_type,
            'report': report,
            'analysis': analysis
        }
        
        # Load existing history
        history = self.load_history()
        
        # Add new entry
        history.append(entry)
        
        # Save back
        with open(self.filename, 'w') as f:
            json.dump(history, f, indent=2)
        
        return True
    
    def load_history(self):
        """Load history from file"""
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def get_recent(self, n=10):
        """Get N most recent entries"""
        history = self.load_history()
        return history[-n:] if history else []
    
    def clear_history(self):
        """Clear all history"""
        with open(self.filename, 'w') as f:
            json.dump([], f)
        return True

# Test
if __name__ == "__main__":
    print("\n" + "="*50)
    print("Storage System Test")
    print("="*50 + "\n")
    
    storage = Storage()
    
    # Save a test entry
    storage.save_analysis(
        "system",
        "CPU: 25%, RAM: 50%, Disk: 80%",
        "Status: Good. No issues detected."
    )
    
    # Load history
    history = storage.load_history()
    print(f"✅ Saved {len(history)} entries")
    
    # Show recent
    recent = storage.get_recent(5)
    print(f"✅ Loaded {len(recent)} recent entries")
    
    print("\n✅ Storage system working!\n")
