## Control the klinger MD4

import visa
rm = visa.ResourceManager()
print(rm.list_resources())

klinger = rm.open_resource('GPIB0::8::INSTR')
klinger.write_termination = '\r'
klinger.read_termination = '\r'
print(klinger.write("PW0"))
print(klinger.write("DW"))

print(klinger.read())
print(klinger.write("PW1"))