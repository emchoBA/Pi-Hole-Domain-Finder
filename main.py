import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import socket


def get_domains(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')

    links = set()
    tags = ['a', 'ad', 'img', 'script', 'link', 'iframe']
    for tag in soup.find_all(tags):
        href = tag.get('href') or tag.get('src')
        if href:
            links.add(urljoin(url, href))

    domains = set()
    for link in links:
        parsed_url = urlparse(link)
        if parsed_url.netloc:
            if "ad" in parsed_url.netloc:
                print(parsed_url.netloc + ": Probably is a ad domain!\n")
            domains.add(parsed_url.netloc)

    return domains


def get_ip_addresses(domains):
    ip_addresses = {}
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            ip_addresses[domain] = ip
        except socket.gaierror:
            ip_addresses[domain] = "Unable to resolve"
    return ip_addresses

def main():
    url = input("Enter the website URL to analyze: ")
    print(f"Analyzing {url}...")

    domains = get_domains(url)
    ip_addresses = get_ip_addresses(domains)

    print("\nDomains and their IP addresses:")
    for domain, ip in ip_addresses.items():
        print(f"{domain}: {ip}")
    if len(ip_addresses) != 0:
        print("\n\t*Unable to resolve means Pi-Hole is working!*")


if __name__ == "__main__":
    main()
