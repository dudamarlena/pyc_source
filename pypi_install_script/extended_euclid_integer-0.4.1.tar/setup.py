from distutils.core import setup

setup(
  name = 'extended_euclid_integer',                                                     #название библиотеки
  packages = ['extended_euclid_integer'],                                               #имя пакета, расположение файлов
  version = '0.4.1',                                                                      #версия
  license='MIT',                                                                        #кодовое название лицензии
  description = 'modular inverse',                                                      #описание
  author = 'Vova Nenashkin',                                                            #автор
  author_email = 'nenashkinvov@gmail.com',                                              #почта
  url = 'https://github.com/SuLG-ik/Euclid-Algorithm',                                  #ссылка на github проект
  download_url = 'https://github.com/SuLG-ik/Euclid-Algorithm/archive/master.zip',      #ссылка для скачивания с github
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],                                       #ключевые слова  
  classifiers=[
    'Development Status :: 3 - Alpha',                                                  #статус библиотеки
    'Intended Audience :: Developers',                                                  #целевая аудитория
    'Topic :: Software Development :: Build Tools',                                     #тема
    'License :: OSI Approved :: MIT License',                                           #лицензия
    'Programming Language :: Python :: 3',                                              #язык программирования
  ],
)
