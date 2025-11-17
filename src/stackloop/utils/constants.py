IGNORED_DIRS = {
    # Version control
    ".git",
    ".hg",
    ".svn",
    # Python
    "__pycache__",
    "venv",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    # Node / JS / TS
    "node_modules",
    "dist",
    "build",
    # Java / JVM
    "target",
    ".gradle",
    ".idea",
    # Rust / Cargo
    "target",
    # Go
    "bin",
    # Ruby
    "vendor",
    # .NET / C#
    "bin",
    "obj",
    ".vs",
    "packages",
    # Misc / temp
    ".stackloop",
    ".cache",
    ".DS_Store"
}

DEFAULT_COMMANDS = {
    # --- Python ---
    "Python": "python main.py",
    # --- JavaScript / TypeScript ---
    "Node.js": "npm run build",
    # --- Go ---
    "Go": "go run .",
    # --- C# / .NET ---
    "C#": "dotnet run",
    # --- Java ---
    "Java": "java Main",
    # --- Rust ---
    "Rust": "cargo run",
    # --- Ruby ---
    "Ruby": "ruby main.rb",
    # --- Fallback ---
    "Other": "sh run.sh"
}


SUPPORTED_MODELS = {
    "groq": [       
        "openai/gpt-oss-120b",          
        "openai/gpt-oss-20b" 
    ],
    "openai": [
        "gpt-5",                    # OpenAI's flagship and strongest coding model with high reasoning ability
        "gpt-4o",
        "gpt-4o-mini",              # An efficient model balancing speed and power at a low cost
    ],
    "anthropic": [
        "claude-opus-4.1",          # Anthropic's most powerful model, improves on previous versions
        "claude-sonnet-4.5",        # The best model in the world for agents and coding tasks
    ]
}
