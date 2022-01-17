from enum import unique
import pyvcard
from mimetypes import MimeTypes
import datetime


class ContactData:
    def _vcard(self, builder):
        pass

    def _from_vcard(self, source):
        pass

    def set(self, tuple):
        pass


class NameContactData(ContactData):
    def __init__(self, source=None, name_first=True):
        self._name = ["" for i in range(5)]
        self.name_first = name_first
        self._from_vcard(source)

    def set(self, tuple):
        if isinstance(tuple, str):
            tuple = tuple.split(" ")
            if self.name_first:
                if len(tuple) > 2:
                    self.prefix = tuple[0]
                    self.given_name = tuple[1],
                    self.additional_name = tuple[2]
                    self.surname = tuple[3]
                    self.suffix = tuple[4]
                elif len(tuple) == 2:
                    self.surname = tuple[1]
                    self.given_name = tuple[0]
                elif len(tuple) == 1:
                    self.given_name = tuple[0]
            else:
                if len(tuple) > 2:
                    self.prefix = tuple[0]
                    self.given_name = tuple[2],
                    self.additional_name = tuple[3]
                    self.surname = tuple[1]
                    self.suffix = tuple[4]
                elif len(tuple) == 2:
                    self.surname = tuple[0]
                    self.given_name = tuple[1]
                elif len(tuple) == 1:
                    self.given_name = tuple[0]
        else:
            if len(tuple) < 5:
                raise ValueError(
                    "Required 5 arguments for name data, not", len(tuple))
            self._name = list(tuple)[:5]

    @property
    def suffix(self):
        return self._name[4]

    @property
    def given_name(self):
        return self._name[1]

    @property
    def surname(self):
        return self._name[0]

    @property
    def prefix(self):
        return self._name[3]

    @property
    def additional_name(self):
        return self._name[2]

    @suffix.setter
    def suffix(self, value: str):
        self._name[4] = value

    @given_name.setter
    def given_name(self, value: str):
        self._name[1] = value

    @surname.setter
    def surname(self, value):
        self._name[0] = value

    @prefix.setter
    def prefix(self, value):
        self._name[3] = value

    @additional_name.setter
    def additional_name(self, value):
        self._name[2] = value

    def fullname(self):
        if self.name_first:
            return " ".join([self.prefix, self.given_name,
                             self.additional_name, self.surname, self.suffix])
        else:
            return " ".join([
                self.prefix, self.surname, self.given_name,
                self.additional_name, self.suffix])

    def __repr__(self):
        return self.fullname()

    def _vcard(self, builder):
        builder.add_property("N", list(self._name))
        builder.add_property("FN", self.fullname())

    def _from_vcard(self, source):
        if pyvcard.is_vcard_property(source):
            self._name = list(source.values)


class EmailContactData(ContactData):
    DEFINED_TYPES = ["home", "work", "pref", "other"]

    def __init__(self, source=None):
        self._type = ["internet"]
        self._email = None
        self._from_vcard(source)

    @property
    def type(self):
        return self._type

    @property
    def email(self):
        return self._email

    def preferred(self):
        return "pref" in self.type

    def set(self, tuple):
        if len(tuple) < 2:
            raise ValueError(
                "Required 2 arguments to email data: type and email")
        type = tuple[0].split(",")
        self._type.extend(type)
        self._email = tuple[1]

    def _vcard(self, builder):
        if self.email:
            builder.add_property("EMAIL", self._email, params={} if not self._type else {
                                 "TYPE": ",".join(self._type)})

    def _from_vcard(self, source):
        if pyvcard.is_vcard_property(source):
            self._email = source.value
            if "TYPE" in source.params:
                self._type = source.params["TYPE"].split(",")

    def __repr__(self):
        return self.email


