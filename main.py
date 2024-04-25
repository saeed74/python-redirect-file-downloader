import requests
import os 
import time

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
        #print("our header : ",headers)
        print("respone_headers : ", response.headers)
        print("status_code: ", response.status_code)

        content_type = response.headers.get('content-type', '').lower()

        print("response content_type: ", content_type)

        if 'text/html' in content_type:

            print("response content_type: ", content_type)
            print("wait 5 second and check cotent type after that")
            time.sleep(5)

            new_content_type = response.headers.get('content-type', '').lower()

            print("new_content_type:" , new_content_type)

        else:

            print("direct download. content_type is: ", content_type)
            # Save the file in the specified directory
            output_path = os.path.join(path, name)
            with open(output_path , 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"File {name} downloaded successfully.")

        

    except requests.RequestException as e:
        print(f"Error downloading file from {url}: {e}")



#download("https://appchemistry.dabirmodern.ir/files/export-files/keyas(10).jks","keyas(10).jks","")
download("https://appchemistry.dabirmodern.ir/files/test/keyas.jks","keyas.jks","")