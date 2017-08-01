import bs4
import dryscrape
import requests

csrf = "RcGcTDU7TdyCz5RjbwiEarAtQnjdghrG"
sess_id = "2WYuXtHco+9UWhqbFK4nrCc4ehgDPmkPbxSKwXSTWu4="

session = dryscrape.Session()
session.visit("https://www.openlearning.com/unswcourses")
