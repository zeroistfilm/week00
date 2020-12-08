
import jwt


encoded = jwt.encode({'password': 'iqwqqqd'},'junggle', algorithm='HS512')

print(encoded)
decode=jwt.decode(encoded, 'junggle', algorithms=['HS512', 'HS256'])
print(decode)