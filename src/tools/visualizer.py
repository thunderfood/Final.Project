# src/tools/visualizer.py

import plotly.graph_objects as go

def create_gauge_chart(value, title, max_value=100):
    """Create a gauge chart for a metric"""
    
    # Determine color based on value
    if value < 50:
        color = "green"
    elif value < 80:
        color = "yellow"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        gauge = {
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# Test
if __name__ == "__main__":
    print("\n✅ Visualizer created!")
    print("Use in Streamlit with: st.plotly_chart(fig)\n")
```

Now you can add charts to your dashboard! (I'll show you how if you want)

---

## ✅ What You've Built So Far

### **Core Features:**
- ✅ System health monitoring (CPU, RAM, Disk)
- ✅ AI-powered analysis and recommendations
- ✅ History tracking (saves all checks)
- ✅ Modern tabbed interface
- ✅ Configuration system (.env)
- ✅ Local storage (JSON)

### **File Structure:**
```
ai-pc-assistant/
├── .env                    (your settings)
├── venv/                   (Python environment)
├── src/
│   ├── config.py          (configuration loader)
│   ├── tools/
│   │   ├── system_monitor.py    (PC health checker)
│   │   ├── storage.py           (save history)
│   │   ├── email_checker.py     (email placeholder)
│   │   └── visualizer.py        (charts - optional)
│   └── llm/               (empty for now)
├── data/
│   └── history.json       (saved analyses)
├── test.py                (connection test)
├── main.py                (CLI version)
├── dashboard.py           (simple dashboard)
└── dashboard_v2.py        (enhanced dashboard) ⭐
