from concurrent.futures import ThreadPoolExecutor
import sys
import time
import requests

G = '\033[1;32m'
R = '\033[1;31m'

print((G + """
  _____________ _____________  ___ ___    _____    _________ ___ ___ .___  _________
 /   _____/    |   \\______   \\/   |   \\  /  _  \\ /   _____//   |   \\|   |/   _____/
 \\_____  \\|    |   /|    |  _/    ~    \\/  /_\\  \\ \\_____  \\    ~    \\   |\\_____  \\ 
 /        \\    |  / |    |   \\    Y    /    |    \\/        \\    Y    /   |/        /
/_______  /______/  |______  /\\___|_  /\\____|__  /_______  /\\___|_  /|___/_______  /
        \\/                 \\/       \\/         \\/        \\/       \\/             \\/ 

"""))

print("                                 Best Fuzzing Tool      ")
print('\n')

wordlist = []
res = []

def loads():
    animation = [
        "[■□□□□□□□□□□□□□□]",
        "[■■□□□□□□□□□□□□□]",
        "[■■■□□□□□□□□□□□□]",
        "[■■■■□□□□□□□□□□□]",
        "[■■■■■□□□□□□□□□□]",
        "[■■■■■■□□□□□□□□□]",
        "[■■■■■■■□□□□□□□□]",
        "[■■■■■■■■□□□□□□□]",
        "[■■■■■■■■■□□□□□□]",
        "[■■■■■■■■■■□□□□□]",
        "[■■■■■■■■■■■□□□□]",
        "[■■■■■■■■■■■■□□□]",
        "[■■■■■■■■■■■■■□□]",
        "[■■■■■■■■■■■■■■□]",
        "[■■■■■■■■■■■■■■■]"
    ]
    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r\t\t\t" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")

def fetch_and_merge_wordlists(*urls):
    for url in urls:
        print(G+"[*] Staring Action Be Ready...")
        print('\n')
        with requests.get(url) as response:
            for line in response.iter_lines():
                wordlist.append(line.decode("utf-8"))
    loads()

def make_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open("scan_result.txt", "a") as a:
                a.write(f"{url}\n")
                res.append(url)
            print('\n')
            print(G+f"[*] Found Yahh : {url} => [{response.status_code}]")     
            print('\n')
        else:
            print(R+f"[*] Trying Hard : {url} => [{response.status_code}]")
    except Exception as e:
        pass

def main():
    input_url = input("[=>] Enter the URL : ")
    input_url = input_url.lower().replace("http://", "").replace("https://", "").replace("www.", "").rstrip("/")
    wordlistss = int(input("[=>] Enter 1 for common fuzz, 2 for parameter fuzz, or 3 for both Fuzz : "))

    if wordlistss == 1:
        fetch_and_merge_wordlists("http://ffuf.me/wordlist/common.txt")
    elif wordlistss == 2:
        fetch_and_merge_wordlists("http://ffuf.me/wordlist/parameters.txt")
    elif wordlistss == 3:
        fetch_and_merge_wordlists("http://ffuf.me/wordlist/parameters.txt", "http://ffuf.me/wordlist/common.txt")
    else:
        print("please Select a valid option Run again the program")
        exit()
    
    base_url = f"http://{input_url}/{{element}}"

    urls_to_check = [base_url.format(element=element) for element in wordlist]
    with ThreadPoolExecutor(20) as executor:
        executor.map(make_request, urls_to_check)
    if res:
        with open("scan_result.txt", "w") as file:
                    file.write("\n".join(res))
if __name__ == "__main__":
    main()
