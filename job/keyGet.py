import re
import sys
import json


class StringtoTable(object):
    """
    type 0:
                        Session          Up          Down
    Total                     2           2             0

    type 1:
    Port Channel IPv4 Sessions
    NeighAddr                              LD/RD         RH/RS     State     Int             Parent Int
    20.0.0.1                             4100/4099       Up        Up        Gi4             Po1
    20.0.0.1                             4101/4097       Up        Up        Gi5             Po1
    """

    def __init__(self, _string, descrLine=2):
        self.table_Head = []
        self.table_Row = []
        self.table_Type = 1
        self.descrLine = descrLine
        self.createTable(_string)

    def createTable(self, _string):

        def delSpace(_list):
            if '' in _list:
                _list.remove('')
            return _list

        row_start = self.descrLine
        a = _string
        row_Head = []
        row_Content = []
        split_String = []
        count = 0
        for x in a.split('\r\n'):
            if x == '':
                pass
            else:
                split_String.append(x)

        for x in split_String[row_start:]:
            # split table into string,one row---> a string
            if len(x) is not 0:
                if count is 0:  # deal with tabel header
                    regex = re.compile('\s\s+')
                    row_Head = delSpace(regex.split(x))
                else:  # deal with tabel content row
                    regex = re.compile('\s+')
                    row_Content.append(delSpace(regex.split(x)))
                count = count + 1
        # finish tabel operatioin
        # tabel type (heaer == row elem or header == row elem-1)
        if len(row_Head) == len(row_Content[0]):
            self.table_Type = 1
        elif len(row_Head) == len(row_Content[0]) - 1:
            self.table_Type = 0
            row_Head.insert(0, 'None')
        else:
            self.table_Type = -1

        self.table_Head = row_Head
        self.table_Row = row_Content

    def inqueryTable(self, key1=None, value1=None, key2=None):
        _value = None
        _index = self.table_Head.index(key2)
        _index1 = self.table_Head.index(key1)
        for x in self.table_Row:
            if str(x[_index1]) == value1:
                _value = x[_index]
        return _value


if __name__ == "__main__":
    a = "\r\nPort Channel IPv4 Sessions\r\nshisi\r\nshisi\r\nNeighAddr                              LD/RD         RH/RS     State     Int             Parent Int\r\n20.0.0.2                             4099/4100       Up        Up        Gi4             Po1            \r\n20.0.0.2                             4097/4101       Up        Up        Gi6             Po1            \r\n"
    print(a)
    myTableClass = StringtoTable(_string=a, descrLine=3)
    get = myTableClass.inqueryTable(key1="Int", value1="Gi4", key2="NeighAddr")
    print(get)
