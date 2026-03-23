#!/usr/bin/env python3
"""
Health Check Module for Python Projects
========================================
Centralized health verification functions for OpenClaw-managed projects.

Usage:
    from health_check import health_check
    result = health_check()
    print(result)
"""

import sys
import os
import importlib.util
from typing import Dict, Any, List, Tuple


def check_python_version() -> Tuple[bool, str]:
    """Verify Python version is 3.9+."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor} (requires 3.9+)"


def check_dependencies() -> Tuple[bool, str]:
    """Verify required dependencies can be imported."""
    required_files = ["requirements.txt", "pyproject.toml"]
    deps_found = False
    deps_file = None
    
    for fname in required_files:
        if os.path.exists(fname):
            deps_found = True
            deps_file = fname
            break
    
    if not deps_found:
        return False, "No dependency file found"
    
    # Try importing key dependencies based on project type
    common_deps = ["pytest", "requests", "pydantic", "fastapi"]
    missing = []
    
    for dep in common_deps:
        try:
            importlib.import_module(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        return False, f"Missing optional deps: {', '.join(missing)}"
    
    return True, f"Dependencies OK ({deps_file})"


def check_project_structure() -> Tuple[bool, str]:
    """Verify basic project structure."""
    required = ["README.md", ".gitignore"]
    missing = [f for f in required if not os.path.exists(f)]
    
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    
    return True, "Structure OK"


def check_docker() -> Tuple[bool, str]:
    """Check Docker configuration if present."""
    docker_files = ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"]
    found = [f for f in docker_files if os.path.exists(f)]
    
    if not found:
        return False, "No Docker config"
    
    return True, f"Docker: {', '.join(found)}"


def check_security() -> Tuple[bool, str]:
    """Check for security configuration."""
    security_files = [".grype.yaml", "SECURITY.md", ".pre-commit-config.yaml"]
    found = [f for f in security_files if os.path.exists(f)]
    
    if not found:
        return False, "No security config"
    
    return True, f"Security: {', '.join(found)}"


def check_ci_cd() -> Tuple[bool, str]:
    """Check CI/CD configuration."""
    has_github = os.path.isdir(".github/workflows")
    has_jenkins = os.path.exists("Jenkinsfile")
    
    if not has_github and not has_jenkins:
        return False, "No CI/CD config"
    
    configs = []
    if has_github:
        configs.append("GitHub Actions")
    if has_jenkins:
        configs.append("Jenkins")
    
    return True, f"CI/CD: {', '.join(configs)}"


def health_check() -> Dict[str, Any]:
    """
    Run all health checks and return results.
    
    Returns:
        Dict with 'status' (pass/fail), 'checks' (list of check results),
        and 'summary' (overall message)
    """
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Docker", check_docker),
        ("Security", check_security),
        ("CI/CD", check_ci_cd),
    ]
    
    results = []
    passed = 0
    
    for name, check_fn in checks:
        try:
            ok, msg = check_fn()
            results.append({
                "name": name,
                "status": "PASS" if ok else "FAIL",
                "message": msg
            })
            if ok:
                passed += 1
        except Exception as e:
            results.append({
                "name": name,
                "status": "ERROR",
                "message": str(e)
            })
    
    status = "pass" if passed == len(checks) else "degraded" if passed > 0 else "fail"
    
    return {
        "status": status,
        "passed": passed,
        "total": len(checks),
        "checks": results,
        "summary": f"{passed}/{len(checks)} checks passed"
    }


def main():
    """CLI entry point."""
    result = health_check()
    
    print(f"\n🏥 Health Check Results")
    print(f"=" * 40)
    print(f"Status: {result['status'].upper()}")
    print(f"Summary: {result['summary']}\n")
    
    for check in result['checks']:
        icon = "✅" if check['status'] == "PASS" else "❌" if check['status'] == "FAIL" else "⚠️"
        print(f"  {icon} {check['name']}: {check['message']}")
    
    print()
    
    # Exit with appropriate code
    if result['status'] == 'fail':
        sys.exit(1)
    elif result['status'] == 'degraded':
        sys.exit(0)  # Degraded is still usable
    sys.exit(0)


if __name__ == "__main__":
    main()