class TelContactData(ContactData):
    DEFINED_TYPES = [
        'home', 'msg', 'work', 'pref', 'voice', 'fax',
        'cell', 'video', 'pager', 'bbs', 'modem', 'car',
        'text', 'isdn', 'pcs', 'textphone', 'main', 'other'
    ]

    def __init__(self, source=None):
        self._type = None
        self._phone = None
        self._from_vcard(source)

    @property
    def type(self):
        return self._type

    @property
    def phone(self):
        return self._phone

    def integer(self):
        return pyvcard.strinteger(self.phone)

    def set(self, tuple):
        if len(tuple) < 2:
            raise ValueError(
                "Required 2 arguments to telnumber data: type and number")
        type = tuple[0].split(",")
        self._type.extend(type)
        self._phone = tuple[1]

    def _vcard(self, builder):
        if self.phone:
            builder.add_property("TEL", self._phone, params={} if not self._type else {
                                 "TYPE": ",".join(self._type)})

    def _from_vcard(self, source):
        if pyvcard.is_vcard_property(source):
            self._phone = source.value
            if "TYPE" in source.params:
                self._type = source.params["TYPE"].split(",")

    def __repr__(self):
        return self.phone


class AddressContactData(ContactData):
    DEFINED_TYPES = [
        'pref',
        'dom',
        'intl',
        'postal',
        'parcel',
        'home',
        'work',
        'other',
    ]

    def __init__(self, source=None):
        self._type = None
        self._adr = ["" for i in range(7)]
        self._from_vcard(source)

    @property
    def type(self):
        return self._type

    @property
    def adr(self):
        return self._adr

    def __repr__(self):
        return " ".join(self._adr).strip()

    def set(self, tuple):
        if len(tuple) < 2:
            raise ValueError(
                "Required 2 arguments to address data: type and street address")
        type = tuple[0].split(",")
        self._type.extend(type)
        self._adr[2] = tuple[1]

    def _vcard(self, builder):
        if self._adr:
            builder.add_property("ADR", list(self._adr), params={} if not self._type else {
                                 "TYPE": ",".join(self._type)})

    def _from_vcard(self, source):
        if pyvcard.is_vcard_property(source):
            self._adr = source.values
            if "TYPE" in source.params:
                self._type = source.params["TYPE"].split(",")


class OrganizationContactData(ContactData):
    def __init__(self, sources=None):
        self._title = None
        self._org = None
        self._from_vcard(sources)

    @property
    def title(self):
        return self._title

    @property
    def org(self):
        return self._org

    def __repr__(self):
        return "{} : {}".format(self.org, self.title)

    def set(self, tuple):
        if len(tuple) < 2:
            raise ValueError(
                "Required 2 arguments to organiztion data: org and title")
        self._org = [tuple[0]] if isinstance(tuple[0], str) else tuple[0]
        self._title = tuple[1]

    def _vcard(self, builder):
        if self.org:
            builder.add_property("ORG", list(self._org))
        if self.title:
            builder.add_property("TITLE", self._title)

    def _from_vcard(self, sources):
        if sources:
            for source in sources:
                if pyvcard.is_vcard_property(source):
                    if source.name == "ORG":
                        self._org = source.values
                    elif source.name == "TITLE":
                        self._title = source.value


class AnniversaryContactData(ContactData):
    def __init__(self, source=None):
        self._date = None
        self._from_vcard(source)

    @property
    def datetime(self):
        return self._date

    def _get_strdate(self):
        if isinstance(self._date, datetime.date):
            return self._date.strftime("%Y-%m-%d")
        elif isinstance(self._date, datetime.datetime):
            return self._date.strftime("%Y-%m-%dT%H:%M:%S")

    def __repr__(self):
        return self._get_strdate()

    def set(self, datetime):
        if isinstance(datetime, datetime.date) or isinstance(datetime.datetime):
            self._date = datetime

    def _vcard(self, builder):
        if self._date:
            date = self._get_strdate()
            builder.add_property("BDAY", date)

    def _from_vcard(self, source):
        if pyvcard.is_vcard_property(source):
            self._date = source.typedvalue.datetime


