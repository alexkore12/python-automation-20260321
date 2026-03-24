#!/usr/bin/env python3
"""
Python Automation CLI - Command Line Interface for the FastAPI Backend

Usage:
    python cli.py <command> [options]

Commands:
    health          Check API health status
    items list      List all items
    items create    Create a new item
    items get       Get item by ID
    items update    Update an item
    items delete    Delete an item
    users list      List all users (admin)
    users create    Create a new user (admin)
    token           Generate access token
    report          Generate system report

Examples:
    python cli.py health
    python cli.py token --username admin --password secret
    python cli.py items list
    python cli.py items create --name "Widget" --price 29.99
    python cli.py items get --id 1
"""

import argparse
import json
import os
import sys
import base64
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = 30


class Colors:
    """ANSI color codes for terminal output"""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def green(text: str) -> str:
    return f"{Colors.GREEN}{text}{Colors.RESET}"


def red(text: str) -> str:
    return f"{Colors.RED}{text}{Colors.RESET}"


def yellow(text: str) -> str:
    return f"{Colors.YELLOW}{text}{Colors.RESET}"


def blue(text: str) -> str:
    return f"{Colors.BLUE}{text}{Colors.RESET}"


def api_request(
    method: str,
    endpoint: str,
    token: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Make an authenticated API request"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as response:
            result = json.loads(response.read().decode())
            return {"status": response.status, "data": result}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            error_data = json.loads(error_body)
            return {"status": e.code, "error": error_data}
        except json.JSONDecodeError:
            return {"status": e.code, "error": {"detail": error_body}}
    except urllib.error.URLError as e:
        return {"status": 0, "error": {"detail": str(e.reason)}}


def cmd_health(token: Optional[str] = None) -> int:
    """Check API health"""
    print(blue("Checking API health..."))
    result = api_request("GET", "/health", token)

    if result["status"] == 200:
        data = result["data"]
        print(green("✓ API is healthy"))
        print(f"  Status: {data.get('status')}")
        print(f"  Timestamp: {data.get('timestamp')}")
        return 0
    else:
        print(red(f"✗ API is unhealthy (status {result['status']})"))
        if "error" in result:
            print(f"  Error: {result['error'].get('detail', 'Unknown')}")
        return 1


def cmd_token(args: argparse.Namespace) -> int:
    """Generate access token"""
    print(blue("Generating access token..."))

    if not args.username or not args.password:
        print(red("Error: --username and --password are required"))
        return 1

    result = api_request(
        "POST",
        "/auth/login",
        data={"username": args.username, "password": args.password},
    )

    if result["status"] == 200:
        data = result["data"]
        print(green("✓ Authentication successful"))
        print(f"  Access Token: {data.get('access_token', '')[:50]}...")
        print(f"  Token Type: {data.get('token_type')}")
        print(f"  Expires In: {data.get('expires_in')} seconds")
        return 0
    else:
        print(red(f"✗ Authentication failed (status {result['status']})"))
        if "error" in result:
            print(f"  Error: {result['error'].get('detail', 'Unknown')}")
        return 1


def cmd_items_list(token: Optional[str]) -> int:
    """List all items"""
    print(blue("Fetching items..."))
    result = api_request("GET", "/items", token)

    if result["status"] == 200:
        data = result["data"]
        items = data if isinstance(data, list) else data.get("items", [])
        print(green(f"✓ Found {len(items)} items"))
        for item in items:
            print(f"  [{item.get('id')}] {item.get('name', 'N/A')} - ${item.get('price', 'N/A')}")
        return 0
    else:
        print(red(f"✗ Failed to fetch items (status {result['status']})"))
        return 1


def cmd_items_get(args: argparse.Namespace, token: Optional[str]) -> int:
    """Get item by ID"""
    print(blue(f"Fetching item {args.id}..."))
    result = api_request("GET", f"/items/{args.id}", token)

    if result["status"] == 200:
        item = result["data"]
        print(green(f"✓ Item found"))
        for key, value in item.items():
            print(f"  {key}: {value}")
        return 0
    else:
        print(red(f"✗ Item not found (status {result['status']})"))
        return 1


def cmd_items_create(args: argparse.Namespace, token: Optional[str]) -> int:
    """Create a new item"""
    data = {}
    if args.name:
        data["name"] = args.name
    if args.description:
        data["description"] = args.description
    if args.price is not None:
        data["price"] = args.price

    if not data:
        print(red("Error: At least --name is required"))
        return 1

    print(blue(f"Creating item..."))
    result = api_request("POST", "/items", token, data)

    if result["status"] == 201:
        item = result["data"]
        print(green(f"✓ Item created with ID {item.get('id')}"))
        return 0
    else:
        print(red(f"✗ Failed to create item (status {result['status']})"))
        if "error" in result:
            print(f"  Error: {result['error'].get('detail', 'Unknown')}")
        return 1


def cmd_items_delete(args: argparse.Namespace, token: Optional[str]) -> int:
    """Delete an item"""
    print(blue(f"Deleting item {args.id}..."))
    result = api_request("DELETE", f"/items/{args.id}", token)

    if result["status"] in (200, 204):
        print(green(f"✓ Item {args.id} deleted"))
        return 0
    else:
        print(red(f"✗ Failed to delete item (status {result['status']})"))
        return 1


def cmd_users_list(token: Optional[str]) -> int:
    """List all users"""
    print(blue("Fetching users..."))
    result = api_request("GET", "/users", token)

    if result["status"] == 200:
        users = result["data"]
        print(green(f"✓ Found {len(users)} users"))
        for user in users:
            print(f"  [{user.get('id')}] {user.get('username')} ({user.get('email')}) - {user.get('role')}")
        return 0
    else:
        print(red(f"✗ Failed to fetch users (status {result['status']})"))
        return 1


def cmd_report(token: Optional[str]) -> int:
    """Generate system report"""
    print(blue("Generating system report...\n"))

    # Health
    print(yellow("=== Health Status ==="))
    health = api_request("GET", "/health", token)
    if health["status"] == 200:
        print(green(f"  API: Healthy"))
    else:
        print(red(f"  API: Unhealthy"))

    # Items count
    print(yellow("\n=== Items ==="))
    items = api_request("GET", "/items", token)
    if items["status"] == 200:
        item_list = items["data"] if isinstance(items["data"], list) else items["data"].get("items", [])
        print(f"  Total items: {len(item_list)}")
    else:
        print("  Could not fetch items")

    # Users count
    print(yellow("\n=== Users ==="))
    users = api_request("GET", "/users", token)
    if users["status"] == 200:
        print(f"  Total users: {len(users['data'])}")
    else:
        print("  Could not fetch users (admin only)")

    print()
    return 0


def get_token_from_env() -> Optional[str]:
    """Get token from environment variable"""
    return os.getenv("API_TOKEN") or os.getenv("AUTH_TOKEN")


def main():
    parser = argparse.ArgumentParser(
        description="Python Automation CLI - Command line interface for the API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--url",
        default=API_BASE_URL,
        help=f"API base URL (default: {API_BASE_URL})",
    )
    parser.add_argument(
        "--token",
        default=get_token_from_env(),
        help="API access token (or set API_TOKEN env var)",
    )
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # health
    subparsers.add_parser("health", help="Check API health status")

    # token
    token_parser = subparsers.add_parser("token", help="Generate access token")
    token_parser.add_argument("--username", required=True, help="Username")
    token_parser.add_argument("--password", required=True, help="Password")
    token_parser.set_defaults(func=lambda a, t: cmd_token(a))

    # items
    items_parser = subparsers.add_parser("items", help="Manage items")
    items_sub = items_parser.add_subparsers(dest="items_command")

    items_list = items_sub.add_parser("list", help="List all items")
    items_list.set_defaults(func=lambda a, t: cmd_items_list(t))

    items_get = items_sub.add_parser("get", help="Get item by ID")
    items_get.add_argument("--id", type=int, required=True, help="Item ID")
    items_get.set_defaults(func=lambda a, t: cmd_items_get(a, t))

    items_create = items_sub.add_parser("create", help="Create new item")
    items_create.add_argument("--name", required=True, help="Item name")
    items_create.add_argument("--description", help="Item description")
    items_create.add_argument("--price", type=float, help="Item price")
    items_create.set_defaults(func=lambda a, t: cmd_items_create(a, t))

    items_delete = items_sub.add_parser("delete", help="Delete item")
    items_delete.add_argument("--id", type=int, required=True, help="Item ID")
    items_delete.set_defaults(func=lambda a, t: cmd_items_delete(a, t))

    # users
    users_parser = subparsers.add_parser("users", help="Manage users")
    users_sub = users_parser.add_subparsers(dest="users_command")

    users_list = users_sub.add_parser("list", help="List all users (admin)")
    users_list.set_defaults(func=lambda a, t: cmd_users_list(t))

    # report
    subparsers.add_parser("report", help="Generate system report").set_defaults(
        func=lambda a, t: cmd_report(t)
    )

    args = parser.parse_args()

    # Update global URL
    global API_BASE_URL
    API_BASE_URL = args.url

    if args.command is None:
        parser.print_help()
        return 1

    return args.func(args, args.token)


if __name__ == "__main__":
    sys.exit(main())
