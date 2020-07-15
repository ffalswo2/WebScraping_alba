from urllib import parse
import re

a = parse.quote('%7C%7C%B8%B6%C6%F7%B1%B8%7C%7C%C0%FC%C3%BC%2C')

print(a.encode('utf-16'))