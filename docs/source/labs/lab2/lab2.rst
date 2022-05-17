*************
Laboratorio 2
*************

**Aspectos importantes del diseño y del Endpoint**
================
En este laboratorio se implementara una parte del eiemanager en el cual existe un archivo llamado devices.json que guarda la
informacion de los dispositivos, tanto de su nombre, como el tipo que son. tambien existe un archivo init que hacer que la 
carpeta se comporte como un modulo, y este almacena el modulo de punto de entrada, con la informacion del autor, email, y
version, luego un archivo llamado Command.py que abarca el comando ABC, el command runner, y los hilos. En la carpeta
config se encuentra un archivo llamad devices.json que da como ejemplos algunos dispositivos con su respectivo identificador,
nombre, tipo, comando e ip. En la carpeta device se encuentra un archivo llamado device.py que es donde se declaran los 
parametros que caracterizan a los dispositivos, por medio de funciones que contienen el nombre, el tipo, entre otros.
Dentro de la carpeta eie_commands, device, se encuentra el archivo DeviceManager.py, el cual administra el control de los 
dispositivos y contiene un init general, que inicializa los dispositivos dependiendo de su tipo haciendo un mapa del diccionario
Un init config que invoca la lista de dispositivos del archivo .json, hay otro que invoca su tipo y nombre para organizarlos 
en una lista, tambien dentro de la carpeta Device existe un archivo llamado computers.py el cual se conecta con el device y
tiene una clase que tiene el nombre y lista de los dispositivos.
