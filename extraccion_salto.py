from src.soporte_extraccion_salto import extraccion_salto_nac, extraccion_salto_int
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")

url = url_scrapeo

if __name__ == "__main__":
 
    extraccion_salto_nac(url)
    extraccion_salto_int(url)