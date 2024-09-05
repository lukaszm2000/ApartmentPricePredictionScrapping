import time
from selenium import webdriver
import os
import otodom.constants as const
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

class Otodom(webdriver.Chrome):
    def __init__(self, driver_path=r'C:\Program Files (x86)\chromdriver.exe',teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Otodom, self).__init__()
        self.implicitly_wait(1)
        self.maximize_window()

    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        time.sleep(3)

    def accept_cookies(self):
        cookies = self.find_element(by=By.CSS_SELECTOR,value="#onetrust-accept-btn-handler")
        cookies.click()
        time.sleep(1)

    def choose_city(self,city='Warszawa'):
        city_field = self.find_element(by=By.CSS_SELECTOR,value=".css-8xh6ab")
        self.execute_script("arguments[0].removeAttribute('readonly')", city_field)
        city_field.click()
        city_field.clear()
        city_field.send_keys(city)

        time.sleep(1)
        
        first_suggestion = self.find_element(By.CSS_SELECTOR, ".e12tw922.css-1q6iflv")
        first_suggestion.click()

        time.sleep(2)

    def choose_max_min_price(self,price_min = 300_000, price_max = 2_500_000):
        price_min_field = self.find_element(By.CSS_SELECTOR, 'input#priceMin')
        price_min_field.click()
        price_min_field.clear()
        price_min_field.send_keys(str(price_min))

        time.sleep(1)

        price_max_field = self.find_element(By.CSS_SELECTOR, 'input#priceMax')
        price_max_field.click()
        price_max_field.clear()
        price_max_field.send_keys(str(price_max))

        time.sleep(1)

    def show_results(self):
        show_results_field = self.find_element(by=By.CSS_SELECTOR,value="#search-form-submit")
        time.sleep(3)
        show_results_field.click()
        time.sleep(3)

    def _get_offer_links(self):
        all_offer_class = self.find_element(by=By.CSS_SELECTOR,value='div[data-cy="search.listing.organic"]')
        articles = all_offer_class.find_elements(by=By.CSS_SELECTOR,value='.css-136g1q2.eeungyz0')
        a_elements = [article.find_element(By.CSS_SELECTOR, 'a[href]') for article in articles]
        links = [a_element.get_attribute('href') for a_element in a_elements]
        return links

    def _save_link_to_file(self, links):
        file_path = os.path.join(os.getcwd(), 'offer_links.csv') 
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=['links'])

        new_links_df = pd.DataFrame(links, columns=['links'])
        df = pd.concat([df, new_links_df], ignore_index=True)
        df.to_csv(file_path, index=False)
        
    def _scroll_to_page_button(self,offset=-100):
        pagination_element = self.find_element(By.CSS_SELECTOR, 'ul[data-cy="frontend.search.base-pagination.nexus-pagination"]')
        self.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top + window.scrollY + arguments[1]);", pagination_element, offset)
        time.sleep(2)
    
    def get_and_save_all_links(self):
        while True:
            try:
                links = self._get_offer_links()  
                self._save_link_to_file(links)

                change_page_buttons = self.find_elements(By.CSS_SELECTOR, 'li.css-4oud49')
                next_page_button = change_page_buttons[-1]
                if next_page_button.get_attribute("aria-disabled") == "true":
                    print("No more pages.")
                    break

                self._scroll_to_page_button(next_page_button)
                time.sleep(1.5)
                next_page_button.click()
                time.sleep(3)

            except NoSuchElementException:
                print("Next button not found.")
                break

    def visit_all_links_and_save_parameters(self):
        file_path_links = os.path.join(os.getcwd(), 'offer_links.csv')
        if not os.path.exists(file_path_links):
            print('No such file!')
            return
        
        df_links = pd.read_csv(file_path_links)


        file_path_offers_details = os.path.join(os.getcwd(), 'offers_details_2.csv') 
        if os.path.exists(file_path_offers_details):
            df_offer_details = pd.read_csv(file_path_offers_details)
        else:
            df_offer_details = pd.DataFrame(columns=const.OFFER_DETAILS_NAME + const.OFFER_ADDITIONAL_DETAILS_NAME + ['Link'])


        for index , row in df_links.iterrows():
            link = row['links']
            self.execute_script("window.open('');")
            self.switch_to.window(self.window_handles[-1])
            

            self.get(link)  

            if index == 0:
                self.accept_cookies()

            address = self.find_elements(by=By.CSS_SELECTOR, value="a[aria-label='Adres']")
            if not address:
                self.close()
                self.switch_to.window(self.window_handles[0])
                continue
        

            expired_alert = self.find_elements(By.CSS_SELECTOR, 'div[data-cy="expired-ad-alert"]')

            if expired_alert:
                print(f"Link {link} jest nieaktualny, pomijam.")
                self.close()
                self.switch_to.window(self.window_handles[0])
                continue

            details = self._get_all_offer_details()
            details['Link'] = link
            
            self.close()
            self.switch_to.window(self.window_handles[0])
            
            new_df_offer_details = pd.DataFrame([details], columns=df_offer_details.columns.to_list())
            df_offer_details = pd.concat([df_offer_details, new_df_offer_details], ignore_index=True)
            
            df_offer_details.to_csv(file_path_offers_details, index=False)


    def _get_all_offer_details(self):

        offer_details_dict = self._get_offer_details()

        offer_details_dict = self._get_offer_additional_details(offer_details_dict)
        
        return offer_details_dict
    
    def _get_offer_details(self):

        details_dict = {}

        address = self.find_element(by=By.CSS_SELECTOR, value=".css-70qvj9 a").text
        price = self.find_element(by=By.CSS_SELECTOR, value='strong[data-cy="adPageHeaderPrice"]').text

        details_dict.update({'Adres': address, 'Cena': price})

        offer_details_elements = self.find_elements(by=By.CSS_SELECTOR, value='.css-1ivc1bc.ewb0mtf1')

        offer_details_classes_values = [offer_details_element.find_elements(by=By.CSS_SELECTOR,value='.css-1qzszy5.ewb0mtf2')[-1] for offer_details_element in offer_details_elements]
        offer_details_classes_names = [offer_details_element.find_elements(by=By.CSS_SELECTOR,value='.css-1qzszy5.ewb0mtf2')[0] for offer_details_element in offer_details_elements]

        offer_details_values = [offer_details_class_value.text for offer_details_class_value in offer_details_classes_values]
        offer_details_names = [offer_details_class_name.text for offer_details_class_name in offer_details_classes_names]


        details_dict['Certyfikat energetyczny'] = None

        for idx, _ in enumerate(offer_details_names):
            if offer_details_names[idx] != 'Obsługa zdalna':
                details_dict[offer_details_names[idx]] = offer_details_values[idx] if offer_details_values[idx] not in const.UNKNOWN_OFFER_DETAIL else None
        
        return details_dict
        
    def _get_offer_additional_details(self,details_dict):

        offer_additional_details_elements = self.find_elements(by=By.CSS_SELECTOR, value='.css-tpkder.ewb0mtf1')

        offer_additional_details_classes_values = [offer_additional_details_element.find_elements(by=By.CSS_SELECTOR,value='.css-1qzszy5.ewb0mtf2, .css-1sqc82x.ewb0mtf2')[-1] for offer_additional_details_element in offer_additional_details_elements]
        offer_additional_details_classes_names = [offer_additional_details_element.find_elements(by=By.CSS_SELECTOR,value='.css-1qzszy5.ewb0mtf2, .css-1sqc82x.ewb0mtf2')[0] for offer_additional_details_element in offer_additional_details_elements]
        

        offer_additional_details_values = [offer_additional_details_class_value.text for offer_additional_details_class_value in offer_additional_details_classes_values]
        offer_additional_details_names = [offer_additional_details_class_name.text for offer_additional_details_class_name in offer_additional_details_classes_names]

        for idx, _ in enumerate(offer_additional_details_names):
            details_dict[offer_additional_details_names[idx]] = offer_additional_details_values[idx] if offer_additional_details_values[idx] not in const.UNKNOWN_OFFER_DETAIL else None

        return details_dict
