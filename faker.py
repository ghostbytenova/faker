import json, random, os
from unidecode import unidecode
from dataclasses import dataclass

whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation + whitespace
CACHE_OF_DATA = {}

@dataclass
class DateOfBirth:
    day: int 
    month: int 
    year: int

    @property
    def m(self):
        return str(self.month)
    @property
    def d(self):
        return str(self.day)
    @property
    def y(self):
        return str(self.year)
    @property
    def mm(self):
        return f"{self.month:02d}"
    @property
    def dd(self):
        return f"{self.day:02d}"
    @property
    def yy(self):
        return f"{self.year % 100:02d}"
    @property
    def yyyy(self) -> str:
        return str(self.year)
    def __str__(self):
        return self.format()
    def to_dict(self):
        return {"day": self.day, "month": self.month, "year": self.year}
    def to_list(self):
        return [self.day, self.month, self.year]
    def to_tuple(self):
        return (self.day, self.month, self.year)
    def format(self, fmt: str = "dd/mm/yyyy"):
        """Trả về chuỗi theo định dạng tùy ý."""
        return (
            fmt.replace("dd", self.dd)
            .replace("mm", self.mm)
            .replace("yyyy", self.y)
            .replace("yy", self.yy)
            .replace("d", self.d)
            .replace("m", self.m)
            .replace("y", self.y)
            )
    def json(self):
        return self.to_dict()
    
@dataclass
class Information:
    fullName: str
    firstName: str
    lastName: str
    ufirstName: str
    ulastName: str
    username: str
    birthday: DateOfBirth

    def __getitem__(self, key) -> str:
        return getattr(self, key)
    
    def __setitem__(self, key, value) -> None:
        return setattr(self, key, value)
    
    def json(self):
        my_set = self.__dict__
        my_set["birthday"] = self.birthday.json()
        return my_set

class FakerError(Exception):
    """ Generator name error"""

def generator(size=6, chars = None): 
    return ''.join(random.choice(chars) for _ in range(size))

