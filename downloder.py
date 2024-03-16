import os
import requests
from bs4 import BeautifulSoup

main_folder = "omniscient_reader's_viewpoint_manga_downloads"
os.makedirs(main_folder, exist_ok=True)
for i in range(1, 'bölüm sayısı'): # manga bölüm sayısını yazın

    folder_name = f"bolum-{i}"
    folder_path = os.path.join(main_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    manga_url = f"https://manga-sitesi/bolum-{i}/" # manga sitesi linkini yazın 
    response = requests.get(manga_url)
    soup = BeautifulSoup(response.content, "html.parser")

    manga_pages = soup.find_all("img", {"class": "wp-manga-chapter-img"}) # class ismi değişebilir

    manga_page_list = []

    for page in manga_pages:
        manga_page = page.get('data-src') # data-src, src veya başka bir şey olabilir
        manga_page_list.append(manga_page)

    with open(os.path.join(folder_path, f"bolum-{i}.sh"), "w") as f:
        f.write('curl -# -K - <<URL \n')
        index = 1
        for page in manga_page_list:
            f.write(f'url="{page.lstrip()}" \n output="{index}.webp"\n')
            index += 1
        f.write('URL\n')
        # Gerekirse convert komutunu ekle (webp to jpg)
        # f.write('for file in *.webp; do\n')
        # f.write('\tconvert "$file" "${file%.webp}.jpg"\n')
        # f.write('\trm "$file"\n')
        # f.write('done\n')

with open(os.path.join(main_folder, "download_all.sh"), "w") as f:
    for i in range(1, 197):
        folder_name = f"bolum-{i}"
        f.write(f'echo "bolum-{i}" && cd {folder_name} && bash bolum-{i}.sh && cd ..\n')