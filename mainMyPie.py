import zeichnePie
import os

def ZeichnePie(paramDict):
    labels = paramDict.get('labels')
    if len(labels) == 0:
        print('mainMyPie:ZeichnePie: keine labels. Das könnte sein! es wird nicht als Fehler betrachtet!')

    sizes = paramDict.get('sizes')
    if len(sizes) == 0:
        print('mainMyPie:ZeichnePie: keine sizes-Werte. Fehler! Abbruch!')
        return 1

    ozp = zeichnePie.ZeichnePie(paramDict)
    return 0

if __name__ == '__main__':
    title = 'My Pie'
    labels = [2001, 2002, 2003, 2004]
    sizes = [2, 5, 7, 3]
    paramDict = {}
    paramDict['labels'] = labels
    paramDict['sizes'] = sizes
    paramDict['title'] = title
    workDir = os.getcwd()
    paramDict['file'] = workDir + '/myPie.png'

    ZeichnePie(paramDict)


