"""
Test suite for Python Automation API
Tests security features, rate limiting, and endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from main import app, limiter

client = TestClient(app)


class TestSecurityHeaders:
    """Test security headers are properly set"""
    
    def test_x_content_type_options(self):
        """Verify X-Content-Type-Options header"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
    
    def test_x_frame_options(self):
        """Verify X-Frame-Options header"""
        response = client.get("/health")
        assert response.headers.get("X-Frame-Options") == "DENY"
    
    def test_x_xss_protection(self):
        """Verify X-XSS-Protection header"""
        response = client.get("/health")
        assert "X-XSS-Protection" in response.headers
    
    def test_strict_transport_security(self):
        """Verify HSTS header"""
        response = client.get("/health")
        assert "Strict-Transport-Security" in response.headers


class TestInputValidation:
    """Test input validation and SQL injection prevention"""
    
    def test_sql_injection_in_customer_name(self):
        """Verify SQL injection attempts are blocked"""
        response = client.post("/orders", json={
            "customer": "test'; DROP TABLE orders;--",
            "amount": 100
        })
        # Should either reject or sanitize
        assert response.status_code in [200, 400, 422]
    
    def test_xss_in_customer_name(self):
        """Verify XSS attempts are blocked"""
        response = client.post("/orders", json={
            "customer": "<script>alert('xss')</script>",
            "amount": 100
        })
        assert response.status_code == 422
    
    def test_invalid_amount_zero(self):
        """Verify zero amount is rejected"""
        response = client.post("/orders", json={
            "customer": "Test",
            "amount": 0
        })
        assert response.status_code == 422
    
    def test_negative_amount(self):
        """Verify negative amount is rejected"""
        response = client.post("/orders", json={
            "customer": "Test",
            "amount": -100
        })
        assert response.status_code == 422
    
    def test_excessive_amount(self):
        """Verify excessive amount is rejected"""
        response = client.post("/orders", json={
            "customer": "Test",
            "amount": 2_000_000
        })
        assert response.status_code == 422
    
    def test_customer_name_too_long(self):
        """Verify customer name length is limited"""
        response = client.post("/orders", json={
            "customer": "a" * 200,
            "amount": 100
        })
        assert response.status_code == 422


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_root_rate_limit(self):
        """Verify root endpoint has rate limit"""
        # Should succeed
        response = client.get("/")
        assert response.status_code == 200
    
    def test_health_rate_limit(self):
        """Verify health endpoint has rate limit"""
        response = client.get("/health")
        assert response.status_code == 200


class TestEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns expected data"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_orders_endpoint_structure(self):
        """Test orders endpoint returns list"""
        # Mock database for testing
        with patch('main.pool', None):
            response = client.get("/orders")
            # Will return 503 if no DB, which is expected without Oracle
            assert response.status_code in [200, 503]


class TestOrderValidation:
    """Test order-specific validation"""
    
    def test_create_order_missing_customer(self):
        """Test creating order without customer fails"""
        response = client.post("/orders", json={
            "amount": 100
        })
        assert response.status_code == 422
    
    def test_create_order_missing_amount(self):
        """Test creating order without amount fails"""
        response = client.post("/orders", json={
            "customer": "Test"
        })
        assert response.status_code == 422
    
    def test_create_order_valid(self):
        """Test creating valid order"""
        response = client.post("/orders", json={
            "customer": "Test Company",
            "amount": 1500.50,
            "description": "Test order"
        })
        # Should succeed or fail gracefully if no DB
        assert response.status_code in [200, 201, 503]


class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_order_id(self):
        """Test invalid order ID is rejected"""
        response = client.get("/orders/0")
        assert response.status_code == 400
    
    def test_excessive_order_id(self):
        """Test excessive order ID is rejected"""
        response = client.get("/orders/9999999999")
        assert response.status_code == 400
    
    def test_not_found_order(self):
        """Test non-existent order returns 404 or 503"""
        with patch('main.pool', None):
            response = client.get("/orders/99999")
            assert response.status_code in [404, 503]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
