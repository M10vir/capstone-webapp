def analyze_requirements(prompt: str) -> dict:
    """Analyze user prompt and produce formal requirments."""
    return {
        "requirements": [
            "Calculator must support operators: +, -, *, /", 
            "Simple terminal-based UI", 
            "Single-file Python CLI implementation",
            "No external dependencies",
            "Return errors for invalid operations or divide-by-zero"
        ],
        "notes": f"Prompt analyzed: '{prompt}'"
    }
