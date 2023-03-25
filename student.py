class Student:
    def __init__(self, studentID, name, lastName):
        self._studentID = studentID
        self._name = name
        self._lastName = lastName
        self._email_list = []
        self._answers = []

    def addEmail(self, email):
        self._email_list.append(email)

    def addMiddleName(self,middleName):
        self._middleName_list.append(middleName)

    def checkEmail(self, email):
        for e_mail in self._email_list:
            if e_mail == email:
                return True
        return False

    def nameCheck(self, nameBlock, emailBlock):
        matched = False
        specialCase = False
        nameBlock = nameBlock.replace("İ", "i")
        nameBlock = nameBlock.lower()
        nameBlock = nameBlock.replace("ı", "i")
        nameBlock = nameBlock.replace("ü", "u")
        nameBlock = nameBlock.replace("ö", "o")
        nameBlock = nameBlock.replace("ç", "c")
        nameBlock = nameBlock.replace("ş", "s")
        nameBlock = nameBlock.replace("ğ", "g")


        name = []
        for element in self._name:
            element = element.replace("İ", "i")
            temp = element.lower()
            temp = temp.replace("ı", "i")
            temp = temp.replace("ü", "u")
            temp = temp.replace("ö", "o")
            temp = temp.replace("ç", "c")
            temp = temp.replace("ş", "s")
            temp = temp.replace("ğ", "g")
            name.append(temp)

        lastName = []
        for element in self._lastName:
            temp = element.replace("İ","i")
            temp = temp.lower()
            temp = temp.replace("ı", "i")
            temp = temp.replace("ü", "u")
            temp = temp.replace("ö", "o")
            temp = temp.replace("ç", "c")
            temp = temp.replace("ş", "s")
            temp = temp.replace("ğ", "g")
            lastName.append(temp)
        #Removing the numbers
        nameBlock = ''.join(i for i in nameBlock if not i.isdigit())
        if '@' not in nameBlock:
            splitted = nameBlock.split()
        else:
            splitted = nameBlock
        if emailBlock in self._email_list or nameBlock in self._email_list:
            return True

        if not matched:
            for lname in lastName:
                if lname in splitted:
                    for fname in name:
                        if fname in nameBlock:
                            matched = True
                            break
                        else:
                            tempNB = nameBlock.split()
                            for element in tempNB:
                                if element in fname:
                                    matched = True
                                    specialCase = True
                                    break
                if matched:
                    break
        if splitted[len(splitted) - 1] not in lastName and not specialCase and '@' not in nameBlock:
            matched = False
        elif splitted[0] not in name and not specialCase and '@' not in nameBlock:
            matched = False
            for fname in name:
                if fname in splitted[0]:
                    matched = True
                    break

        if matched:
            if emailBlock not in self._email_list:
                self._email_list.append(emailBlock)
        return matched