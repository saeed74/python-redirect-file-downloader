import requests
import os 

def download(url, name, path):

    # note: we was using wget -O at first place. that was not a good option at all
    # some hostings use 301 redirect and wget was saving html page as key.jks file
    # it took me 3 days to find out that problem is downloaded file not jdk version and OS
    # problem for 301 redirect can solve with curl -O -J -L:
    # https://unix.stackexchange.com/a/74337/434600
    # but its also not good option because debugging is difficult with os command,
    # with help of mehdi we now using build-in request method to download files
    # from URLs and save them as a file:
    
    headers = {}
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Accept"] = "*/*"
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"

    try:
        response = requests.get(url, stream=True, allow_redirects=True, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        print('HERE')
        print("our header : ",headers)
        print("respone headers  : ", response.headers)
        if response.status_code == 301 or response.status_code == 302:
            print("status : ", response.status_code)
            print("headers 2 : ", response.headers)

            new_url = response.headers['Location']
            response = requests.get(new_url, stream=True, allow_redirects=True, headers=headers)
            print("new status code : ", response.status_code)
            print("headers 3 : ", response.headers)

            response.raise_for_status()  # Raise an exception if the request was unsuccessful

        # Save the file in the specified directory
        output_path = os.path.join(path, name)
        with open(output_path , 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File {name} downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
        print("lets try with http..")
        url2 = url.replace('https://','http://')
        try:
            response = requests.get(url2, stream=True, headers=headers)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            # Save the file in the specified directory
            output_path = os.path.join(path, name)
            with open(output_path , 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"File {name} downloaded successfully. (2nd way)")
        except requests.RequestException as e:
            print(f"(2nd way http) Error downloading file from {url}: {e}")



#download("https://appchemistry.dabirmodern.ir/files/export-files/keyas(10).jks","keyas(10).jks","")
download("https://appchemistry.dabirmodern.ir/files/test/keyas.jks","keyas.jks","")