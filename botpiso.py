from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys  # and Krates
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from colorama import init, Fore, Style
from time import sleep, time
from random import randint, choice, uniform
import pickle
import os

init(convert=True)
init(autoreset=True)

bright = Style.BRIGHT
dim = Style.DIM
red = Fore.RED + dim
green = Fore.GREEN + dim
cyan = Fore.CYAN + dim
yellow = Fore.LIGHTYELLOW_EX + dim
blue = Fore.BLUE + dim
white = Fore.WHITE + dim
magenta = Fore.MAGENTA + dim

# Configuracion
LINK_IDEALISTA = "" # Link tablon idealista - https://www.idealista.com/tablon/*****/
FILL_NOMBRE = "" # Nombre
FILL_EDAD = "" # Edad
FILL_EMAIL = "" # Email
FILL_MENSAJE = "" # Mensaje a enviar
DELAY_MENSAJE = 2 # Tiempo a esperar entre cada mensaje enviado

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3");

def clearc():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():

    clearc()
    print(cyan + "\n\n~ Bot Idealista cargado ~")
    print(cyan + " Creado por Tikene\n")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(LINK_IDEALISTA)
    print("\n")

    while True:

        iframeog = driver.find_element_by_xpath("/html/body/iframe")
        driver.switch_to.frame(iframeog)

        while True:
            try:
                lol = driver.find_element_by_id("captcha-container")
            except Exception as e:
                break
            print("Completa el captcha para continuar")
            sleep(4)




        driver.switch_to.default_content()

        try:
            aceptarCookies = driver.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]')
            aceptarCookies.click()
            print("Cookies aceptadas")
        except:
            pass

        listaAnuncios = driver.find_elements_by_class_name("roomie")
        print(magenta + "\n[Numero anuncios: " + white + str(len(listaAnuncios)) + magenta + "]\n")


        if not os.path.exists("users_mensajeados"):
            listaMensajeados = []
        else:
            with open("users_mensajeados", "rb") as f:
                listaMensajeados = pickle.load(f)

        botonNext = driver.find_element_by_class_name("next").find_elements_by_xpath(".//*")[0]

        for anuncio in listaAnuncios:
            IDAnuncio = int(anuncio.get_attribute("id"))
            anuncioRoot = anuncio.find_element_by_class_name("roomie-name.open")
            nombreAnuncio = anuncioRoot.find_elements_by_xpath(".//*")[1]

            if IDAnuncio in listaMensajeados:
                print(red + "Ya mensajeado " + nombreAnuncio.text)
                continue

            datosExtra = anuncio.find_element_by_class_name("roomie-data").text.split(" años ")
            edadAnuncio = datosExtra[0]
            horaAnuncio = datosExtra[1]

            print(yellow + "\nNombre: " + nombreAnuncio.text)
            print(yellow + "Edad: " + edadAnuncio)
            print(yellow + "Hora: " + horaAnuncio)

            nombreAnuncio.click()

            campoUsuario = anuncio.find_element_by_name("username")
            campoEdad = anuncio.find_element_by_name("age")
            campoGenero = anuncio.find_elements_by_class_name("input-radio")[0]
            campoEmail = anuncio.find_element_by_name("userEmail")
            campoTexto = anuncio.find_element_by_name("message")
            botonEnviar = anuncio.find_element_by_name("b-preview")

            for letter in FILL_NOMBRE:
                campoUsuario.send_keys(letter)
                sleep(uniform(0.01, 0.03))

            for letter in FILL_EDAD:
                campoEdad.send_keys(letter)
                sleep(uniform(0.01, 0.03))

            for letter in FILL_EMAIL:
                campoEmail.send_keys(letter)
                sleep(uniform(0.01, 0.03))

            for letter in FILL_MENSAJE:
                campoTexto.send_keys(letter)
                sleep(uniform(0.001, 0.01))

            campoGenero.click()
            botonEnviar.click()
            print(green + "Enviado mensaje a " + blue + nombreAnuncio.text)

            listaMensajeados.append(IDAnuncio)
            with open("users_mensajeados", "wb") as f:
                pickle.dump(listaMensajeados, f)

            sleep(DELAY_MENSAJE)

        botonNext.click()
        print(green + "\nClickeada siguiente pagina")

main()
