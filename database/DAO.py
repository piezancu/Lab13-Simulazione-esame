from database.DB_connect import DBConnect
from model.state import State


class DAO():

    @staticmethod
    def getAllYears():
        connessione = DBConnect.get_connection()
        cursor = connessione.cursor(dictionary=True)

        result = []

        query = """select distinct year(datetime) as y
                    from sighting s 
                    order by y desc"""

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["y"])

        cursor.close()
        connessione.close()

        return result

    @staticmethod
    def getAllShapes():
        connessione = DBConnect.get_connection()
        cursor = connessione.cursor(dictionary=True)

        result = []

        query = """select distinct shape 
                    from sighting s """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        connessione.close()

        return result

    @staticmethod
    def getAllStates():
        connessione = DBConnect.get_connection()
        cursor = connessione.cursor(dictionary=True)

        result = []

        query = """select * 
                    from state"""

        cursor.execute(query, ())

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        connessione.close()

        return result

    @staticmethod
    def getEdges(year, shape, idMap):
        connessione = DBConnect.get_connection()
        cursor = connessione.cursor(dictionary=True)

        result = []

        query = """select state1 st1, state2 st2, count(*) as peso
                    from neighbor n, sighting s
                    where (s.state = n.state1 or s.state = n.state2)
                        and year(s.datetime) = %s 
                        and s.shape = %s
                        and n.state1 < n.state2 
                    group by st1, st2"""

        cursor.execute(query, (year, shape,))

        for row in cursor:
            result.append((idMap[row["st1"]], idMap[row["st2"]], row["peso"]))

        cursor.close()
        connessione.close()

        return result

# query SBAGLIATA perche conta il numero di COPPIE di osservazioni che avvengono nello stesso anno
# negli stati 1 e 2
""" select n.state1 as st1, n.state2 as st2, count(*) as peso
    from neighbor n, sighting s1, sighting s2
    where year(s2.datetime) = year(s1.datetime) 
        and year(s2.datetime) = %s
        and s2.state = n.state2 and s1.state = n.state1
        and s1.shape = s2.shape and s2.shape = %s
    group by n.state1, n.state2 """

# ESAME 23/07/2018, nodi sono allStates, archi sono i vicini, il cui peso è il numero di avvistamenti 
# che distano massimo nGiorni in quell'anno nei 2 stati
@staticmethod
    def getEdges1(year, max_diff_g):
        connessione = DBConnect.get_connection()
        cursor = connessione.cursor()

        result = []

        query = """select s.state, s2.state, count(*)
                    from sighting s, sighting s2, neighbor n 
                    where year(s.`datetime`) = %s
                        and year(s2.`datetime`) = %s 
                        and s.state != s2.state 
                        and s.state = n.state1 
                        and s2.state = n.state2
                        and s.state < s2.state 
                        and datediff(s.`datetime`, s2.`datetime`) <= %s
                    group by s.state, s2.state """

        print("Creazione archi")
        cursor.execute(query, (year, year, max_diff_g,))
        print("Archi creati")

        for row in cursor:
            result.append((row[0], row[1], row[2]))

        cursor.close()
        connessione.close()

        return result