class PhotoContactData(ContactData):
    def __init__(self, source=None, islogo=False):
        self._bytes = None
        self._type = None
        self.islogo = islogo
        self._from_vcard(source)

    def set(self, path):
        if isinstance(path, str):
            m = MimeTypes()
            type = m.guess_type(path)[0].split("/")[1].upper()
            with open(path, "rb") as fobj:
                self._bytes = fobj.read()
        elif isinstance(path, bytes):
            self._bytes = path

    @property
    def bytes(self):
        return self._bytes

    @property
    def type(self):
        return self._type

    def _vcard(self, builder):
        if self._bytes:
            paramsdict = {"ENCODING": "b"}
            if self._type:
                paramsdict["TYPE"] = self._type
            builder.add_property(
                "PHOTO" if not self.islogo else "LOGO", self._bytes, params=paramsdict)

    def _from_vcard(self, source):
        if pyvcard.is_vcard_property(source):
            self._bytes = source.value
            if "TYPE" in source.params:
                self._type = source.params["TYPE"]


class ContactField:
    def __init__(self, type, unique=False):
        self._unique = unique
        self._type = type
        self._container = []

    @property
    def values(self):
        return tuple(self._container)

    def __getitem__(self, key):
        return self._container[key]

    def __len__(self):
        return len(self._container)

    def __iter__(self):
        return iter(self._container)

    def set(self, value):
        if self._unique:
            if type(value) != self._type:
                object = self._type()
                if isinstance(object, ContactData):
                    object.set(value)
            else:
                object = value
            if len(self) == 0:
                self._container = [object]
            else:
                self._container[0] = object
        else:
            if type(value) != self._type:
                object = self._type()
                if isinstance(object, ContactData):
                    object.set(value)
            else:
                object = value
            self._container.append(object)

    @property
    def value(self):
        return self._container[-1]

    def _vcard(self, builder):
        for cnt in self._container:
            if isinstance(cnt, ContactData):
                cnt._vcard(builder)


class Contact:
    def __init__(self, source=None):
        self.name = ContactField(NameContactData, True)
        self.tel = ContactField(TelContactData)
        self.email = ContactField(EmailContactData)
        self.nickname = ContactField(str, True)
        self.org = ContactField(OrganizationContactData, True)
        self.address = ContactField(AddressContactData)
        self.url = ContactField(str)
        self.note = ContactField(str, True)
        self.birthday = ContactField(AnniversaryContactData, True)
        self.photo = ContactField(PhotoContactData, True)
        self.logo = ContactField(PhotoContactData, True)
        self._importvcf(source)

    def exportvcf(self):
        builder = pyvcard.builder()
        builder.set_version("3.0")
        self.name._vcard(builder)
        self.tel._vcard(builder)
        self.address._vcard(builder)
        self.email._vcard(builder)
        self.org._vcard(builder)
        self.logo._vcard(builder)
        self.photo._vcard(builder)
        self.birthday._vcard(builder)
        for val in self.note.values:
            builder.add_property("NOTE", val)
        for val in self.url.values:
            builder.add_property("URL", val)
        for val in self.nickname.values:
            builder.add_property("NICKNAME", val)
        return builder.build()

    def _importvcf(self, source):
        tmp = []
        if pyvcard.is_vcard(source):
            source = pyvcard.migrate_vcard(source).migrate("3.0")
            for property in source:
                if property.name == "N":
                    self.name.set(NameContactData(property))
                elif property.name == "TEL":
                    self.tel.set(TelContactData(property))
                elif property.name == "ADR":
                    self.address.set(AddressContactData(property))
                elif property.name == "EMAIL":
                    self.email.set(EmailContactData(property))
                elif property.name == "NICKNAME":
                    self.nickname.set(property.value)
                elif property.name == "URL":
                    self.url.set(property.value)
                elif property.name == "NOTE":
                    self.note.set(property.value)
                elif property.name == "BDAY":
                    self.birthday.set(AnniversaryContactData(property))
                elif property.name == "PHOTO":
                    self.photo.set(PhotoContactData(property))
                elif property.name == "LOGO":
                    self.logo.set(PhotoContactData(property, True))
                elif property.name == "ORG" or property.name == "TITLE":
                    tmp.append(property)
        if tmp:
            self.org.set(OrganizationContactData(tmp))

    def __repr__(self):
        return f"Contact {self.name.value.fullname()}"

    def __str__(self):
        return self.name.value.fullname()
