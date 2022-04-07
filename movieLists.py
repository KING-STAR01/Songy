


class GetLinks:
    movielinkslist = []

    def __init__(self):
        self.get()

    def get(self):
        with open("movielinks.txt") as file:
            for i in file:

                GetLinks.movielinkslist.append(i[:-1])


class GetNames:
    movielist = []

    def __init__(self):
        self.get()

    def get(self):
        with open("movienames.txt") as file:
            for i in file:
                i = i.replace('(',"")
                i = i.replace(')',"")
                GetNames.movielist.append(i[:-1])


if __name__ == "__main__":
    obj = GetLinks()

    obj1 = GetNames()
    print(obj.movielinkslist)
    print(obj1.movielist)
