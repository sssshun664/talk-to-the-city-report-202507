#!/usr/bin/env python3
"""
Migration script for Talk to the City Scatter to latest LangChain and OpenAI versions.

This script helps migrate from the legacy versions to the current compatible versions.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True

def install_dependencies():
    """Install updated dependencies."""
    commands = [
        ("pip install -U pip", "Updating pip"),
        ("pip install -r requirements.txt", "Installing new dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def verify_installation():
    """Verify that the new libraries are working."""
    try:
        print("\n🔍 Verifying installation...")
        
        # Test OpenAI
        import openai
        print(f"✅ OpenAI version: {openai.__version__}")
        
        # Test LangChain
        import langchain
        print(f"✅ LangChain version: {langchain.__version__}")
        
        # Test LangChain OpenAI
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        print("✅ LangChain OpenAI integration working")
        
        # Test LangChain Core
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
        print("✅ LangChain Core messages working")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_pipeline():
    """Test if the pipeline can initialize."""
    try:
        print("\n🧪 Testing pipeline initialization...")
        
        # Check if OpenAI API key is set
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  OPENAI_API_KEY environment variable not set")
            print("   Please set it before running the pipeline:")
            print("   export OPENAI_API_KEY=your_api_key_here")
            return False
            
        # Try to import and create basic instances
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from utils import messages
        
        # Test basic functionality without making API calls
        llm = ChatOpenAI(model="gpt-4.1-2025-04-14", temperature=0.0)
        print("✅ ChatOpenAI initialized successfully")
        
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        print("✅ OpenAIEmbeddings initialized successfully")
        
        # Test message formatting
        test_messages = messages("/system\nYou are helpful\n/human\nTest", "test input")
        print("✅ Message formatting working")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False

def main():
    """Main migration function."""
    print("🚀 Talk to the City - Migration to Latest LangChain/OpenAI")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Installation verification failed")
        sys.exit(1)
    
    # Test pipeline
    if not test_pipeline():
        print("\n❌ Pipeline test failed")
        print("\n📋 Next steps:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Test the pipeline with: python main.py configs/example-polis.json")
        sys.exit(1)
    
    print("\n🎉 Migration completed successfully!")
    print("\n📋 Next steps:")
    print("1. Set your OPENAI_API_KEY environment variable if not already set")
    print("2. Test the pipeline with: python main.py configs/example-polis.json")
    print("3. Check the generated reports in the outputs/ directory")

if __name__ == "__main__":
    main() 