from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from class_team import Team
import time
import math
from operator import itemgetter
from collections import Counter
import traceback


class Bot_futball:

    driver = ""
    # Настройки бота
    # Колличество последних матчей за которые ведется статистика >= 5 и <= 10
    statistics_from_count_match = 5
    # Считать колличество побед в последних n матчах
    st_wins_last_mach = True
    # Брать ли в расчет победы в n очных встречах
    st_wins_oponents_last_mach = True
    # Брать ли в расчет коффициент
    st_coefficient = True
    # Смотреть таблицу
    st_place_in_the_table = True
    # Смотреть таблицу уровня игры на данный момент
    st_place_in_the_table_form = True
    # Смотреть ли главные составы
    st_main_cast = True
    # Прощитывать xg и среднее время владения мячом
    st_xg_and_average_ball_possession = True
    # считать процент выигрышей в данной ситуации (дома, в гостях)
    st_game_type_win = True
    # Ссылка на страницу с игрой
    game_url = ""
    # Команда хозяев
    teamHome = ""
    # Команда гостей
    teamAway = ""
    # Аргументировать принятое решение
    argument = ""
    #Status Выполнения бота
    status = ""
    #Вывод бота (результат)
    result_mach = list()

    # Функция создания бота
    def __init__(self, game_url, statistics_from_count_match, st_wins_last_mach, st_wins_oponents_last_mach, st_coefficient, st_place_in_the_table,
                 st_place_in_the_table_form, st_main_cast, st_xg_and_average_ball_possession, st_game_type_win, argument):
        self.game_url = game_url
        self.statistics_from_count_match = statistics_from_count_match
        self.st_wins_last_mach = st_wins_last_mach
        self.st_wins_oponents_last_mach = st_wins_oponents_last_mach
        self.st_coefficient = st_coefficient
        self.st_place_in_the_table = st_place_in_the_table
        self.st_place_in_the_table_form = st_place_in_the_table_form
        self.st_main_cast = st_main_cast
        self.st_xg_and_average_ball_possession = st_xg_and_average_ball_possession
        self.st_game_type_win = st_game_type_win
        self.argument = argument
        self.teamHome = Team("h2h_home", statistics_from_count_match)
        self.teamAway = Team("h2h_away", statistics_from_count_match)

    # Функция получения средних значений владения мячем, среднее количество забитых голов за игру, среднее количество ударов за игру
    def getStatisticsFromNMatch(self, team_type):
        matches_teamHome = self.driver.find_elements_by_css_selector(
            "." + team_type + " tr")
        mainHandle = self.driver.current_window_handle
        average_ball_possession = 0
        shoots = 0
        goals = 0
        count_game_foreach = (self.statistics_from_count_match + 1) if len(
            matches_teamHome) > self.statistics_from_count_match else len(matches_teamHome)
        coast = list()
        for i in range(count_game_foreach):
            matches_teamHome[i].click()
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                if(handle != mainHandle):
                    time.sleep(2)
                    flag_statistica = True
                    try:
                        self.driver.find_element_by_id(
                            "a-match-statistics").click()
                    except:
                        flag_statistica = False

                    team_name = ""

                    if(flag_statistica):
                        text_shots = self.driver.find_elements_by_css_selector(
                            "#tab-statistics-0-statistic .statRow")[2].text
                        text_goals = self.driver.find_element_by_id(
                            "event_detail_current_result").text.split("\n\n")[0].split("-")

                        if(team_type == "h2h_home"):
                            team_name = self.teamHome.getProperties()[0]
                        else:
                            team_name = self.teamAway.getProperties()[0]

                    target_coast_class = ""

                    if(team_name == self.driver.find_element_by_css_selector(".tname-home .participant-imglink").text):
                        target_coast_class = ".fl"
                        if(flag_statistica):
                            average_ball_possession = average_ball_possession + \
                                float(self.driver.find_element_by_css_selector(
                                    ".statText--homeValue").text[0:-1])
                            shoots = shoots + int(text_shots.split("\n")[0])
                            goals = goals + int(text_goals[0])
                    else:
                        target_coast_class = ".fr"
                        if(flag_statistica):
                            average_ball_possession = average_ball_possession + \
                                float(self.driver.find_element_by_css_selector(
                                    ".statText--awayValue").text[0:-1])
                            shoots = shoots + int(text_shots.split("\n")[2])
                            goals = goals + int(text_goals[1])

                    # Беребираем стартовый состав
                    if(self.st_main_cast):
                        flag_main_coast = True
                        try:
                            self.driver.find_element_by_id(
                                "a-match-lineups").click()
                        except:
                            flag_main_coast = False

                        if(flag_main_coast):
                            players = self.driver.find_elements_by_css_selector(
                                ".parts " + target_coast_class + " .name")[0:11:1]
                            for i in range(len(players)):
                                coast.append(players[i].text)

                    self.driver.close()
                    self.driver.switch_to.window(mainHandle)

        goals = goals / self.statistics_from_count_match
        shoots = shoots / self.statistics_from_count_match
        average_ball_possession = math.floor(
            average_ball_possession / self.statistics_from_count_match)

        xg = ""
        try:
            xg = math.floor(shoots / (shoots/goals))
        except:
            xg = 0

        if(team_type == "h2h_home"):
            self.teamHome.setProperties(
                "average_ball_possession", average_ball_possession)
            self.teamHome.setProperties("xg", xg)
            if(self.st_main_cast):
                self.teamHome.main_cast_list = dict(
                    Counter(coast).most_common(11))
        else:
            self.teamAway.setProperties(
                "average_ball_possession", average_ball_possession)
            self.teamAway.setProperties("xg", xg)
            if(self.st_main_cast):
                self.teamAway.main_cast_list = dict(
                    Counter(coast).most_common(11))

    # Получить составы команд
    def getCoastCurrentMatch(self, team_type):
        team_name = ""

        if(team_type == "h2h_home"):
            team_name = self.teamHome.getProperties()[0]
        else:
            team_name = self.teamAway.getProperties()[0]
        target_coast_class = ""
        if(team_name == self.driver.find_element_by_css_selector(".tname-home .participant-imglink").text):
            target_coast_class = ".fl"
        else:
            target_coast_class = ".fr"
        coast = list()
        players = self.driver.find_elements_by_css_selector(
            ".parts " + target_coast_class + " .name")[0:11:1]
        for i in range(len(players)):
            coast.append(players[i].text)
        if(team_type == "h2h_home"):
            self.teamHome.getCoastProcentCurentMatch(coast)
        else:
            self.teamAway.getCoastProcentCurentMatch(coast)

    # Функция выявления победителя
    def Reffery(self):
        TeamHomeStatistics = self.teamHome.getProperties()
        TeamAwayStatistics = self.teamAway.getProperties()
        countpointsTeamHome = 0
        countpointsTeamAway = 0

        for i in range(1, len(TeamHomeStatistics)):
            if(i != 3 and i != 7 and i != 8):
                if(TeamHomeStatistics[i] > TeamAwayStatistics[i]):
                    countpointsTeamHome = countpointsTeamHome + 1
                elif(TeamHomeStatistics[i] < TeamAwayStatistics[i]):
                    countpointsTeamAway = countpointsTeamAway + 1
            elif(i == 3 or i == 7 or i == 8):
                if(TeamHomeStatistics[i] < TeamAwayStatistics[i]):
                    countpointsTeamHome = countpointsTeamHome + 1
                elif(TeamHomeStatistics[i] > TeamAwayStatistics[i]):
                    countpointsTeamAway = countpointsTeamAway + 1

        reffery_response = "В матче: " + \
            TeamHomeStatistics[0] + " - " + TeamAwayStatistics[0] + "\n"
        raznica = countpointsTeamHome - countpointsTeamAway
        if(raznica < 0):
            raznica *= -1

        if(raznica == 1):
            reffery_response += "Я не уверен что они выиграют матч, но (поставь с иксом) на: "
        if(raznica == 2):
            reffery_response += "Если брать логически (поставь с иксом) на: "
        if(raznica == 3):
            reffery_response += "Я почти уверен! что победит: "
        if(raznica >= 4):
            reffery_response += "Железно, победит: "

        if(countpointsTeamHome > countpointsTeamAway):
            reffery_response += TeamHomeStatistics[0]
        elif(countpointsTeamHome < countpointsTeamAway):
            reffery_response += TeamAwayStatistics[0]
        else:
            reffery_response += "Я думаю будет ничья!"

        if(self.argument):
            reffery_response += "\n"
            for i in range(1, len(TeamHomeStatistics)):
                if(i == 1 and self.st_wins_last_mach):
                    reffery_response += "\nКолличество побед в последних " + \
                        str(self.statistics_from_count_match) + " матча: \n" + \
                        TeamHomeStatistics[0] + " " + str(TeamHomeStatistics[i]) + " - " + str(
                            TeamAwayStatistics[i]) + " " + TeamAwayStatistics[0]
                elif (i == 2 and self.st_wins_oponents_last_mach):
                    reffery_response += "\nКолличество побед в очных встречах: \n" + \
                        TeamHomeStatistics[0] + " " + str(TeamHomeStatistics[i]) + " - " + str(
                            TeamAwayStatistics[i]) + " " + TeamAwayStatistics[0]
                elif (i == 3 and self.st_coefficient):
                    reffery_response += "\nКоффициенты на победу: \n" + \
                        TeamHomeStatistics[0] + " " + str(TeamHomeStatistics[i]) + " - " + str(
                            TeamAwayStatistics[i]) + " " + TeamAwayStatistics[0]
                elif (i == 4 and self.st_xg_and_average_ball_possession):
                    reffery_response += "\nСреднее владение мячом: \n" + \
                        TeamHomeStatistics[0] + " " + str(TeamHomeStatistics[i]) + "% - " + str(
                            TeamAwayStatistics[i]) + "% " + TeamAwayStatistics[0]
                elif (i == 5 and self.st_xg_and_average_ball_possession):
                    reffery_response += "\nОжидаемое колличество голов: \n" + \
                        TeamHomeStatistics[0] + " " + str(float(TeamHomeStatistics[i])) + " - " + str(float(
                            TeamAwayStatistics[i])) + " " + TeamAwayStatistics[0]
                elif (i == 6 and self.st_xg_and_average_ball_possession):
                    reffery_response += "\n" + \
                        TeamHomeStatistics[0] + " побед дома: " + \
                        str(TeamHomeStatistics[i])
                    reffery_response += "\n" + \
                        TeamAwayStatistics[0] + " побед в гостях: " + \
                        str(TeamAwayStatistics[i])
                elif (i == 7 and self.st_place_in_the_table):
                    reffery_response += "\n" + \
                        TeamHomeStatistics[0] + " турнирная таблица: " + \
                        str(TeamHomeStatistics[i]) + " место"
                    reffery_response += "\n" + \
                        TeamAwayStatistics[0] + " турнирная таблица: " + \
                        str(TeamAwayStatistics[i]) + " место"
                if (i == 8 and self.st_place_in_the_table_form):
                    reffery_response += "\n" + \
                        TeamHomeStatistics[0] + " таблица прогресса: " + \
                        str(TeamHomeStatistics[i]) + " место"
                    reffery_response += "\n" + \
                        TeamAwayStatistics[0] + " таблица прогресса: " + \
                        str(TeamAwayStatistics[i]) + " место"
                if (i == 9 and self.st_main_cast):
                    reffery_response += "\nПроцент основного состава на игру: \n" + \
                        TeamHomeStatistics[0] + " " + str(TeamHomeStatistics[i]) + "% - " + str(
                            TeamAwayStatistics[i]) + "% " + TeamAwayStatistics[0]

            flag = " сильнее " if(countpointsTeamHome >
                                  countpointsTeamAway) else " слабее "
            reffery_response += "\nИз этого следует, что при сравнении этих показателей , команда " + \
                TeamHomeStatistics[0] + flag
            reffery_response += "команды " + TeamAwayStatistics[0] + "."

        return reffery_response

    def botStart(self):
        self.status = "Запускаем бота"
        # Настраиваем браузер
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(25)
        # Ответ функции
        response = list()
        time.sleep(3)
        try:
            self.driver.get(self.game_url)
            self.status = "Получаю названия команд"

            # Получаем название команд
            self.teamHome.setProperties("team_name", self.driver.find_element_by_css_selector(
                ".tname-home .participant-imglink").text)
            self.teamAway.setProperties("team_name", self.driver.find_element_by_css_selector(
                ".tname-away .participant-imglink").text)

            # Получаем колличество побед за последние 5 игр
            if(self.st_wins_last_mach):
                self.status = "Получаю колличество побед в последних " + str(self.statistics_from_count_match) + " играх"
                # Переходим во вкладку H2H
                self.driver.find_element_by_id("a-match-head-2-head").click()
                self.teamHome.getTeamCountWin(self.driver.find_element_by_id(
                    "tab-h2h-overall").get_attribute('innerHTML'), self.statistics_from_count_match)
                self.teamAway.getTeamCountWin(self.driver.find_element_by_id(
                    "tab-h2h-overall").get_attribute('innerHTML'), self.statistics_from_count_match)
            # Получаем колличество побед в очном противостоянии
            if(self.st_wins_oponents_last_mach):
                self.status = "Получаю колличество побед в последних " + str(self.statistics_from_count_match) + " очных встречах"
                try:
                    self.teamHome.getTeamVictoryVsOponents(self.driver.find_element_by_class_name(
                        "h2h_mutual").get_attribute('innerHTML'), self.statistics_from_count_match)
                    self.teamAway.getTeamVictoryVsOponents(self.driver.find_element_by_class_name(
                        "h2h_mutual").get_attribute('innerHTML'), self.statistics_from_count_match)
                except:
                    print("Данные команды не играли друг с другом")
            # Получаем коффициенты
            if(self.st_coefficient):
                self.status = "Получаю коффициенты"
                flag_comments_type = "default-live-odds"
                try:
                    self.driver.find_element_by_class("live-offer2")
                    flag_comments_type = "#default-live-odds"
                except:
                    flag_comments_type = "#default-odds"
                try:
                    self.teamHome.setProperties("coefficient", float(self.driver.find_element_by_css_selector(
                        flag_comments_type + " .o_1 span .odds-wrap").text))
                    self.teamAway.setProperties("coefficient", float(self.driver.find_element_by_css_selector(
                        flag_comments_type + " .o_2 span .odds-wrap").text))
                except:
                    print("У данной игры нет коффициентов")
            # Переходим во вкладку таблица и получаем таблицу лиги
            if(self.st_place_in_the_table):
                self.status = "Получаю места в таблице"
                try:
                    self.driver.find_element_by_id("a-match-standings").click()
                    table = self.driver.find_element_by_id(
                        "table-type-1").get_attribute('innerHTML')
                    # Получаем место в таблице
                    self.teamHome.getTeamTablePlace(table)
                    self.teamAway.getTeamTablePlace(table)
                except:
                    print("У данного соревнования  нет таблицы")
            # Переходим во вкладку таблица->форма и получаем место в таблице прогресса на данный момент
            if(self.st_place_in_the_table_form):
                self.status = "Получаю места в таблице прогресса"
                try:
                    self.driver.find_element_by_id("tabitem-form").click()
                    table = self.driver.find_element_by_id(
                        "table-type-5-5").get_attribute('innerHTML')
                    # Получаем место в таблице
                    self.teamHome.getTeamTableFormPlace(table)
                    self.teamAway.getTeamTableFormPlace(table)
                except:
                    print("У данного соревнования  нет таблицы")
            # Переходим во вкладку H2H и собираем и прощитываем статистику
            if(self.st_xg_and_average_ball_possession):
                self.status = "Собираю статистику команд"
                self.driver.find_element_by_id("a-match-head-2-head").click()
                if(self.statistics_from_count_match > 5):
                    time.sleep(1)
                    show_more = self.driver.find_elements_by_class_name(
                        "show_more")
                    try:
                        show_more[0].click()
                        show_more[1].click()
                    except:
                        print("Одна из команд сыграла меньше 5 игры")

                # Получаем статистику и xg
                self.getStatisticsFromNMatch("h2h_home")
                self.getStatisticsFromNMatch("h2h_away")
            # Считаем сколько команда выйграли игр дома или в гостях(смотря по данной игре) в n играх
            if(self.st_game_type_win):
                status = "Получаем колличество побед дома - в гостях"
                # Получаем процент выигрыша команды дома
                self.driver.find_element_by_id("h2h-home").click()
                # Получаем колличество побед в сыгранных дома матчах
                html_table_team_game_home = self.driver.find_elements_by_css_selector(
                    "#tab-h2h-home .h2h-wrapper")[0].get_attribute('innerHTML')
                self.teamHome.getTeamGameTypeWin(
                    html_table_team_game_home, self.statistics_from_count_match)
                # Получаем процент выигрыша команд в гостях
                self.driver.find_element_by_id("h2h-away").click()
                html_table_team_game_home = self.driver.find_elements_by_css_selector(
                    "#tab-h2h-away .h2h-wrapper")[0].get_attribute('innerHTML')
                self.teamAway.getTeamGameTypeWin(
                    html_table_team_game_home, self.statistics_from_count_match)
            # Берем составы на данную игры
            if(self.st_main_cast):
                self.status = "Просматриваю составы команд"
                try:
                    self.driver.find_element_by_id("a-match-summary").click()
                    self.driver.find_element_by_id("a-match-lineups").click()
                except:
                    print("На данный момент команды не обьявили основные составы.")
                # Получаем составы команд на данную игру
                coatHomeTeam = self.getCoastCurrentMatch("h2h_home")
                coastAwayTeam = self.getCoastCurrentMatch("h2h_away")
            
            self.status = "Сравниваю показатели команд"
            # Закрываем браузер
            self.driver.quit()
            # Находим победителя
            reffery_result = self.Reffery()
            self.result_mach.append("Success")
            self.result_mach.append(reffery_result)
            return self.result_mach
        except:
            self.driver.quit()
            self.result_mach.append("Error")
            self.result_mach.append(
                "Возможно у вас не стабильное подключение к интернету, попробуйте еще раз.")
            return self.result_mach
