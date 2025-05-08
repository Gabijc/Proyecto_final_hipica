from src.soporte_extraccion_completo import extraccion_completo_nac, extraccion_completo_int
import os 
from dotenv import load_dotenv

load_dotenv()
url_scrapeo = os.getenv("url_scrapeo")

url = url_scrapeo

if __name__ == "__main__":

    extraccion_completo_nac(url)
    extraccion_completo_int(url)