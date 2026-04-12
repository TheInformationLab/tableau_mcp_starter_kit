#!/usr/bin/env python3
"""
Test script to verify OpenAI model connection
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test if we can connect to OpenAI and get a response"""
    try:
        # Check if API key is set
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment variables")
            return False

        print("✅ OPENAI_API_KEY found")

        # Initialize the model
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        print("✅ ChatOpenAI model initialized successfully")

        # Test with a more complex message to ensure API call
        messages = [HumanMessage(content="Please write a short paragraph about artificial intelligence and its impact on modern technology. Make it at least 100 words long.")]
        response = llm.invoke(messages)

        if response and hasattr(response, 'content') and len(response.content) > 50:
            print(f"✅ OpenAI response received ({len(response.content)} characters)")
            print(f"Response preview: {response.content[:100]}...")
            return True
        else:
            print("❌ No valid response from OpenAI or response too short")
            return False

    except Exception as e:
        print(f"❌ Error testing OpenAI connection: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing OpenAI model connection...")
    success = test_openai_connection()
    if success:
        print("\n🎉 OpenAI connection test passed!")
    else:
        print("\n💥 OpenAI connection test failed!")