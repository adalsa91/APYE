# Práctica 0: Git y GitHub
##Prerrequisitos
- [x] Rellenar la hoja de cálculo correspondiente la equivalencia entre nombre real y nick en GitHub.
- [x] Cumplimentar los objetivos de la primera sesión.
## Configurar entorno
### 1. Clave ssh
Generamos el par de claves:

    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

Añadimos la clave pública creada a nuestra cuenta de GitHub:

![Clave ssh GitHub](https://github.com/adalsa91/PracticasIV/blob/hito0/images/practica0/image1.png)

### 2. Parámetros de Git
Introducimos el nombre y correo electrónico que se mostrará en los commits.

    $ git config --global user.name "Adrian Alvarez"
    $ git config --global user.email email@example.com

También configuramos el editor por defetco:

    $ git config --global core.editor emacs

![Configuración de Git](https://github.com/adalsa91/PracticasIV/blob/hito0/images/practica0/image2.png)

###3. Completar perfil de GitHub
![Perfil GitHub](https://github.com/adalsa91/PracticasIV/blob/hito0/practica0/image3.png)


## Creación del repositorio del proyecto
### 1.Inicializar proyecto
Al crear el proyecto podemos elegir inicializar el archivo **.gitignore**, el archivo **README** y elegir una licencia.

![Inicialización del respositorio del proyecto](https://github.com/adalsa91/PracticasIV/blob/hito0/practica0/image4.png)

### 2. Creación de rama para hito 0
Creamos una nueva rama para la práctica 0.

    $ git checkout -b hito0

Y subimos la nueva rama al remoto.

    & git push origin hito0

### 3. Creación de hitos e issues
A través de la web de GitHub creamos un hito (Milestone) para agrupar las tareas (issues) del hito 0.

![Creación del hito 0](https://github.com/adalsa91/PracticasIV/blob/hito0/practica0/image5.png)

Ahora creamos tareas referentes a ese hito.
