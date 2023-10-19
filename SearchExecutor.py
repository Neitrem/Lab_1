from db.DBE import DBExecutor
import pymorphy2


class SearchExecutor():
    
    __db_exec = None

    def __init__(self, DBexec: DBExecutor) -> None:
        self.__db_exec = DBexec

    def ProcessRequest(self, request: str) -> (str, str):

        print(request)
        word_list = self.__split_request(request=request)
        word_list = self.__lower(word_list)
        search_req_list = self.__create_requests_list(word_list)
        answer = self.__compare_requests(search_req_list)
        if (answer[0] != "ERROR"):
            self.__update_syn_data(answer[0])

        return answer
    
    def __update_syn_data(self, answer):
        for i in answer:
            print(i)
            if not i['status']:
                self.__db_exec.updateSynonym(i['stored_word'], i['search_word'])

        # self.__db_exec.updateSynonym()

    def __lower(self, word_list):
        for i in range(len(word_list)):
            word_list[i] = word_list[i].lower()

        return word_list

    def __split_request(self, request: str) -> list:
        request_raw = request.split()

        def pos(word, morth=pymorphy2.MorphAnalyzer()):
            "Return a likely part of speech for the *word*."""
            return morth.parse(word)[0].tag.POS

        functors_pos = {'INTJ', 'PRCL', 'PREP'}  # function words
        
        return [word for word in request_raw if pos(word) not in functors_pos]
    
    

    def __create_requests_list(self, request: list) -> list:
        synonyms_lines = [[i[1], i[2] ]for i in self.__db_exec.getSynonyms()]

        res = []

        def find_syn_line(word: str) -> list:
            for syn_line in synonyms_lines:
                if word in syn_line:
                    return syn_line
            return [word]
        
        def compare_lists(l1, l2) -> bool:
            for i in range(len(l1)):
                if(l1[i] != l2[i]):
                    return False
            return True
        
        def add_request(var_req):
            for i in res:
                if compare_lists(i, var_req):
                    return
            res.append(var_req)
        
        def create_posible_request(req: list, i=0):
            for pos in range(i, len(req)):
                syn_line = find_syn_line(req[pos])
                for syn in syn_line:
                    r = list(req)
                    r[pos] = syn
                    add_request(r)
                    if i < len(req):
                        create_posible_request(r, pos+1)

        
        create_posible_request(request)
        return res
            
    def __compare_requests(self, search_req_list) -> dict:
        stored_requests_data = [[self.__split_request(i[1]), i[2]] for i in self.__db_exec.getRequests()]
        answ_persentage = []

        for stored_request_data in stored_requests_data: # обходит все сохранённые запросы
            for search_request in search_req_list: # обходит все возможные запросы пользователя
                stored_request_words  = self.__lower(stored_request_data[0]) # список слов из сохранённого запроса
                if(len(stored_request_words) == len(search_request)): # проверяем соответствует ли длинна
                    count = 0
                    temp_data = list()
                    for i in range(len(stored_request_words)): # обходим и сравниваем все слова из обоих списков
                        status = True
                        # print(stored_request_words[i], search_request[i])
                        if(stored_request_words[i] == search_request[i]):
                            count += 1
                        else:
                            status = False
                        temp_data.append({
                            "status": status,
                            "stored_word": stored_request_words[i],
                            "search_word": search_request[i],
                        })
                    result_comparing = count / len(stored_request_words)
                    if(result_comparing >= 0.75):
                        return temp_data, stored_request_data[1]
                    
        return "ERROR", 'Ошибка поиска, недостаточно совпадений'


