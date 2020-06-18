import unittest
from trello_api import trello_api
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime
import sys
import HtmlTestRunner
import xmlrunner

class trello_api_test(unittest.TestCase):
    key = ''
    token = ''
    trello_api(key, token)
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    board_id = ''
    short_url = ''
    now = datetime.now()
    board = 'teste-{}'.format(now.strftime('%m-%d-%Y-%H-%M-%S'))
    user = ''
    password = ''

    @classmethod
    def setUpClass(self):

        user = ''
        password = ''
        url = 'https://trello.com/login'
        self.driver.get(url)
        self.driver.find_element_by_name('user').send_keys(self.user)
        sleep(2)
        login_by_pass = self.driver.find_element_by_name('password')
        login_by_atlassian = self.driver.find_element_by_class_name('atlassian-brand')
        if login_by_pass.is_displayed():
            login_by_pass.send_keys(self.password)
            self.driver.find_element_by_id('login').click()
        elif login_by_atlassian.is_displayed():
            login_by_atlassian.click()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'password')))
            self.driver.find_element_by_id('password').send_keys(self.password)
            self.driver.find_element_by_id('login-submit').click()
        WebDriverWait(self.driver, 30).until(EC.title_contains('Quadros'))
        self.board_id, self.short_url = trello_api.create_board(self, self.board)
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), {})]'.format(self.board))))
        self.driver.find_element_by_tag_name('body').screenshot('create_board.png')

    def test_001_create_backlog_column(self):
        id_backlog, response = trello_api.create_column(self, self.board_id, 'BackLog')
        self.assertEqual(response, 200)
        name = trello_api.get_column_name(self, id_backlog)
        self.assertEqual(name, 'BackLog')
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_001_create_backlog_column.png')

    def test_002_create_todo_column(self):
        id_todo, response = trello_api.create_column(self, self.board_id, 'ToDo')
        self.assertEqual(response, 200)
        name = trello_api.get_column_name(self, id_todo)
        self.assertEqual(name, 'ToDo')
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_002_create_todo_column.png')

    def test_003_create_inprogress_column(self):
        id_inprogress, response = trello_api.create_column(self, self.board_id, 'in Progress')
        self.assertEqual(response, 200)
        name = trello_api.get_column_name(self, id_inprogress)
        self.assertEqual(name, 'in Progress')
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_003_create_inprogress_column.png')

    def test_004_create_testing_column(self):
        id_testing, response = trello_api.create_column(self, self.board_id, 'Testing')
        self.assertEqual(response, 200)
        name = trello_api.get_column_name(self, id_testing)
        self.assertEqual(name, 'Testing')
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_004_create_testing_column.png')

    def test_005_create_done_column(self):
        id_done, response = trello_api.create_column(self, self.board_id, 'Done')
        self.assertEqual(response, 200)
        name = trello_api.get_column_name(self, id_done)
        self.assertEqual(name, 'Done')
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_005_create_done_column.png')

    def test_006_create_card(self):
        column_id = trello_api.get_card_column(self, self.board_id, 'BackLog')
        trello_api.move_column_top(self, column_id)
        self.id_card, response = trello_api.create_card(self, column_id, 'teste')
        self.assertEqual(response, 200)
        name, column = trello_api.get_card_data(self, self.id_card)
        self.assertEqual(name, 'teste')
        self.assertEqual(column, column_id)
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_006_create_card.png')

    def test_007_edit_card_name(self):
        card_id = trello_api.get_card_id(self, self.board_id, 'teste', 'BackLog')
        response = trello_api.update_card(self, card_id, name = 'Teste Deal')
        self.assertEqual(response, 200)
        name, _ = trello_api.get_card_data(self, card_id)
        self.assertEqual(name, 'Teste Deal')
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_007_edit_card_name.png')

    def test_008_move_card_todo(self):
        column_id = trello_api.get_card_column(self, self.board_id, 'ToDo')
        card_id = trello_api.get_card_id(self, self.board_id, 'Teste Deal', 'BackLog')
        response = trello_api.update_card(self, card_id, idList= column_id)
        self.assertEqual(response, 200)
        _, column = trello_api.get_card_data(self, card_id)
        self.assertEqual(column, column_id)
        trello_api.move_column_top(self, column_id)
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_008_move_card_todo.png')

    def test_009_move_card_inprogress(self):
        column_id = trello_api.get_card_column(self, self.board_id, 'in Progress')
        card_id = trello_api.get_card_id(self, self.board_id, 'Teste Deal', 'ToDo')
        response = trello_api.update_card(self, card_id, idList= column_id)
        self.assertEqual(response, 200)
        _, column = trello_api.get_card_data(self, card_id)
        self.assertEqual(column, column_id)
        trello_api.move_column_top(self, column_id)
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_009_move_card_inprogress.png')

    def test_010_move_card_testing(self):
        column_id = trello_api.get_card_column(self, self.board_id, 'Testing')
        card_id = trello_api.get_card_id(self, self.board_id, 'Teste Deal', 'in Progress')
        response = trello_api.update_card(self, card_id, idList= column_id)
        self.assertEqual(response, 200)
        _, column = trello_api.get_card_data(self, card_id)
        self.assertEqual(column, column_id)
        trello_api.move_column_top(self, column_id)
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_010_move_card_testing.png')

    def test_011_move_card_done(self):
        column_id = trello_api.get_card_column(self, self.board_id, 'Done')
        card_id = trello_api.get_card_id(self, self.board_id, 'Teste Deal', 'Testing')
        response = trello_api.update_card(self, card_id, idList= column_id)
        self.assertEqual(response, 200)
        _, column = trello_api.get_card_data(self, card_id)
        self.assertEqual(column, column_id)
        trello_api.move_column_top(self, column_id)
        self.driver.get(self.short_url)
        self.driver.find_element_by_tag_name('body').screenshot('test_011_move_card_done.png')

    def test_012_exclude_board(self):
        response = trello_api.delete_board(self,self.board_id)
        self.assertEqual(response, 200)
        self.assertEqual(trello_api.get_board(self, self.board_id), 404)
        self.driver.find_element_by_tag_name('body').screenshot('test_012_exclude_board.png')

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

if __name__ == "__main__":
    html_report_dir = './html_report'
    xml_report_dir = './reports/xml_report'
    trello_api_test.password = sys.argv.pop()
    trello_api_test.user = sys.argv.pop()
    trello_api_test.token = sys.argv.pop()
    trello_api_test.key = sys.argv.pop()
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=html_report_dir))

