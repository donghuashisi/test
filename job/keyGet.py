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

        if len(split_String) == row_start:
            return

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
        return

    def inqueryTable(self, key1=None, value1=None, key2=None):
        if self.table_Head == [] or self.table_Row == []:
            return None
        _value = ""
        _index = self.table_Head.index(key2)
        _index1 = self.table_Head.index(key1)
        for x in self.table_Row:
            if str(x[_index1]) == value1:
                _value = x[_index]
        return _value


class StringtoKeyValue(object):

    def __init__(self, _string):
        self.string = _string
        self.keyValueList = {}
        self.getKeyValue(_string)

    def getKeyValue(self, string):
        a = string
        for i in a.split('\r\n'):
            if i == '':
                pass
            else:
                res = re.split(pattern=r'(\s\s+)|,', string=i)
                for x in res:
                    if x is not None and re.search(pattern=r':|=', string=x):
                        pair = x.split(":")
                        pair[0] = pair[0].strip()
                        pair[1] = pair[1].strip()
                        self.keyValueList[pair[0]] = pair[1]
        pass

    def getValueByKey(self, key=None):
        return self.keyValueList[key]

    def insertVlaueKey(self, key=None, value=None):
        pass


if __name__ == "__main__":

    a = "\r\nPort Channel IPv4 Sessions\r\nshisi\r\nshisi\r\nNeighAddr                              LD/RD         RH/RS     State     Int             Parent Int\r\n20.0.0.2                             4099/4100       Up        Up        Gi4             Po1            \r\n20.0.0.2                             4097/4101       Up        Up        Gi6             Po1            \r\n"
    a = "\r\nPort Channel IPv4 Sessions\r\nshisi\r\nshisi\r\n"
    myTableClass = StringtoTable(_string=a, descrLine=3)
    get = myTableClass.inqueryTable(key1="Int", value1="Gi4", key2="NeighAddr")
    print(get)

    b = '\r\nIPv6 Sessions\r\nNeighAddr                              LD/RD         RH/RS     State     Int\r\n2001:2001::2                            1/1          Up        Up        Gi4\r\nSession state is UP and not using echo function.\r\nSession Host: Hardware\r\nOurAddr: 2001:2001::1                           \r\nHandle: 1\r\nLocal Diag: 0, Demand mode: 0, Poll bit: 0\r\nMinTxInt: 50000, MinRxInt: 50000, Multiplier: 3\r\nReceived MinRxInt: 50000, Received Multiplier: 3\r\nHolddown (hits): 0(0), Hello (hits): 50(0)\r\nRx Count: 2068, Rx Interval (ms) min/max/avg: 38/49/43\r\nTx Count: 2753, Tx Interval (ms) min/max/avg: 24/45/33\r\nElapsed time watermarks: 0 0 (last: 0)\r\nRegistered protocols: IPv6 Static CEF \r\nTemplate: bfd_tempalte\r\nUptime: 00:01:44\r\nLast packet: Version: 1                  - Diagnostic: 0\r\n             State bit: Up               - Demand bit: 0\r\n             Poll bit: 0                 - Final bit: 0\r\n             C bit: 1                                   \r\n             Multiplier: 3               - Length: 24\r\n             My Discr.: 1                - Your Discr.: 1\r\n             Min tx interval: 50000      - Min rx interval: 50000\r\n             Min Echo interval: 0       \r\n'
    myKeyValueContain = StringtoKeyValue(b)
    print(myKeyValueContain.keyValueList)
    print(myKeyValueContain.getValueByKey(key='Multiplier'))
