from src.soporte_extraccion_doma import extraccion_doma_nac, extraccion_doma_int
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")

url = url_scrapeo

if __name__ == "__main__":
 
    extraccion_doma_nac(url)
    extraccion_doma_int(url)