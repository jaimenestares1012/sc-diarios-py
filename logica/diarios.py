from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from bd.mongo import insertarMongo, buscarMongo, deletearMongo

class Principal():
    def __init__(self, url):
        self.url = url
        
        # Crear instancia de UserAgent
        ua = UserAgent()

        # Obtener un agente de usuario aleatorio
        user_agent = ua.random

        # Crear opciones del controlador
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')

        try:
            self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=options.to_capabilities())
            self.wait = WebDriverWait(self.driver, 10)
        except:
            pass
        print(" 1 - Inicio abrir webdriver y navegador ")
        

    def logica(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        # container = self.driver.find_element(By.CLASS_NAME , 'paginated-list--infinite')
        noticias = self.driver.find_elements(By.CLASS_NAME , 'ListSection_list__section--item__zeP_z')
        print("len", len(noticias))
        
        print()
        # i = 0
        # while i < 10:
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     i = i + 1
        #     time.sleep(3)
        arrayArreglos = []
        for noticia in noticias:
            scroll_distance = 500
            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            try:

                url = noticia.find_element(By.XPATH,  './div/h2/a').get_attribute('href')
                arrayArreglos.append(url)
                # time.sleep(12)
                # ventanas = self.driver.window_handles
                # print(ventanas)
                # time.sleep(10)

                # html = self.driver.page_source
                # soup = BeautifulSoup(html, "html.parser")
                # div = soup.find('div')
                # h1 = div.find('h1')
                # h2 = div.find('h2')
                # # tbody = div.find('tbody')
                # print("h1", h1)
                # print("h2", h2)
               

            except Exception as e:
                print("Error:", str(e))
                time.sleep(20)
                self.driver.quit()
                pass

        for visita in arrayArreglos:
            try:
                print("visita", visita)
                self.driver.get(visita)
                time.sleep(5)
                # interna_content = self.driver.find_elements(By.ID , 'interna_content')

                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                interna_content = soup.find(id="interna_content")
                datos = interna_content.find('div')
                datetime_str = datos.find('time')['datetime']
                contexto = datos.find('span')
                print("datetime_str", datetime_str)
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
                    json = {
                        'titulo': titulo.text.strip(),
                        'subtitulo': subtitulo.text.strip(),
                        'contexto': contexto.text.strip(),
                        'datetime_str': datetime_str,
                        'parrafos_limpios': texto_limpio.strip()
                    }
                    print("json", json)
                    json_limpio = {
                        'source_place': '2dfa9ecb0179a4e4',
                        'sample_lang': 'es',
                        'sample_app': 'web',
                        'source_snetwork_id': 'nws',
                        'sample_created_at': json['datetime_str'],
                        'sample_text': json['parrafos_limpios'].strip(),
                        'sample_link': '',
                        'author_id': '',
                        'author_fullname': 'La Republica',
                        'author_photo': '',
                        'author_screen_name': 'larepublica.pe',
                        'sample_post_author_id': '',
                        'sample_post_author': 'La Republica', 
                        'sample_post_author_photo': '',
                        'sample_post_id': '', 
                        'sample_post_text': json['titulo'].replace('\\"', '"').replace("\\'", "'") + json['contexto'].replace('\\"', '"').replace("\\'", "'"), 
                        'sample_post_created_at': 1684411320000,
                        'sample_post_image': '',
                        'sample_post_link': ''
                                            
                        # 'titulo': ,
                        # 'subtitulo': json['subtitulo'].replace('\\"', '"').replace("\\'", "'"),
                        # 'contexto': json['contexto'].replace('\\"', '"').replace("\\'", "'"),
                        # 'datetime_str': json['datetime_str'],
                    }

                    print(json_limpio)
                    insertarMongo(json_limpio, "politica")

                # Imprimir el arreglo de párrafos limpios

                # json = {
                #     'titulo': titulo.text.strip(),
                #     'subtitulo': subtitulo.text.strip(),
                #     'contexto': contexto.text.strip(),
                #     'datetime_str': datetime_str,
                #     'parrafos_limpios': parrafos_limpios
                # }
                # print("JSON-------->", json)
            
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