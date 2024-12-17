from Assets import AoCAssets as ac
import re


class day13:
    def __init__(self, filename):
        self.data = ac.read_file(filename)
        self.game_data = self.parse_data()
        self.solution1 = self.part1()

    def parse_data(self):
        game = {}
        i = 1
        game[i] = {}
        for line in self.data:
            if line.startswith("Button A"):
                result = re.search(r"X\+(.*), Y\+(.*)", line)
                game[i]['Xmovea'] = int(result.group(1))
                game[i]['Ymovea'] = int(result.group(2))
            elif line.startswith("Button B"):
                result = re.search(r"X\+(.*), Y\+(.*)", line)
                game[i]['Xmoveb'] = int(result.group(1))
                game[i]['Ymoveb'] = int(result.group(2))
            elif line.startswith("Prize"):
                result = re.search(r"X=(.*), Y=(.*)", line)
                game[i]['Xfinal'] = int(result.group(1))
                game[i]['Yfinal'] = int(result.group(2))
            elif line == "":
                i = i+1
                game[i] = {}
            else:
                print('unexpected input')
        return(game)

    def part1(self):
        total = 0
        for k, v in self.game_data.items():
            z = v['Xfinal']/v['Xmovea']
            c = z - ((v['Xmoveb'] * (v['Yfinal']/v['Ymoveb']))/v['Xmovea'])
            d = v['Xmoveb']/(v['Ymoveb'] * v['Xmovea'])
            a = c/(1-(v['Ymovea'] * d))
            b = (v['Yfinal'] - v['Ymovea']*a)/v['Ymoveb']
            if (round(a, 3)%1 == 0) and (round(b, 3)%1 == 0):
                total = total + (a*3) + b
        print(total)
        return int(total)
