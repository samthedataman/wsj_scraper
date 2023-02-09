#!/usr/bin/env python3.9
import random
import time
import os
from scraper_utils import log
from scraper_base import Scraper, ScraperState
import regex as re
import asyncio


class ArticleCommentsScraper(Scraper):

    def _login(self):
        self.driver.get(
            'https://sso.accounts.dowjones.com/login?state=hKFo2SAyaEVBbUlxVVlqV0w5blRIVnFGYWtNSlpCYmwwaXJUd6FupWxvZ2luo3RpZNkgTkV4djhHWVJKZl9KX0ZVNVVSMTJzR0FXZDI3bC1BaE-jY2lk2SA1aHNzRUFkTXkwbUpUSUNuSk52QzlUWEV3M1ZhN2pmTw&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts%20suuid%20createTimestamp&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=8b0c1450-b8a6-4f08-88de-8ee4c1e877e5&ui_locales=en-us-x-wsj-215-2&mars=-1&ns=prod%2Faccounts-wsj#!/signin')
        search = self.driver.find_element_by_class_name("username")
        time.sleep(5)
        search.send_keys(os.getenv('WSJ_username'))
        self.driver.find_element_by_xpath('//*[@id="basic-login"]/div[1]/form/div[2]/div[6]/div[1]/button[2]').click()
        time.sleep(5)
        password = self.driver.find_element_by_id("password-login-password")
        password.send_keys(os.getenv('WSJ_password'))
        time.sleep(5)
        button = self.driver.find_element_by_xpath('//*[@id="password-login"]/div/form/div/div[5]/div[1]/button')
        button.click()
        time.sleep(20)
        if self.state == ScraperState.perform_login:
            self.state = ScraperState.get_nav_links
        else:
            # then we are performing a manual login via global error handler here
            self.state = ScraperState.process_page
            if self.num_times_article_retry < self.max_article_retries:
                # then retry the problematic article
                self.section_sublink_index = 0 if self.section_sublink_index <= 0 else self.section_sublink_index - 1
                self.num_times_article_retry += 1


    def _get_nav_links(self):
        raw_links = self.driver.find_elements_by_class_name("style--section-link--2rDVp5ht")
        for header in raw_links:
            self.header_links.append(header.get_attribute("href"))
        self.header_links = list(set(self.header_links))
        for head_link in self.header_links:
            log(head_link)
        self.state = ScraperState.get_section_sublinks

    # returns true if found button and showed conversations successfully
    def _show_conversations(self):
        try:
            clicker = self.driver.find_element_by_xpath('//*[@id="comments_sector"]/button')
            clicker.click()
            log("found clicker in try statement 1")
            return True
        except:
            pass
        try:
            clicker = self.driver.find_element_by_xpath("//button[contains(text(),'conversation_toggle')]")
            clicker.click()
            log("found clicker in try statement 2")
            return True
        except:
            pass
        try:
            clicker = self.driver.execute_script(
                "return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.document.querySelector(\'[class=\"conversation-caret\"\')")
            clicker.click()
            log("found clicker in try statement 3")
            return True
        except:
            pass
        try:
            clicker = self.driver.execute_script("return document.querySelector(\'[class=\"conversation-caret\"\')"),
            clicker.click()
            log("found clicker in try statement 4")
            return True
        except:
            pass
        try:
            clicker = self.driver.find_element_by_id("conversation-container").find_elements_by_tag_name("button")[0]
            clicker.click()
            log("found clicker in try statement 5")
            return True
        except:
            pass
        log("Article appears to have no conversations right now")
        return False

    def _get_nav_page_sub_links(self):
        section_page_link = self.header_links[self.header_links_index]
        self.driver.get(section_page_link)
        elements = self.driver.find_elements_by_xpath("//a[@href]")
        sublinks = []
        for element in elements:
            if str(element.get_attribute('href')).startswith("https://www.wsj.com/articles"):
                sublinks.append(element.get_attribute('href'))
        for link in list(set(sublinks)):
            log(f"{section_page_link} contains the sublink: {link}")
        self.current_section_sublinks = list(set(sublinks))
        self.section_sublink_index = 0
        self.state = ScraperState.process_page

    def _click_show_more_button_a_lot(self):
        max_show_more_clicks = 30
        for click_num in range(0, max_show_more_clicks):
            log(f"clicking show more button {click_num + 1}/{max_show_more_clicks} times")
            try:
                target = self.driver.execute_script(
                    "return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelector(\"button[data-spmark='show-more']\")")
                if target.is_displayed():
                    target.click()
                    time.sleep(5)
            except Exception as e:
                log(f"Show more button not found on attempt {click_num + 1 }/{max_show_more_clicks} with error: {e}")
                if re.search('page crash', str(e), re.IGNORECASE) or re.search('invalid session id', str(e), re.IGNORECASE):
                    raise
                time.sleep(5)
                return

    async def _click_element_after_delay(self, element, delay, element_index, num_elements):
        await asyncio.sleep(delay)
        try:
            element.click()
            log(f"Clicked element {element_index + 1}/{num_elements}")
        except Exception as e:
            error_string = str(e)
            error_formatted = (error_string[:75] + '...') if len(error_string) > 75 else error_string
            log(f"Error clicking element {element_index + 1}/{num_elements}: {error_formatted}")

    async def _expand_replies(self):
        log("Expanding Replies")
        try:
            replies = self.driver.execute_script(
                "return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelectorAll(\"[data-open-web-class='conversation-message-show-replies']\")")
        except Exception as e:
            log(f"reply buttons not found with error: {e}")
            return

        if len(replies) > 0:  # the first reply button click always throws an exception
            num_elements = len(replies)
            delays = sorted([random.uniform(0, num_elements / 10.0) for i in range(num_elements)])
            try:
                tasks = [asyncio.create_task(self._click_element_after_delay(reply, delays[i], i, num_elements)) for i, reply in enumerate(replies)]
                await asyncio.gather(*tasks)
            except Exception as e:
                log(f"Clicking all replies at once failed with error: {e}")
                if re.search('page crash', str(e), re.IGNORECASE) or re.search('invalid session id', str(e), re.IGNORECASE):
                    raise
                return

    async def _expand_see_mores(self):
        log("Clicking see more buttons")
        try:
            see_more_buttons = self.driver.execute_script(
                "return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelectorAll(\"[data-spot-im-class='message-text'] > span\")")
        except Exception as e:
            log(f"see more buttons not found with error: {e}")
            if re.search('page crash', str(e), re.IGNORECASE) or re.search('invalid session id', str(e), re.IGNORECASE):
                raise
            return

        if len(see_more_buttons) > 0:  # the first seem_more_button click always throws an exception
            num_elements = len(see_more_buttons)
            delays = sorted([random.uniform(0, num_elements / 10.0) for i in range(num_elements)])
            try:
                tasks = [asyncio.create_task(self._click_element_after_delay(button, delays[i], i, num_elements)) for i, button in enumerate(see_more_buttons)]
                await asyncio.gather(*tasks)
            except Exception as e:
                log(f"Clicking see more buttons all at once failed with error: {e}")
                if re.search('page crash', str(e), re.IGNORECASE) or re.search('invalid session id', str(e), re.IGNORECASE):
                    raise
                return

    def _process_page(self):
        
        if self.section_sublink_index >= len(self.current_section_sublinks):
            self.header_links_index += 1
            self.state = ScraperState.get_section_sublinks
            if self.header_links_index >= len(self.header_links):
                self.state = ScraperState.create_master_csv
            return

        log(f"scraping sublink {self.section_sublink_index + 1}/{len(self.current_section_sublinks)} of section {self.header_links_index + 1}/{len(self.header_links)}")

        ############################GRAB EACH LINK AND PAGE LOAD PAGE##################
        self.current_article_link = self.current_section_sublinks[self.section_sublink_index]
        self.section_sublink_index += 1
        log(f'going to: {self.current_article_link}')
        self.driver.get(self.current_article_link)
        time.sleep(15)

        ############################SHOWHING CONVERSATION BUTTON CLICK##############################
        log("looking for conversations")
        if not self._show_conversations():
            return

        time.sleep(7)

        #######################SHOWING MORE BUTTON BEING CLICKED######################### (30 button clicks should capture most of the data)
        self._click_show_more_button_a_lot()

        #####################EXPANDING REPLYS############################################
        asyncio.run(self._expand_replies())

        #######################EXPANDING SEE MORE (LONER COMMENTS)###############
        asyncio.run(self._expand_see_mores())

        time.sleep(10)
        #########v######################GETTING METADATA##################################
        ####################MAKING METADATA LISTS################################
        try:
            all_raw_names = self.driver.execute_script(
                "return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelectorAll(\"[class=\'Typography__text--11-2-8 Typography__t4--11-2-8 Typography__l6--11-2-8 src-components-Username-index__wrapper src-components-Username-index__truncated src-components-Username-index__button\'\")")
            time.sleep(2)
            all_raw_texts = self.driver.execute_script(
                "return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelectorAll(\"[data-spot-im-class='message-text']\")")
            time.sleep(2)
            all_raw_dates = self.driver.execute_script(
                "return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelectorAll(\"[data-spot-im-class=\'message-timestamp\'\")")
            time.sleep(2)
            all_raw_data = self.driver.execute_script(
                "return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelectorAll(\"[class=\'components-MessageLayout-index__message-container\'\")")
            ####################TRY PRINTING SAMPLE DATA######################
            log(f"len(names_row): {len(all_raw_names)}")
            log(f"len(texts_raw): {len(all_raw_texts)}")
            log(f"len(date_raw): {len(all_raw_dates)}")
            log(f"len(all_data_raw): {len(all_raw_data)}")
        except Exception as e:
            log(f"aborting csv save {self.current_article_link} due to meta data retrieval error: {e}")
            if re.search('page crash', str(e), re.IGNORECASE) or re.search('invalid session id', str(e), re.IGNORECASE):
                raise
            return

        ####################APPENDING DATA TO LISTS##################################
        log(f"Saving to CSV {self.current_article_link}")
        self._save_article_to_csv(all_raw_data, all_raw_dates, all_raw_names, all_raw_texts)
        #save_csv_thread = threading.Thread(target=self._save_article_to_csv, name=f"Saving CSV: {self.current_article_link}", args=(all_raw_data, all_raw_dates, all_raw_names, all_raw_texts))
        #save_csv_thread.start()
        #self.all_threads.append(save_csv_thread)
        self.article_csv_save_count += 1
        log(f"Successfully saved CSV! {self.article_csv_save_count} total articles saved!")
        self.num_times_article_retry = 0


article_comments_scraper = ArticleCommentsScraper()
article_comments_scraper.run()
log("Finished!!!")
