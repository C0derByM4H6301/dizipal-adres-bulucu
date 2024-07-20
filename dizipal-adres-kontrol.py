import requests
from rich import print                   
import argparse
import time
from yaspin import yaspin                        
from colorama import Fore, init
init(autoreset=True)                                    
from yaspin.spinners import Spinners
parser=argparse.ArgumentParser(description="Mahmut(Paşa) tarafından kodlanmıştır. https://github.com/X0derByM4H6301")
parser.add_argument("-rn","--range_min", type=int, default=0,help="Range minumum değer, tipi tam sayı. defailt 0")                      
parser.add_argument("-rx","--range_max", type=int, default=1000,help="Range maksimum değer, tipi tam sayı. default 1000") 
parser.add_argument("-u","--urlonly", action="store_true",help="Sadece URL ekrana bastırır")                     
parser.add_argument("-s","--showdied",action="store_true",help="Canlı olmayan linkleri ekrana basar")                
parser.add_argument("-t","--timeout", type=int,default=1, help="Url başına maksimum kontrol süresi. Default 1")
parser.add_argument("-b","--byteoutput",action="store_true",help="Anasayfa byte boyutlarının yazılmasını engeller.")
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
                                                                      
spinner = yaspin(Spinners.line,text="Adresler kontrol ediliyor...", color="blue")#,side="right" )
if not args.byteoutput:                                     
    print("[red underline]uyarı![/] genellikle 40000 byte altı sayfa boyutu o domainin dizipal değil host servisince canlı tutulduğunun göstergesidir.")
#print(args)                                                          
spinner.start()                                    
url = "https://dizipal{}.com"
for i in range(args.range_min,args.range_max+1):            
    url_to_check = url.format(i)
    spinner.text = f"{Fore.CYAN}{url_to_check}{Fore.RESET} adresi kontrol kontrol ediliyor..."
#    print(url_to_check)                                
    if is_live(url_to_check):
        if args.urlonly == False:                              
            if not args.byteoutput:
                spinner.write(f"Bu URL {Fore.GREEN}{url_to_check}{Fore.RESET} canlı, ({Fore.CYAN}{get_size(url_to_check)}{Fore.RESET}) byte")
            else:                                              
                spinner.write(f"Bu URL {Fore.GREEN}{url_to_check}{Fore.RESET} canlı.")                              
        if args.urlonly == True:
            spinner.write(f"{Fore.GREEN}{url_to_check}{Fore.RESET}")  
    if is_live(url_to_check) == False:
        if args.showdied:
            if args.urlonly:                                   
                spinner.write(f"{Fore.RED}{url_to_check}{Fore.RESET}")
            else:                     
                spinner.write(f"Bu URL {Fore.RED}{url_to_check}{Fore.RESET} canlı değil")                       
spinner.stop() 