class Faker:
    def __init__(self, 
                 lang = 'vietnamese', 
                 gender = 'all', 
                 datatype='txt'
                ):
        global CACHE_OF_DATA
        self.__names = []
        self.tmp: dict = {}
        self.called: list = []
        self.lang = lang
        self._gender = gender
        self.__path = os.path.dirname(__file__)
        firstname, lastname = None, None
        firstname = os.path.join(self.__path, 'data/%s/firstnames.txt' % lang)
        lastname = os.path.join(self.__path, 'data/%s/%s.%s' % (lang, gender, datatype))
        self.__first_names = {} 
        
        if "first_name" in CACHE_OF_DATA:
            self.__first_names = CACHE_OF_DATA["first_name"]
        else:
            self.__first_names = open(firstname, encoding='utf8').read().splitlines()
            CACHE_OF_DATA["first_name"] = self.__first_names
            
        if "names" not in CACHE_OF_DATA:
            with open(lastname, "r", encoding='utf8') as names:
                names = names.read()
                if datatype == 'txt':
                    self.__names = names.splitlines()
                    
                if datatype == 'json':
                    self.__names = json.load(names)
                
                CACHE_OF_DATA["names"] = self.__names
        else: 
            self.__names = CACHE_OF_DATA["names"]
            
    def first_name(self, unsigned = False)->str:
        r = random.choice(self.__first_names)
        self.called.append("firstname")
        if unsigned:
            r = unidecode(r)
        self.tmp['ufirst_name'] = unidecode(r)
        self.tmp['first_name'] = r
        return r

    def last_name(self, unsigned = False)->str:
        r = random.choice(self.__names)
        self.called.append("lastname")
        rand = random.randint(1, 2)
        if rand == 1 and self.lang == "vietnamese":
            if "girl" in self._gender:
                r = "Thị "+ r
            elif "boy" in self._gender:
                r = "Văn "+ r

        if unsigned:
            r = unidecode(r)
        self.tmp['ulast_name'] = unidecode(r)
        self.tmp['last_name'] = r
        return r

    def fullname(self, unsigned = False, returns = str):
        if "firstname" in self.called and "lastname" in self.called:
            first_name = self.tmp['ufirst_name'] if unsigned else self.tmp['first_name']
            last_name = self.tmp['ulast_name'] if unsigned else self.tmp['last_name']
        else:
            first_name = self.first_name(unsigned=unsigned)
            last_name = self.last_name(unsigned=unsigned)
        if unsigned:
            first_name = unidecode(first_name)
            last_name = unidecode(last_name)
        fullname = f"{first_name} {last_name}"
        if returns == str:
            return fullname
        if returns == "delim": 
            return f"{first_name}:{last_name}"
        if returns == tuple:
            return (first_name, last_name)

    def username(self, unsigned = True, ext = int, sep="_", range_ext = (1000, 2000))->str:
        first_name, last_name = self.fullname(unsigned=unsigned, returns=tuple)
        first_name = first_name.replace(" ", sep)
        last_name  = last_name.replace(" ", sep)

        extension = ""
        if range_ext is not None and ext is not None:
            if ext == int:
                # range_ext phải là tuple (min,max) số nguyên
                if not (isinstance(range_ext, tuple) and len(range_ext) == 2 and all(isinstance(x, int) for x in range_ext)):
                    raise FakerError("For ext=int, range_ext must be a tuple (min:int, max:int).")
                a, b = range_ext
                if a > b:
                    raise FakerError("range_ext min must be <= max.")
                extension = str(random.randint(a, b))

            elif ext == str:
                # range_ext có thể là: int (độ dài), tuple(min_len,max_len), hoặc chuỗi cố định
                if isinstance(range_ext, int):
                    length = range_ext
                elif isinstance(range_ext, tuple) and len(range_ext) == 2 and all(isinstance(x, int) for x in range_ext):
                    a, b = range_ext
                    if a > b:
                        raise FakerError("range_ext min must be <= max.")
                    length = random.randint(a, b)
                elif isinstance(range_ext, str):
                    extension = range_ext
                    length = 0
                else:
                    raise FakerError("For ext=str, range_ext must be an int length, (min:int,max:int), or a string.")

                if extension == "":
                    extension = generator(length)

            else:
                raise FakerError("ext must be int, str, or None.")

        username = f"{first_name}{sep}{last_name}"
        if extension:
            username = f"{username}{sep}{extension}"

        if unsigned:
            username = unidecode(username)
        return username
    
    @classmethod
    def generateUsername(cls, length: int = 20, sep="", chars=digits, lang="vietnamese", gender="all"):
        username = cls(lang=lang, gender=gender).username(range_ext=None, sep=sep)
        username_length = len(username)
        if username_length < length:
            username += generator(length - username_length, chars=chars)
        return username

    def email(self, server = "hotmail.com", sep="")->str:
        username = self.username(sep=sep)
        email =  str(username)+"@"+server
        return email

    @classmethod
    def generateInformation(cls, length = (15, 20), sep="_", chars=digits, lang="vietnamese", gender="all", birthday = (1990, 2008)):
        fakerInstance = cls(lang=lang, gender=gender)
        first_name = fakerInstance.first_name()
        last_name = fakerInstance.last_name()
        username = fakerInstance.username(sep=sep, range_ext=None)
        birthday = fakerInstance.birthday(min=birthday[0], max=birthday[1])
        username_length = len(username)
        if username_length < length[0]:
            h = length[1] - username_length
            if h > 6:
                username = username + birthday.format("ddmmyyyy")
            elif h > 4 and h <= 6:
                username = username+ birthday.yy
            elif h > 2 and h <= 4:
                username = username+ birthday.yyyy
            else:
                username = username+ birthday.yy
        
        return Information(
            fullName=f"{first_name} {last_name}",
            firstName=first_name,
            lastName=last_name,
            ufirstName=unidecode(first_name),
            ulastName=unidecode(last_name),
            username=username,
            birthday=birthday
        )

    @staticmethod
    def gender():
        gender = random.choice(['male', "female", "other"])
        return gender

    @staticmethod
    def password(min = 10, max = 20, letters = ascii_letters):
        if type(min) != int and type(max) != int:
            raise FakerError("Min or max must be type int")
        if min > max:
            raise FakerError("Please set max mustbe over min number")
        lettors:str = letters
        if type(letters) == list:
            lettors = ""
            for letter in letters:
                lettors+=str(letter)
        password = generator(random.randint(min, max), chars=lettors)
        return password

    def birthday(self, min = 1990, max = 2006):
        month = random.randint(1, 12)
        year = random.randint(min, max)
        if month == 2 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
            day = random.randint(1, 29)
        elif month == 2 and year % 4 !=0: 
            day = random.randint(1, 28)
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month != 2: 
            day = random.randint(1, 30)

        return DateOfBirth(day=day, month=month, year=year)


if __name__ == "__main__":
    new = Faker.generateInformation()
    print(new)
