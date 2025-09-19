from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.data import urban_routes_url, phone_number, card_number, message_for_driver
from utils.retrive_code import retrieve_phone_code

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    requests_taxi_button = (By.CSS_SELECTOR, 'button.round')
    comfort_icon = (By.XPATH, '//div[@class="tcard-title" and text()= "Comfort"]') # button Comfort
    phone_button = (By.CLASS_NAME, "np-text") # click phone
    phone_number = (By.ID, "phone") # text number
    next_phone = (By.XPATH, "//button[text() = 'Siguiente' and @type='submit']")  # button exit
    sms_code = (By.XPATH, '//*[@id="code"]')  # 3478 code send_key()
    code_accept_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    credit_card_button = (By.XPATH, "//div[text() = 'Método de pago' and @class = 'pp-text']") # Clic para habilitar la información de la TC
    add_new_card = (By.XPATH, "//img[@alt = 'plus']") # Signo de + para adicionar la TC
    credit_card_number = (By.CLASS_NAME,"card-input") # Número de la TC
    credit_card_code = (By.NAME, "code") # Código de la TC
    submit_accept_tc = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]') # Botón aceptar TC
    close_credit_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button') # x para cierre de la TC
    input_driver_msg = (By.ID, 'comment') # Mensaje al conductor
    select_blanket = (By.XPATH, "//div[text() = 'Manta y pañuelos']/following-sibling::div/div") # Pedir manta y pañuelo
    counter_ice_cream = (By.XPATH, '//div[@class="counter-plus"]')
    ice_cream_amount = (By.CLASS_NAME, "counter-value")
    order_taxi_button = (By.XPATH, '//*[@class = "smart-button"]') # Boton de pedir taxi click()
    modal_window = (By.CLASS_NAME, 'order-header-title') # text
    modal_window_driver = (By.CLASS_NAME, 'order-body') #wait

    def __init__(self, driver):
        self.phone_input = None
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def set_from(self, from_address):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        self.wait.until(EC.presence_of_element_located(self.from_field)).send_keys(from_address)

    def set_to(self, to_address):
        #self.driver.find_element(*self.to_field).send_keys(to_address)
        self.wait.until(EC.presence_of_element_located(self.to_field)).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_request_taxi_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.requests_taxi_button))

    def click_on_request_button(self):
        self.get_request_taxi_button().click()

        # Button Comfort
    def get_comfort_icon(self):
        return self.wait.until(EC.element_to_be_clickable(self.comfort_icon))

    def click_on_comfort_button(self):
        self.get_comfort_icon().click()

        # Button phone number and text number
    def get_click_phone(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.phone_button)).click()

    def set_phone_number(self, phone_number):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.phone_number)).send_keys(phone_number)

    def click_follow_phone(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.next_phone)).click()

    def set_code_number(self, sms):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.sms_code)).send_keys(sms)

    def get_code_number(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.sms_code)).get_property('value')

    def is_enable_accept_code(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.code_accept_button)).is_enabled()

    def click_code_number(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.code_accept_button)).click()

        # Agregar una tarjeta de crédito
    def click_credit_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.credit_card_button)).click()

    def fill_credit_card(self, card_number, code):
        self.wait.until(EC.presence_of_element_located(self.add_new_card)).click()
        self.wait.until(EC.presence_of_element_located(self.credit_card_number)).send_keys(card_number)
        self.wait.until(EC.presence_of_element_located(self.credit_card_code)).send_keys(code)
        self.wait.until(EC.presence_of_element_located(self.credit_card_number)).click()

    def get_card_number(self):
        return self.driver.find_element(*self.credit_card_number).get_property('value')

    def get_card_code(self):
        return self.driver.find_element(*self.credit_card_code).get_property('value')

    def submit_accept(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_accept_tc)).click()

    def click_close_card(self):
        self.wait.until((EC.element_to_be_clickable(self.close_credit_card))).click()

        # Escribir un mensaje para el controlador
    def click_driver_msg(self):
        self.wait.until((EC.element_to_be_clickable(self.input_driver_msg))).click()

    def get_driver_msg(self):
        return self.driver.find_element(*self.input_driver_msg).get_property('value')

    def set_driver_msg(self):
        self.wait.until(EC.presence_of_element_located(self.input_driver_msg)).send_keys(message_for_driver)

        # Pedir una manta y pañuelos
    def is_enable_select_blanket_button(self):
        return self.wait.until(EC.presence_of_element_located(self.select_blanket)).is_enabled()

        # Pedir una manta y pañuelos
    def click_select_blanket(self):
        self.wait.until(EC.presence_of_element_located(self.select_blanket)).click()

        # Pedir 2 helados
    def click_ice_cream_add(self, quantity_ice):
        for i in range(quantity_ice):
            self.wait.until(EC.presence_of_element_located(self.counter_ice_cream)).click()

        # obtener cantidad de helados (label)
    def get_ice_cream_amount(self):
        return self.wait.until(EC.presence_of_element_located(self.ice_cream_amount)).text

        # Botón azul para pedir taxi luego de ingresada la información
    def get_order_button_taxi(self):
        return self.wait.until(EC.element_to_be_clickable(self.order_taxi_button)).click()

        # Aparece el modal
    def is_displayed_modal(self):
        return self.wait.until(EC.presence_of_element_located(self.modal_window)).is_displayed()

    def get_modal_info(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.modal_window))
        self.wait.until(EC.presence_of_element_located(self.modal_window_driver))


# Getter → busca y devuelve el elemento.
# Setter, clicker, reader → interactúan con él.
