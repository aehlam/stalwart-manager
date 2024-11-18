# Usage Guide

## Quick Start

1. Start the service:
```bash
stalwart-manager
```

2. Open web interface at `http://localhost:8000`

3. Enter required information:
   - Domain name
   - Cloudflare credentials
   - Admin email

## Configuration Guide

### Basic Configuration

The Stalwart Manager is configured for sending 50,000 emails per day with proper rate limiting and compliance settings.

### Rate Limits

- SMTP (Port 25):
  - 50 concurrent connections per IP
  - 100 messages per connection
  - 1000 recipients per connection
  - 10 errors before temporary block

- Submission (Port 587):
  - 35 messages per minute
  - 100 recipients per message
  - 10 concurrent connections
  - Throttling after 1000 messages

### CAN-SPAM Compliance

The server is configured to enforce:
- Required List-Unsubscribe header
- Physical address requirement
- Unsubscribe link requirement
- Maximum spam score threshold
- DKIM signing
- SPF checking

### DNS Configuration

After deployment, you need to add these DNS records:

1. **SPF Record**
```
TXT @ "v=spf1 ip4:YOUR_SERVER_IP ~all"
```

2. **DKIM Record**
```
TXT mail._domainkey "v=DKIM1; k=rsa; p=YOUR_PUBLIC_KEY"
```

3. **DMARC Record**
```
TXT _dmarc "v=DMARC1; p=none; rua=mailto:admin@yourdomain.com"
```

### Monitoring

The server provides monitoring through:
- Detailed logging
- Bounce tracking
- Complaint tracking
- Performance metrics (every 60 seconds)

## Management Tasks

### Creating Email Accounts

1. Access management interface at `http://your-server:8080`
2. Log in with admin credentials
3. Navigate to "Accounts"
4. Click "Add Account"

### Managing Rate Limits

1. Access config file at `/etc/stalwart/config.toml`
2. Modify rate limit settings
3. Restart service:
```bash
docker restart stalwart-mail
```

### Viewing Logs

```bash
docker logs stalwart-mail
```

### Backup and Restore

Backup:
```bash
stalwart-manager backup create
```

Restore:
```bash
stalwart-manager backup restore <backup-file>
```

## Best Practices

### IP Warm-up Schedule

Week 1:
- Day 1-2: 5,000 emails/day
- Day 3-4: 10,000 emails/day
- Day 5-7: 20,000 emails/day

Week 2:
- Day 8-10: 30,000 emails/day
- Day 11-14: 40,000 emails/day

Week 3:
- Day 15+: 50,000 emails/day

### List Hygiene

1. Remove bounces immediately
2. Process unsubscribes within 10 days
3. Clean inactive subscribers (6+ months)
4. Validate email syntax before sending

### Monitoring Health

1. Check bounce rates (keep under 2%)
2. Monitor complaint rates (keep under 0.1%)
3. Track delivery rates (aim for 98%+)
4. Review spam scores regularly

## Troubleshooting

### Common Issues

1. **High Bounce Rates**
   - Check email list quality
   - Verify DNS records
   - Review sending patterns

2. **Delivery Issues**
   - Check IP reputation
   - Verify SPF/DKIM alignment
   - Review authentication logs

3. **Performance Issues**
   - Monitor system resources
   - Check rate limit settings
   - Review queue size

### Getting Help

1. Check logs:
```bash
docker logs stalwart-mail
```

2. View configuration:
```bash
cat /etc/stalwart/config.toml
```

3. Check system resources:
```bash
docker stats stalwart-mail
```

## Security

### Best Practices

1. Use strong passwords
2. Enable TLS for all connections
3. Regular security updates
4. Monitor authentication logs
5. Implement IP allowlisting

### Compliance

1. Maintain clear unsubscribe process
2. Include physical address
3. Honor unsubscribe requests
4. Keep records of consent
5. Monitor bounce/complaint rates
