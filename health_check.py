#!/usr/bin/env python3
"""
Health Check Module for Python Automation API

Módulo de health check que verifica el estado de los componentes
del sistema: servicio principal, conexión a base de datos y APIs externas.

Uso:
    from health_check import HealthChecker

    health = HealthChecker()
    result = health.check_all()
    print(result)

Endpoints:
    - /health - Estado general
    - /health/ready - Verificación de preparación
    - /health/live - Verificación de vida

Configuración via .env:
    HEALTH_CHECK_INTERVAL=30
    HEALTH_CHECK_TIMEOUT=10
"""
import sys
import os
import logging
from pathlib import Path
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthChecker:
    """Verificador de salud del sistema y componentes"""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.checks = {}

    def check_service(self) -> Dict[str, Any]:
        """Verifica el estado del servicio principal"""
        try:
            # Verify main module is importable
            import main
            return {
                'status': 'healthy',
                'service': 'python-automation-api',
                'version': getattr(main, '__version__', '2.0.0')
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

    def check_database(self) -> Dict[str, Any]:
        """Verifica conexión a Oracle Database"""
        try:
            import oracledb

            dsn = os.getenv('ORACLE_DSN', 'localhost:1521/orclpdb1')
            user = os.getenv('ORACLE_USER')
            password = os.getenv('ORACLE_PASSWORD')

            if not user or not password:
                return {
                    'status': 'skipped',
                    'reason': 'Oracle credentials not configured'
                }

            conn = oracledb.connect(user=user, password=password, dsn=dsn)
            conn.close()

            return {
                'status': 'healthy',
                'database': 'oracle',
                'dsn': dsn
            }
        except ImportError:
            return {
                'status': 'skipped',
                'reason': 'oracledb not installed'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

    def check_environment(self) -> Dict[str, Any]:
        """Verifica variables de entorno críticas"""
        required = ['ORACLE_USER', 'ORACLE_PASSWORD']
        optional = ['ALLOWED_ORIGINS', 'RATE_LIMIT', 'LOG_LEVEL']

        missing = [v for v in required if not os.getenv(v)]

        return {
            'status': 'healthy' if not missing else 'degraded',
            'missing_required': missing,
            'configured_optional': [v for v in optional if os.getenv(v)]
        }

    def check_all(self) -> Dict[str, Any]:
        """Ejecuta todos los health checks"""
        self.checks = {
            'service': self.check_service(),
            'database': self.check_database(),
            'environment': self.check_environment()
        }

        overall = 'healthy'
        for check in self.checks.values():
            if check.get('status') == 'unhealthy':
                overall = 'unhealthy'
                break
            elif check.get('status') == 'degraded':
                overall = 'degraded'

        return {
            'overall': overall,
            'checks': self.checks
        }


def main():
    """CLI para ejecutar health checks"""
    checker = HealthChecker()

    print("=" * 50)
    print("🔍 Python Automation - Health Check")
    print("=" * 50)

    result = checker.check_all()

    for check_name, check_result in result['checks'].items():
        status = check_result.get('status', 'unknown')
        icon = {'healthy': '✅', 'unhealthy': '❌', 'degraded': '⚠️', 'skipped': '⏭️'}.get(status, '❓')
        print(f"{icon} {check_name}: {status}")

        if 'error' in check_result:
            print(f"   Error: {check_result['error']}")
        if 'reason' in check_result:
            print(f"   Reason: {check_result['reason']}")

    print()
    print(f"Overall: {result['overall'].upper()}")

    sys.exit(0 if result['overall'] == 'healthy' else 1)


if __name__ == '__main__':
    main()
