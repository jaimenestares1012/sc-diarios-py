from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from bd.mongo import insertarMongo
from utils.functions import urlnoticia, hashear
from datetime import datetime

class Principal():
    def __init__(self, url, fecha_scraping):
        self.url = url
        self.fecha_scraping = fecha_scraping
        
        # Crear instancia de UserAgent
        ua = UserAgent()

        # Obtener un agente de usuario aleatorio
        user_agent = ua.random

        # Crear opciones del controlador
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')

        try:
            self.driver = webdriver.Remote(command_executor='http://192.168.54.215:4444/wd/hub', desired_capabilities=options.to_capabilities())
            self.wait = WebDriverWait(self.driver, 10)
        except:
            pass
        print(" 1 - Inicio abrir webdriver y navegador ")
        

    def logica(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        # container = self.driver.find_element(By.CLASS_NAME , 'paginated-list--infinite')
        noticias = self.driver.find_elements(By.CLASS_NAME , 'ListSection_list__section--item__zeP_z')
        
        # fecha_scraping = 

        # Convertir el string en un objeto datetime
        isend = False
        fecha_actual = datetime.strptime(self.fecha_scraping, "%Y-%m-%d").date()
        arrayNoticias = []
        scroll_distance = 5000
        self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

        for noticia in noticias:
            try:
                url = noticia.find_element(By.XPATH,  './div/h2/a').get_attribute('href')
                url_img = noticia.find_element(By.XPATH,  './figure/img').get_attribute('src')
                fecha_publicada = noticia.find_element(By.XPATH,  './div/div/time').text.split('|')[1].strip() 
                fecha_publicada_obj = datetime.strptime(fecha_publicada, "%d/%m/%Y").date()
                if fecha_publicada_obj == fecha_actual:
                    data = {
                        "url": url,
                        'url_img': url_img
                    }
                    arrayNoticias.append(data)
                    isend = True
                else:
                    print("Noticia fuera de fecha")
                    isend = False       
            except Exception as e:
                print("Error:", str(e))
                time.sleep(10)
                self.driver.quit()
                pass

        
        if isend:
            print("Click botón, ver más")
            time.sleep(3)
            self.driver.find_element(By.CLASS_NAME , 'ShowMoreButton_showMore__button__so1IY ').click()
            time.sleep(4)
            noticias2 = self.driver.find_elements(By.CLASS_NAME , 'ListSection_list__section--item__zeP_z')
            for noticia in noticias2[24:]:
                try:
                    url = noticia.find_element(By.XPATH,  './div/h2/a').get_attribute('href')
                    fecha_publicada = noticia.find_element(By.XPATH,  './div/div/time').text.split('|')[1].strip() 
                    fecha_publicada_obj = datetime.strptime(fecha_publicada, "%d/%m/%Y").date()
                    if fecha_publicada_obj == fecha_actual:
                        data = {
                            "url": url,
                            'url_img': url_img
                        }
                        arrayNoticias.append(data)
                        isend = True
                    else:
                        print("Noticia fuera de fecha")
                        isend = False       
                except Exception as e:
                    print("Error:", str(e))
                    time.sleep(10)
                    self.driver.quit()
                    pass
        

        for noticia in arrayNoticias:
            try:
                url_noticia = noticia['url']
                url_img = noticia['url_img']
                self.driver.get(url_noticia)
                time.sleep(5)
                scroll_distance = 500
                self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                time.sleep(5)
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                interna_content = soup.find(id="interna_content")
                datos = interna_content.find('div')
                datetime_str = datos.find('time')['datetime']
                contexto = datos.find('span')
                fecha_datetime = datetime.fromisoformat(datetime_str)
                timestamp = fecha_datetime.timestamp() * 1000
                titulo = interna_content.find('h1')
                subtitulo = interna_content.find('h2')

                MainContent_main__body__i6gEa = interna_content.find(class_="MainContent_main__body__i6gEa")    
                parrafos = MainContent_main__body__i6gEa.find_all('p')


                # Recorrer cada elemento de la lista parrafos
                for parrafo in parrafos:
                    # Extraer el contenido del párrafo eliminando las etiquetas HTML
                    texto_limpio = ''.join(parrafo.findAll(text=True))
                    # Agregar el párrafo limpio a la lista parrafos_limpios
                    print("<------------->")
                    urlParrafo = urlnoticia(url_noticia, texto_limpio.strip())
                    
                    json_limpio = {
                        'id':  hashear(urlParrafo),
                        'source_place': '2dfa9ecb0179a4e4',
                        'sample_lang': 'es',
                        'sample_app': 'web',
                        'source_snetwork_id': 'nws',
                        'sample_created_at': timestamp,
                        'sample_text': texto_limpio.strip(),
                        'sample_link': urlParrafo,
                        'author_id': 'md5pordefinir',
                        'author_fullname': 'Diario La República',
                        'author_photo': 'Fotobds3',
                        'author_screen_name': 'larepublica.pe',
                        'sample_post_author_id': 'md5pordefinir',
                        'sample_post_author': 'Diario La República', 
                        'sample_post_author_photo': 'Fotobds3',
                        'sample_post_id': hashear(url_noticia), 
                        'sample_post_text': titulo.text.strip().replace('\\"', '"').replace("\\'", "'") + subtitulo.text.strip().replace('\\"', '"').replace("\\'", "'"), 
                        'sample_post_created_at': timestamp,
                        'sample_post_image': url_img,
                        'sample_post_link': url_noticia
                    }

                    print(json_limpio)
                    insertarMongo(json_limpio, "politica")
                time.sleep(10)
            except Exception as e:
                print("Error:", str(e))
                time.sleep(20)
                pass
        self.driver.quit()

    def extraData(self, html):
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find('div')
        print("div", div)
        h1 = div.find('h1')
        h2 = div.find('h2')
        # tbody = div.find('tbody')
        print("h1", h1)
        print("h2", h2)
        # titulo = self.driver.find_element(By.XPATH , '/html/body/div[1]/div/div[4]/div[2]/h1').text
        # print("titulo", titulo)
        return 0