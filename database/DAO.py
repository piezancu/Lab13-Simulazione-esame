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

