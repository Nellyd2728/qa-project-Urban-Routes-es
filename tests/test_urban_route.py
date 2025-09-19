import time

from data import data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from data.data import phone_number
from pages import urban_routes_page as urp
import utils.retrive_code as retrive_code

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option("perfLoggingPrefs", {'enableNetwork': True, 'enablePage': True})
        chrome_options.set_capability('goog:loggingPrefs',{'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = urp.UrbanRoutesPage(cls.driver)

        # Configuración de la dirección
    def test_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

        # seleccionar la tarifa comfort
    def test_select_comfort(self):
        self.routes_page.click_on_request_button()
        self.routes_page.click_on_comfort_button()
        assert self.routes_page.get_comfort_icon()

        # Rellenar el número de teléfono
    def test_number_phone(self):
        self.routes_page.get_click_phone()
        self.routes_page.set_phone_number(phone_number)
        self.routes_page.click_follow_phone()
        sms = retrive_code.retrieve_phone_code(self.driver)
        self.routes_page.set_code_number(sms)
        assert self.routes_page.get_code_number() == sms
        assert self.routes_page.is_enable_accept_code() == True
        self.routes_page.click_code_number()

        # Agregar una tarjeta de crédito
    def test_add_credit_card(self):
        self.routes_page.click_credit_button()
        self.routes_page.fill_credit_card(data.card_number, data.card_code)
        assert self.routes_page.get_card_number() == data.card_number
        assert self.routes_page.get_card_code() == data.card_code
        self.routes_page.submit_accept()
        self.routes_page.click_close_card()

        # Escribir un mensaje para el controlador
    def test_msg_driver(self):
        self.routes_page.set_driver_msg()
        assert self.routes_page.get_driver_msg()

        # Pedir una manta y pañuelos
    def test_ask_blanket(self):
        assert self.routes_page.is_enable_select_blanket_button() == True
        self.routes_page.click_select_blanket()

        # Pedir 2 helados
    def test_ask_icecream(self):
        self.routes_page.click_ice_cream_add(2)
        assert self.routes_page.get_ice_cream_amount() == "2"

        # Aparece el modal para buscar el taxi
    def test_order_modal_taxi(self):
        self.routes_page.get_order_button_taxi()
        self.routes_page.get_modal_info()
        assert self.routes_page.is_displayed_modal()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
