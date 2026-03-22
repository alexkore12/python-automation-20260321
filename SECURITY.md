# Security Policy

## 🔴 Recent Security Alerts

### Trivy Supply Chain Attack (March 2026)

**⚠️ ALERT:** Trivy versions 0.69.4 and GitHub Actions (aquasecurity/setup-trivy, aquasecurity/trivy-action) have been compromised in a supply chain attack. 

**Affected versions:**
- Trivy CLI v0.69.4 (malicious)
- GitHub Actions: `aquasecurity/setup-trivy`
- GitHub Actions: `aquasecurity/trivy-action`

**Recommendations:**
1. **Do NOT use** Trivy v0.69.4
2. **Do NOT use** the compromised GitHub Actions
3. Use alternative scanners: Grype, Checkov
4. Pin to specific known-good versions
5. Verify checksums before running any security tool

**References:**
- GHSA: Check GitHub Advisory Database
- Related: CVE-2024-21626

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | ✅                 |
| < 1.0   | ❌ End of Life     |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it via GitHub Issues or contact the maintainer directly.

**Do NOT report security vulnerabilities in public issues.**

## Security Best Practices

### For This Project

1. **Never commit secrets** - Use environment variables
2. **Validate input** - All user input validated via Pydantic
3. **Use parameterized queries** - Prevent SQL injection
4. **Limit CORS** - Don't use `*` in production
5. **Rate limiting** - Implement request limits
6. **HTTPS only** - Never serve over plain HTTP in production
7. **Oracle Wallet** - Use for database credentials in production

### Dependency Security

- Run `pip-audit` regularly
- Use Dependabot alerts
- Pin dependency versions
- Review security advisories weekly

```bash
# Scan for vulnerabilities
pip-audit

# Freeze versions for reproducibility
pip freeze > requirements.lock
```

## Security Updates

- **2026-03-21**: Added supply chain attack warning for Trivy
- **2026-03-21**: Documented alternative scanners (Grype, Checkov)

---

*Last updated: 2026-03-21*
