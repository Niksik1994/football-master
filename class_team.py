from bs4 import BeautifulSoup
import math


class Team():

    # Название команды
    team_name = "_____"
    # Тип команды
    type_team = ""
    # Колличество матчей за которое ведется статистика
    count_match = 0
    # Сколько побед в последних 5 матчах
    wins_from_five_game = 0
    # Сколько побед в очном противостоянии
    victory_vs_oponents = 0
    # Коэфициент на победу
    coefficient = 0
    # Среднее владение мячом в последних 5 играх
    average_ball_possession = 0
    # Средний xg за последние 5 матчей
    xg = 0
    # Как команда играет в данной ситуации(если на выезде то на выезде если дома то дома)
    game_type_win = 0
    # Место в тернирной таблице в данный момент
    place_in_the_table = 0
    # Место в таблице по уровню игры
    place_in_the_table_form = 0
    # Процент основного состава
    main_cast = 0
    main_cast_list = ""

    # Функция инициализации
    def __init__(self, type_team, count_match):
        self.type_team = type_team
        self.count_match = count_match

    # Функция заполнения имяни
    def setProperties(self, properties, value):
        if(properties == "team_name"):
            self.team_name = value
        elif(properties == "wins_from_five_game"):
            self.wins_from_five_game = value
        elif(properties == "victory_vs_oponents"):
            self.victory_vs_oponents = value
        elif(properties == "coefficient"):
            self.coefficient = value
        elif(properties == "average_ball_possession"):
            self.average_ball_possession = value
        elif(properties == "xg"):
            self.xg = value
        elif(properties == "game_type_win"):
            self.game_type_win = value
        elif(properties == "place_in_the_table"):
            self.place_in_the_table = value
        elif(properties == "place_in_the_table_form"):
            self.place_in_the_table_form = value
        elif(properties == "main_cast"):
            self.main_cast = value

    # получаем статистику команды

    def getProperties(self):
        properties = list()
        properties.append(self.team_name)
        properties.append(self.wins_from_five_game)
        properties.append(self.victory_vs_oponents)
        properties.append(self.coefficient)
        properties.append(self.average_ball_possession)
        properties.append(self.xg)
        properties.append(self.game_type_win)
        properties.append(self.place_in_the_table)
        properties.append(self.place_in_the_table_form)
        properties.append(self.main_cast)
        return(properties)

    # получаем статистику команды
    def getPropertiesString(self):
        properties = ""
        properties = "Наименование команды: " + self.team_name + "\n"
        properties = properties + "Колличество попед в последних " + \
            str(self.count_match) + " играх: " + \
            str(self.wins_from_five_game) + "\n"
        properties = properties + "Колличество побед над опонентом в последних " + \
            str(self.count_match) + " очных встречах: " + \
            str(self.victory_vs_oponents) + "\n"
        properties = properties + "Коффициент на победу: " + \
            str(self.coefficient) + "\n"
        properties = properties + "Среднее владение мячем в последних " + \
            str(self.count_match) + " играх: " + \
            str(self.average_ball_possession) + "%\n"
        properties = "Процент основного состава составляет: " + \
            str(self.main_cast) + "%\n"
        properties = properties + \
            "Прогнозируемое колличество голов: " + str(self.xg) + "\n"
        type_string_home = "За последние " + \
            str(self.count_match) + " игр(ы) дома, команда выиграла: "
        type_string_away = "За последние " + \
            str(self.count_match) + " игр(ы) в гостях, команда выиграла: "
        game_type_win_procent = math.ceil(
            self.game_type_win / self.count_match * 100)
        properties = properties + (type_string_home if (self.type_team == "h2h_home") else type_string_away) + \
            str(self.game_type_win) + "(" + str(game_type_win_procent) + "%)\n"
        properties = properties + "Место команды в таблице на данный момент: " + \
            str(self.place_in_the_table) + "\n"
        properties = properties + "По последним " + \
            str(self.count_match) + " играм команду можно расположить на: " + \
            str(self.place_in_the_table_form) + " место\n"
        return(properties)

    def getTeamCountWin(self, source, count_match):
        soap = BeautifulSoup(source, 'html.parser')
        count_wins_team_home = soap.select(
            "." + self.type_team + " .winLose a")[0:count_match:1]
        count = 0
        for elem in count_wins_team_home:
            if(elem.get_text() == "В"):
                count = count + 1
        self.wins_from_five_game = count

    def getTeamVictoryVsOponents(self, source, count_match):
        soap = BeautifulSoup(source, 'html.parser')
        count_wins_team_home = soap.select(" tr td  span strong")[
            0:count_match:1]
        count = 0
        for elem in count_wins_team_home:
            if(elem.get_text() == self.team_name):
                count = count + 1
        self.victory_vs_oponents = count

    def getTeamGameTypeWin(self, source, count_match):
        soap = BeautifulSoup(source, 'html.parser')
        count_wins_team_home = soap.select(".highlight .winLose")[
            0:count_match:1]
        count = 0
        for elem in count_wins_team_home:
            if(elem.get_text() == "В"):
                count = count + 1
        self.game_type_win = count

    def getTeamTablePlace(self, source):
        soap = BeautifulSoup(source, 'html.parser')
        count_wins_team_home = soap.select(".team_name_span a")
        count = 0
        for elem in count_wins_team_home:
            if(elem.get_text() == self.team_name):
                count = count + 1
                break
            else:
                count = count + 1
        self.place_in_the_table = count

    def getTeamTableFormPlace(self, source):
        soap = BeautifulSoup(source, 'html.parser')
        count_wins_team_home = soap.select(".team_name_span a")
        count = 0
        for elem in count_wins_team_home:
            if(elem.get_text() == self.team_name):
                count = count + 1
                break
            else:
                count = count + 1
        self.place_in_the_table_form = count

    def getCoastList(self):
        return self.main_cast_list

    def getCoastProcentCurentMatch(self, coast):
        for i in range(len(coast)):
            if(coast[i] in self.main_cast_list):
                self.main_cast += 9
