import threading
import time
import random
import requests
from rich import print                   
import argparse
import time                   

parser=argparse.ArgumentParser(description="Mahmut(Paşa) tarafından kodlanmıştır. https://github.com/X0derByM4H6301")
parser.add_argument("-rn","--range_min", type=int, default=0,help="Range minumum değer, tipi tam sayı. defailt 0")                      
parser.add_argument("-rx","--range_max", type=int, default=1000,help="Range maksimum değer, tipi tam sayı. default 1000") 
parser.add_argument("-u","--urlonly", action="store_true",help="Sadece URL ekrana bastırır")                     
parser.add_argument("-s","--showdied",action="store_true",help="Canlı olmayan linkleri ekrana basar")                
parser.add_argument("-to","--timeout", type=int,default=5, help="Url başına maksimum kontrol süresi. Default 5")
parser.add_argument("-b","--byteoutput",action="store_true",help="Anasayfa byte boyutlarının yazılmasını engeller.")
parser.add_argument("-th","--threads", type=int, default=5, help="Threads sayısı artıkça arama işlemi hızlanır. Default 5")
args = parser.parse_args()
#print(args)                                                          
def is_live(url):
    try:
        response = requests.get(url, timeout=args.timeout)
        if response.status_code == 200:
            return True                                      
        else:
            return False                   
    except requests.RequestException:
        return False                                                  
def get_size(url):                             
    response = requests.get(url)
    response.raise_for_status()                                       
    page_size = len(response.content)                       
    return page_size
                                                                      
if not args.byteoutput:                                     
    print("[red underline]uyarı![/] genellikle 40000 byte altı sayfa boyutu o domainin dizipal değil host servisince canlı tutulduğunun göstergesidir.")
#print(args)                                                          
def checker(i):
    url = "https://dizipal{}.com"          
    url_to_check = url.format(i)                        
    if is_live(url_to_check):
        if args.urlonly == False:                              
            if not args.byteoutput:
                print(f"Bu URL [green]{url_to_check}[/] canlı, ([cyan]{get_size(url_to_check)}[/]) byte")
            else:                                              
                print(f"Bu URL [green]{url_to_check}[/] canlı.")                              
        if args.urlonly == True:
            print(f"[green]{url_to_check}[/]")  
    if is_live(url_to_check) == False:
        if args.showdied:
            if args.urlonly:                                   
                print(f"[red]{url_to_check}[/]")
            else:                     
                print(f"Bu URL [red]{url_to_check}[/] canlı değil")

yazilar = [i for i in range(args.range_min,args.range_max+1)]
thread_sayisi = args.threads
baslangic_index = 0
time_out = args.timeout
while baslangic_index < len(yazilar):
    son_index = min(baslangic_index + thread_sayisi, len(yazilar))
    threads = []

    for i in range(baslangic_index, son_index):
        t = threading.Thread(target=checker, args=(yazilar[i],))
        t.start()
        threads.append(t)

        # Thread'lerin tamamlanmasını bekle ve 5 saniye içinde tamamlanmayanları sonlandır
    for t in threads:
        t.join(timeout=time_out)
        if t.is_alive():
            #print(f"Thread {t} {time_out} saniye içinde tamamlanamadı, sonlandırılıyor...")
            t.join()

        baslangic_index += thread_sayisi
