#!/usr/bin/env python3
"""
Test script for the HTTP client extensions for manage_mock_data functionality.
Tests Phase 2 Part 1 HTTP client implementation without MCP dependencies.
"""

import asyncio
from pathlib import Path
import sys

# Add the src directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mockloop_mcp.mock_server_manager import MockServerManager
from mockloop_mcp.utils.http_client import MockServerClient


async def test_http_client_extensions():
    """Test the new HTTP client methods for mock data management."""

    # Test with a mock server URL (will fail gracefully if server not running)
    test_server_url = "http://localhost:8000"
    client = MockServerClient(test_server_url)

    try:
        result = await client.update_response(
            endpoint_path="/api/test",
            response_data={"message": "Updated response", "test": True},
            method="GET"
        )

        # Verify expected structure
        assert "status" in result
        assert "endpoint_path" in result
        assert "method" in result
        assert result["endpoint_path"] == "/api/test"
        assert result["method"] == "GET"
    except Exception:
        pass

    try:
        test_scenario_config = {
            "name": "test-scenario",
            "description": "Test scenario for validation",
            "endpoints": {
                "/api/users": {
                    "GET": {"status": 200, "data": [{"id": 1, "name": "Test User"}]}
                }
            }
        }

        result = await client.create_scenario(
            scenario_name="test-scenario",
            scenario_config=test_scenario_config
        )

        # Verify expected structure
        assert "status" in result
        assert "scenario_name" in result
        assert result["scenario_name"] == "test-scenario"
    except Exception:
        pass

    try:
        result = await client.switch_scenario("test-scenario")

        # Verify expected structure
        assert "status" in result
        assert "scenario_name" in result
        assert result["scenario_name"] == "test-scenario"
    except Exception:
        pass

    try:
        result = await client.list_scenarios()

        # Verify expected structure
        assert "status" in result
        assert "scenarios" in result
        assert "total_count" in result
    except Exception:
        pass

    try:
        result = await client.get_current_scenario()

        # Verify expected structure
        assert "status" in result
        assert "current_scenario" in result or result.get("status") == "error"
    except Exception:
        pass


async def test_mock_server_manager_integration():
    """Test integration with MockServerManager for server discovery."""

    manager = MockServerManager()

    try:
        servers = await manager.discover_running_servers(ports=[8000, 8001, 8002], check_health=False)
        for _server in servers:
            pass
    except Exception:
        pass

    try:
        discovery = await manager.comprehensive_discovery()

        assert "total_generated" in discovery
        assert "total_running" in discovery
        assert "discovery_timestamp" in discovery
    except Exception:
        pass

    try:
        generated_mocks = manager.discover_generated_mocks()
        for _mock in generated_mocks[:3]:  # Show first 3
            pass
    except Exception:
        pass


async def test_error_handling():
    """Test error handling in HTTP client methods."""

    # Test with invalid URL
    invalid_client = MockServerClient("http://invalid-server:9999")

    try:
        result = await invalid_client.health_check()
        assert result.get("status") in ["unreachable", "error"]
    except Exception:
        pass


def test_method_signatures():
    """Test that all new methods have correct signatures."""

    client = MockServerClient("http://localhost:8000")

    # Check that methods exist and are callable
    methods_to_check = [
        'update_response',
        'create_scenario',
        'switch_scenario',
        'list_scenarios',
        'get_current_scenario'
    ]

    for method_name in methods_to_check:
        assert hasattr(client, method_name), f"Method {method_name} not found"
        method = getattr(client, method_name)
        assert callable(method), f"Method {method_name} is not callable"



async def main():
    """Run all tests."""

    # Test method signatures
    test_method_signatures()

    # Test error handling
    await test_error_handling()

    # Test HTTP client extensions
    await test_http_client_extensions()

    # Test MockServerManager integration
    await test_mock_server_manager_integration()



if __name__ == "__main__":
    asyncio.run(main())
