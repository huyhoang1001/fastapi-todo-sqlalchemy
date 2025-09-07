#!/usr/bin/env python3
"""
Test runner script for the FastAPI Todo application.
"""
import subprocess
import sys
import os

def run_tests():
    """Run all tests with coverage reporting."""
    
    # Install test dependencies
    print("Installing test dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"], check=True)
    
    # Run unit tests
    print("\n" + "="*50)
    print("Running Unit Tests")
    print("="*50)
    result_unit = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/unit/", 
        "-v", 
        "--tb=short"
    ])
    
    # Run integration tests
    print("\n" + "="*50)
    print("Running Integration Tests")
    print("="*50)
    result_integration = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/integration/", 
        "-v", 
        "--tb=short"
    ])
    
    # Run all tests
    print("\n" + "="*50)
    print("Running All Tests")
    print("="*50)
    result_all = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short"
    ])
    
    # Summary
    print("\n" + "="*50)
    print("Test Results Summary")
    print("="*50)
    print(f"Unit Tests: {'PASSED' if result_unit.returncode == 0 else 'FAILED'}")
    print(f"Integration Tests: {'PASSED' if result_integration.returncode == 0 else 'FAILED'}")
    print(f"Overall: {'PASSED' if result_all.returncode == 0 else 'FAILED'}")
    
    return result_all.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)