import time
import os
from scraper_base import Scraper, ScraperState
from scraper_utils import log
import regex as re
import asyncio
from selenium.webdriver import ActionChains
import numpy as np
import itertools
import pandas as pd


class ProfileCommentsScraper(Scraper):
    profile_comments_output_path = None
    profile_stats_output_path = None
    name_of_poster_list_stat = []
    username_list_stat = []
    post_count_list_stat = []
    like_count_list_stat = []

    def __init__(self):
        super().__init__()
        self.profile_comments_output_path = f"{os.getenv('profile_comments_output_path')}/{self.date_w_time_today}"
        if not os.path.exists(self.profile_comments_output_path):
            os.mkdir(self.profile_comments_output_path)

        self.profile_stats_output_path = f"{os.getenv('profile_stats_output_path')}/{self.date_w_time_today}"
        if not os.path.exists(self.profile_stats_output_path):
            os.mkdir(self.profile_stats_output_path)

    def _login(self):
        self.driver.get('https://sso.accounts.dowjones.com/login?state=hKFo2SAyaEVBbUlxVVlqV0w5blRIVnFGYWtNSlpCYmwwaXJUd6FupWxvZ2luo3RpZNkgTkV4djhHWVJKZl9KX0ZVNVVSMTJzR0FXZDI3bC1BaE-jY2lk2SA1aHNzRUFkTXkwbUpUSUNuSk52QzlUWEV3M1ZhN2pmTw&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts%20suuid%20createTimestamp&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=8b0c1450-b8a6-4f08-88de-8ee4c1e877e5&ui_locales=en-us-x-wsj-215-2&mars=-1&ns=prod%2Faccounts-wsj#!/signin')
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
                target = self.driver.execute_script("return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelector(\"button[data-spmark='show-more']\")")
                if target.is_displayed():
                    target.click()
                    time.sleep(5)
            except Exception as e:
                log(f"Show more button not found on attempt {click_num + 1 }/{max_show_more_clicks} with error: {e}")
                if re.search('page crash', str(e), re.IGNORECASE) or re.search('invalid session id', str(e), re.IGNORECASE):
                    raise
                time.sleep(5)
                return

    def _process_page(self):
        if self.section_sublink_index >= len(self.current_section_sublinks):
            self.header_links_index += 1
            self.state = ScraperState.get_section_sublinks
            if self.header_links_index >= len(self.header_links):
                self.state = ScraperState.done
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

        #########################GETTING EVERY USERNAME DATA########################################
        # unique_names = []
        # names_raw = driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\\\"@spotim/ui-components conversation conversation-survey @spotim/ui-components @spotim/ads @spotim/user-image feed @spotim/entities @spotim/content-entities @spotim/user-info @spotim/rich-editor @spotim/toast-provider @spotim/svg-provider @spotim/notifications-bell notifications @spotim/message live-blog feed-v4 discover user-profile standalone-ui-kit discover @spotim/common-components\"]\')[0].shadowRoot.querySelectorAll(\"[class=\'Button__contentWrapper--11-2-8\'\")")[6:50000]
        names_raw = self.driver.execute_script("return document.querySelectorAll('[data-labels-section]')[0].shadowRoot.querySelectorAll(\"[class=\'Typography__text--11-2-8 Typography__t4--11-2-8 Typography__l6--11-2-8 src-components-Username-index__wrapper src-components-Username-index__truncated src-components-Username-index__button\'\")")
        names_raw = list(set(names_raw))
        pat_1 = r'(\d{0,}\.\d{0,}K|\d{0,}\d{0,}K)'
        pat_2 = r'\d{0,}'

        for names in names_raw:
            time.sleep(10)
            log("scraping individual")
            ActionChains(self.driver).move_to_element(names).click().perform()
            time.sleep(5)
            # if the name is not already in the name of poster list else quit loop and go back to beggining
            try:
                name = self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"src-components-TopMenu-TopMenu__username--lcVW5\"]\')[0].textContent")
            except Exception as e:
                log(f'error getting commenter name: {e}')
                continue

            if name in self.name_of_poster_list_stat:
                log("name already in the og list skipping name")
                self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"closeButton--\"\')[0].click()")
                continue

            name_of_poster = self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"src-components-TopMenu-TopMenu__username--lcVW5\"]\')[0].textContent")
            user_name_of_poster = self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"Typography__text--11-2-13 Typography__t5--11-2-13 Typography__l5--11-2-13 src-components-UserDetails-UserDetails__usernameWrapper--24Mlg\"]\')[0].textContent")
            log(f'new name added to list {name_of_poster} scraping profile')
            post_count = self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"src-components-Navbar-Navbar__Label--2os_g\"]\')[0].textContent")
            log(post_count)
            try:
                like_count = self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"src-components-DetailText-DetailText__DetailText--mSHwD src-components-DetailText-DetailText__DetailText_Grey--2-p-_ src-components-DetailText-DetailText__nowrap--Hwniw\"\')[0].textContent")
            except Exception as e:
                log(f'Error with like count, likely private profile un: {user_name_of_poster}, n: {name_of_poster} and error: {e}')
                continue

            individual_comment_list = []
            replied_to_list = []
            article_posted_to_list = []
            article_links_list = []
            like_count = like_count.replace('Likes received', '')
            if bool(re.search(pat_1, like_count)):
                like_refiged = int(np.ceil(float(like_count.replace('K', '')) * 1000))
                log(like_refiged)
            elif bool(re.search(pat_2, like_count)):
                like_refiged = int(np.ceil(float(like_count)))
            ####appending like count and name of posted #####################
            self.like_count_list_stat.append(like_refiged)
            self.name_of_poster_list_stat.append(name_of_poster)
            self.username_list_stat.append(user_name_of_poster)

            # Posts (4K)
            ####cleaning posts into a numeric interger#####
            post_count = post_count.replace('Posts', '').replace('(', '').replace(')', '')
            if bool(re.search(pat_1, post_count)):
                post_refiged = int(np.ceil(float(post_count.replace('K', '')) * 1000))
                log(post_refiged)
            elif bool(re.search(pat_2, post_count)):
                post_refiged = int(np.ceil(float(post_count)))
                log(post_refiged)
            ##appending to post count list
            self.post_count_list_stat.append(post_refiged)

            ######scrolling to bottum of page based on post range##############
            scroll_counter = 0
            # scroll_height = self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Modal__container--\"\')[0].scrollHeight")
            for i in range(0, post_refiged // 6):
                scroll_counter += 1
                self.driver.execute_script(
                    "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Modal__focusLockWrapper--\"\')[0].scrollIntoView(false)")
                spinner = self.driver.execute_script(
                    "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Spinner__spinner--\"\')[0]")
                try:
                    if spinner.is_displayed() == True:
                        time.sleep(.5)
                        self.driver.execute_script(
                            "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Modal__focusLockWrapper--\"\')[0].scrollIntoView(true)")
                        log("Scrolling done clicker readmores 1")
                        log(
                            f"counter at {round(scroll_counter / (post_refiged // 6) * 100, 2)} % of scrolls complete or {scroll_counter} out of ")

                        read_more_buttons = self.driver.execute_script(
                            "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ShowMoreButton--\"]\')")
                        for button in read_more_buttons:
                            button.click()
                            log("clickin read mores 1")

                        log("read more 1's done readmores 2")
                        read_more_buttons_2 = self.driver.execute_script(
                            "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ShowMore--\"]\')")
                        for button in read_more_buttons_2:
                            button.click()
                            log("clickin read mores 2")

                        # time.sleep(.4)
                        # driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class=\"Modal__focusLockWrapper--11-2-9\"\')[0].window.scrollBy(0,-250)")
                    else:
                        time.sleep(.5)
                        log(
                            f"counter at {round(scroll_counter / (post_count // 6) * 100, 2)} % of scrolls complete")

                        read_more_buttons = self.driver.execute_script(
                            "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ShowMoreButton--\"]\')")
                        for button in read_more_buttons:
                            button.click()
                            log("clickin read mores 1 _no loading needed")

                        log("read more 1's done readmores 2")
                        read_more_buttons_2 = self.driver.execute_script(
                            "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ShowMore--\"]\')")
                        for button in read_more_buttons_2:
                            button.click()
                            log("clickin read mores 2 no loading needed")
                except:
                    continue
            time.sleep(2)

            ####################clicking read more buttons for an individuals post################################
            try:
                log("Getting meta replies data for individual")
                replied_to_web = self.driver.execute_script(
                    "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__Metadata--\"\')")
                for replies in replied_to_web:
                    replied_to_list.append(replies.get_property('textContent'))
                    # log(replied_to_list)

                log("Getting meta comments data for individual")
                individual_comment_web = self.driver.execute_script(
                    "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__TextWrapper--\"\')")
                for comment in individual_comment_web:
                    individual_comment_list.append(comment.get_property('textContent'))
                    # log(individual_comment_list)

                log("Getting the article user replied or posted for individual")
                replied_to_article_web = self.driver.execute_script(
                    "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Typography__bold--\"\')")
                for article in replied_to_article_web:
                    article_posted_to_list.append(article.get_property('textContent'))

                link_of_articles = self.driver.execute_script(
                    "return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"src-components-FeedItem-styles__ExtractWrapper--\"\')")
                for link_of_article in link_of_articles:
                    article_links_list.append(link_of_article.get_attribute("href"))
            except:
                continue
                # log(article_posted_to_list)
            #######wrap in dataframe for individual##################
            zipped_indi = list(itertools.zip_longest(replied_to_list, individual_comment_list, article_posted_to_list, article_links_list))
            log("lists have been zipped")
            indi_df = pd.DataFrame(zipped_indi, columns=['Replied_To', 'Comment', 'Article_Name', 'link'])
            indi_df['Post_or_Reply'] = np.where(indi_df['Replied_To'].str.findall('Replied to'), "Reply", "Post")
            date_patern_regex_all = r'\d{0,}(s|w|y|d|m|h)'
            indi_df['Replied_To_Name'] = indi_df['Replied_To'].str.replace(r'Replied to', '').str.replace(r'Posted','').str.replace('ago', '').str.replace(date_patern_regex_all, '')
            indi_df['Replied_To_Time'] = indi_df['Replied_To'].apply(lambda x: self.time_converter(x))
            indi_df['Date Scraped'] = self.time_today
            indi_df['Name'] = name_of_poster
            indi_df['Username'] = user_name_of_poster
            indi_df['Origonal Article Scraped From'] = self.current_article_link
            indi_df = self._analyze_comment(indi_df)

            log(indi_df)
            # path = f'{self.}/{self.date_w_time_today}'
            # if not os.path.exists(path):
            #     os.mkdir(path)
            indi_df.to_csv(f'{self.profile_comments_output_path}/{name_of_poster}.csv')

            poster_stats = list(itertools.zip_longest(self.username_list_stat, self.name_of_poster_list_stat, self.like_count_list_stat, self.post_count_list_stat))
            user_stat_df = pd.DataFrame(poster_stats, columns=['Username', 'Name of Poster', 'Like Count', 'Post Count'])
            user_stat_df["Date Scraped"] = self.time_today
            user_stat_df.to_csv(f'{self.profile_stats_output_path}/stats.csv')
            self.article_csv_save_count += 1
            log(f"Successfully saved CSVs! {self.article_csv_save_count} total profiles scraped and now with {len(self.username_list_stat)} stats!")
            self.num_times_article_retry = 0
            log("continuing to next profile")

            ###########clost modal and move on##################
            time.sleep(1)
            # go to top of page
            self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Modal__focusLockWrapper\"\')[0].scrollIntoView(true)")
            # click out of page
            self.driver.execute_script("return document.querySelectorAll(\'[data-spot-im-shadow-host=\"@spotim/ui-components user-profile @spotim/svg-provider\"]\')[0].shadowRoot.querySelectorAll(\'[class*=\"Button__circle-icon--\"\')[0].click()")


# exclude_users = [user1, user2]
# oldest_comment_date for existing users
profile_comments_scraper = ProfileCommentsScraper()
profile_comments_scraper.run()
log("FINISHED!!!")
