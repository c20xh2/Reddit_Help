import subprocess

domains = ['iana.org']

for domain in domains:
    filename = f'emails_{domain}.json'
    subprocess.run(['py', '-m', 'scrapy', 'crawl', 'email_spider', '-a', f'domain={domain}', '-o', filename])
