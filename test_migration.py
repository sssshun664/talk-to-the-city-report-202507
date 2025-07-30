#!/usr/bin/env python3
"""
Quick test script to verify the migration was successful.
Tests the core functionality without running the full pipeline.
"""

import os
import sys

def test_imports():
    """Test all the critical imports."""
    print("🧪 Testing imports...")
    
    try:
        # Core libraries
        import openai
        import langchain
        print(f"✅ OpenAI: {openai.__version__}")
        print(f"✅ LangChain: {langchain.__version__}")
        
        # LangChain OpenAI integration
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        print("✅ LangChain OpenAI integration")
        
        # LangChain Core
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
        print("✅ LangChain Core messages")
        
        # Utils
        from utils import messages, typed_message
        print("✅ Local utils module")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_message_formatting():
    """Test the message formatting function."""
    print("\n🧪 Testing message formatting...")
    
    try:
        from utils import messages
        
        test_prompt = """/system
You are a helpful assistant.

/human
This is a test message.

/ai
I understand."""
        
        formatted = messages(test_prompt, "User input")
        
        if len(formatted) == 4:  # system, human, ai, human
            print("✅ Message formatting working correctly")
            return True
        else:
            print(f"❌ Unexpected message count: {len(formatted)}")
            return False
            
    except Exception as e:
        print(f"❌ Message formatting failed: {e}")
        return False

def test_llm_initialization():
    """Test LLM initialization without API calls."""
    print("\n🧪 Testing LLM initialization...")
    
    try:
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        
        # Test ChatOpenAI
        llm = ChatOpenAI(model="gpt-4.1-2025-04-14", temperature=0.0)
        print("✅ ChatOpenAI initialization")
        
        # Test OpenAIEmbeddings with latest model
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        print("✅ OpenAIEmbeddings initialization")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM initialization failed: {e}")
        return False

def test_config_loading():
    """Test configuration file loading."""
    print("\n🧪 Testing config loading...")
    
    try:
        import json
        
        # Test example config
        with open("configs/example-polis.json", "r") as f:
            config = json.load(f)
        
        required_fields = ["name", "question", "input", "model"]
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field: {field}")
                return False
        
        print("✅ Config file loading and validation")
        return True
        
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        return False

def test_api_key():
    """Check if OpenAI API key is set."""
    print("\n🧪 Checking API key...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set")
        print("   Set it with: export OPENAI_API_KEY=your_key_here")
        return False
    elif api_key.startswith('sk-') and len(api_key) > 20:
        print("✅ OpenAI API key appears to be set correctly")
        return True
    else:
        print("⚠️  OpenAI API key format looks suspicious")
        return False

def main():
    """Run all tests."""
    print("🚀 Talk to the City - Migration Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Message Formatting", test_message_formatting),
        ("LLM Initialization", test_llm_initialization),
        ("Config Loading", test_config_loading),
        ("API Key Check", test_api_key),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Migration successful!")
        print("\n📋 Next steps:")
        print("1. Run the full pipeline: python main.py configs/example-polis.json")
        print("2. Check the generated reports")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        print("\n🔧 Common fixes:")
        print("1. Reinstall dependencies: pip install -r requirements.txt")
        print("2. Set API key: export OPENAI_API_KEY=your_key_here")
        print("3. Check Python version: python --version (need 3.10+)")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 