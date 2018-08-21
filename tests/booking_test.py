import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, Chrome


class ChromeTest(unittest.TestCase):

    def setUp(self):
        opts = ChromeOptions()
        opts.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=opts)

    def quantity_children(self):
        quantity_age_children = self.driver.find_elements_by_xpath(
            "//select[@name='age']"
        )
        return len(quantity_age_children)

    def get_input_field_from_date(self, f_day, f_month, f_year):
        day = self.driver.find_element_by_name(f_day)
        # driver.findElement(someLocator).clear();
        month = self.driver.find_element_by_name(f_month)
        year = self.driver.find_element_by_name(f_year)
        return (day, month, year)

    def get_input_values_from_date(self, f_day, f_month, f_year):
        day = self.driver.find_element_by_name(f_day).get_attribute("value")
        month = self.driver.find_element_by_name(
            f_month).get_attribute("value")
        year = self.driver.find_element_by_name(f_year).get_attribute("value")
        return (day, month, year)

    def send_date_keys_to_page(self, date, day=None, month=None, year=None):
        input_day, input_month, input_year = date
        # time.sleep(1)
        if day is not None:
            input_day.send_keys(day)
        # time.sleep(1)
        if month is not None:
            input_month.send_keys(month)
        if year is not None:
            # time.sleep(1)
            input_year.send_keys(year)
        keys = day, month, year
        return keys

    def test_children_qunatity(self):
        """
        Scenario 1. User is able to specify age of each child
            1. go to home page
            2. open menu for selecting strangers number
            3. specify N number of children (N > 1)
        Expect: the number of age inputs is equal to
        """

        driver = self.driver
        driver.get("http://www.booking.com")
        wait = WebDriverWait(driver, 10)
        elem = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='bicon bicon-aclose header-signin-prompt__close']")
            ))

        driver.find_element_by_xpath("//div[data-command='noop']")

        driver.find_element_by_id('xp__guests__toggle').click()
        elem_group_children = Select(
            driver.find_element_by_id('group_children'))
        wait = WebDriverWait(driver, 10)
        elem = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//select[@id='group_children']")
            ))

        elem_group_children.select_by_value("2")
        self.assertEqual(2, self.quantity_children())

        elem_group_children.select_by_value("5")
        self.assertEqual(5, self.quantity_children())

    def test_form_submit_data(self):
        """
        Scenario 2. User is provided with the same search form at search results page
            1. Go to main page
            2. fill search form with any data
            3. submit the form
        Expect: the same values provided inside the form at the left
        """
        driver = self.driver
        driver.get("http://www.booking.com")
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='bicon bicon-aclose header-signin-prompt__close']")
            ))

        city_input = driver.find_element_by_id('ss').send_keys("Kiev")
        # city_input.send_keys("Kiev, Ukraine")
        driver.find_element_by_id('xp__guests__toggle').click()
        elem_group_children = Select(
            driver.find_element_by_id('group_children'))
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//select[@id='group_children']")
            ))
        elem_group_children.select_by_value("2")
        select_age_children = Select(
            driver.find_element_by_xpath("//select[@data-group-child-age='0']")
        )
        select_age_children.select_by_value("12")
        select_age_children = Select(
            driver.find_element_by_xpath("//select[@data-group-child-age='1']")
        )
        select_age_children.select_by_value("6")
        time.sleep(2)

        # driver.execute_script("document.querySelectorAll('label.boxed')[1].click()")

        driver.find_element_by_xpath(
            "//div[@class='xp__dates-inner xp__dates__checkin']").click()
        driver.find_element_by_xpath(
            "//td[@class='c2-day c2-day-s-today']").click()
        driver.find_element_by_xpath(
            "//div[@class='xp__dates-inner xp__dates__checkout']").click()
        # driver.find_element_by_xpath("//td[@data-id='1535587200000']").click()

        # date_fileds_start = self.get_input_field_from_date('checkin_monthday', 'checkin_month', 'checkin_year')
        # date_fileds_end = self.get_input_field_from_date('checkout_monthday', 'checkout_month', 'checkout_year')
        # browser.execute_script("document.getElementById('XYZ').value+='1'")
        # s_date_submit = self.send_date_keys_to_page(date_fileds_start, '25','8', '2018')
        # e_date_submit = self.send_date_keys_to_page(date_fileds_end, '28')
        submit = driver.find_element_by_xpath("//div[@class='xp__button']")
        submit.click()

        time.sleep(5)
        city_submit = driver.find_element_by_name('ss').get_attribute("value")
        self.assertEqual(city_input, city_submit)

        # s_date_value_from_form = self.get_input_values_from_date('checkin_monthday', 'checkin_month', 'checkin_year')
        # self.assertEqual(s_date_submit, s_date_value_from_form)
        # e_date_value_from_form = self.get_input_values_from_date('checkout_monthday', 'checkout_month', 'checkout_year')
        # self.assertEqual(e_date_submit, e_date_value_from_form)

    def test_check_stars_score_of_hotels(self):
        """
        Scenario 3. Resulting search entries are taken based on filter
            Preconditions:
            User is at search result page
            Steps:
                1. select an option of "Star rating" section
                    Expect: each hotel has chosen number of stars
                2. Reset filter
                3. Select "Review score" option
            Expect: each hotel has score corresponding to chosen
        """
        driver = self.driver
        driver.get("http://www.booking.com")
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='bicon bicon-aclose header-signin-prompt__close']")
            ))
        city_input = driver.find_element_by_id('ss').send_keys("Kiev")
        submit = driver.find_element_by_xpath("//div[@class='xp__button']")
        submit.click()
        wait = WebDriverWait(driver, 15)
        stars_of_hotel_checkbox = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH, "//a[@data-id='class-3']"
                )
            )
        )
        stars_of_hotel_checkbox.click()

        time.sleep(4)
        # driver.find_element_by_xpath("//div[@data-class='3']")
        # hotels_stars = driver.find_elements_by_xpath(
        #     "//div[@data-class='3']"
        #     )
        hotels_stars = driver.find_elements_by_xpath(
            "//*[@class='sr_item sr_item_new sr_item_default sr_property_block  sr_flex_layout    sr_item_no_dates             ']"
        )

        for i in hotels_stars:
            self.assertEqual(int(i.get_attribute('data-class')), 3)
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[@data-id='class-3']").click()
        # driver.find_element_by_xpath("//a[@data-id='class-3']").click()
        wait = WebDriverWait(driver, 15)
        review_score = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH, "//a[@data-id='review_score-80']"
                )
            )
        )
        review_score.click()
        time.sleep(3)
        rewiew_score_of_hotels = driver.find_elements_by_xpath(
            "//*[@class='sr_item sr_item_new sr_item_default sr_property_block  sr_flex_layout    sr_item_no_dates             ']"
        )
        for i in rewiew_score_of_hotels:
            self.assertGreaterEqual(float(i.get_attribute('data-score')), 8)

    def test_specify_booking_date_to_see_price(self):
        """
            Scenario 4. User is required to specify booking date to see booking price
            1. choose any city from the menu below
            Expect:
            - page with listed hotels is opened
            - calendar for specifying check in date is opened
            - no result entry containing booking price or booking status
            2. Click "show prices" button for any hotel
            Expect: calendar for specifying check in date is opened
            3. Set any dates for check in and out
            4. Submit search form
            Expect: each result entry booking price or banner saying no free places
        """

        driver = self.driver
        driver.get("http://www.booking.com")
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='bicon bicon-aclose header-signin-prompt__close']")
            ))
        driver.find_element_by_id('ss').send_keys("Kiev Ukraine")
        submit = driver.find_element_by_xpath("//div[@class='xp__button']")
        submit.click()
        time.sleep(4)

        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 "div.sb-searchbox__outer.sb-searchbox-universal")
            ))
        

        close_calendar = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[@class='c2-calendar-close-button c2-calendar-close-button-clearappearance']")
            ))
        close_calendar.click()

        hotel_list = driver.find_element_by_xpath("//div[@data-block-id='hotel_list']")
        self.assertIsNotNone(hotel_list)
        show_price_button = driver.find_element_by_xpath("//button[@class='sr-cta-button-row sr-cta-button-bottom-spacing sr-cta-button-top-spacing']")
        show_price_button.click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "//td[@class='c2-day c2-day-s-today']").click()
        time.sleep(3)
        show_price_button.click()
        price = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='js_rackrate_animation_anchor smart_price_style gray-icon b_bigger_tag animated']")
            ))
        self.assertIsNotNone(price)

    def tearDown(self):
        self.driver.close()

class FirefoxTest(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
