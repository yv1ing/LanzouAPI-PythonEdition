import re
import json
import secrets
import string
import http.client
from urllib.parse import urlparse, parse_qs


def generate_random_str(length=16):
    chars = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def parse_link(src):
    parsed_url = urlparse(str(src))
    query_params = parse_qs(parsed_url.query)
    base_url = parsed_url.netloc
    file_path = parsed_url.path.strip('/')
    file_pass = query_params.get("pwd", [None])[0]

    conn = http.client.HTTPSConnection(base_url)
    conn.request('GET', f'/{file_path}')
    resp = conn.getresponse()
    html = resp.read().decode('utf-8')
    file_match = re.search(r'file=(\d+)', html)
    file = file_match.group(1) if file_match else None
    sign_matches = re.findall(r"'sign':'(.*?)'", html)
    sign = sign_matches[1] if sign_matches else None
    
    random_str = generate_random_str()
    headers = {
        'Referer': f'https://www.lanzoup.com/{file_path}',
        'Content-Type': f'multipart/form-data; boundary=------------------------{random_str}',
    }

    conn = http.client.HTTPSConnection('www.lanzoux.com')
    conn.request(
        method='POST',
        url=f'/ajaxm.php?file={file}',
        body=f'--------------------------{random_str}\nContent-Disposition: form-data; name="action"\n\ndownprocess\n--------------------------{random_str}\nContent-Disposition: form-data; name="sign"\n\n{sign}\n--------------------------{random_str}\nContent-Disposition: form-data; name="p"\n\n{file_pass}\n--------------------------{random_str}\nContent-Disposition: form-data; name="kd"\n\n1\n--------------------------{random_str}--',
        headers=headers,
    )

    resp = conn.getresponse()
    url = json.loads(resp.read().decode('utf-8'))['url']
    headers = {
        'Referer': 'https://developer.lanzoug.com',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    conn = http.client.HTTPSConnection('developer-oss.lanrar.com')
    conn.request(
        method='GET',
        url=f'/file/{url}',
        headers=headers,
    )
    resp = conn.getresponse()

    return resp.getheader('Location')


if __name__ == '__main__':
    src = 'https://wwu.lanzoue.com/xxxxxxx?pwd=xxxx'
    link = parse_link(src)
    print(link)
