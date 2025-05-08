from src.soporte_extraccion_completo import extraccion_completo_nac, extraccion_completo_int


if __name__ == "__main__":

    url = "https://rfhe.com/competiciones/"  
    extraccion_completo_nac(url)
    extraccion_completo_int(url)