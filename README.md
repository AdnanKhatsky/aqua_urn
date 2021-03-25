# aqua_urn
1. Установи виртуального окружения : sudo apt install python3-venv
2. Создай и активируй : 1. python3 -m venv ravenv
                            2. source first_venv/bin/activate
3. Войди в виртуальное окружение : workon ravenv
4. Установи OpenCV: 1. python
                      2. import cv2
5. Проверь камеру: python test_cam.py
6. Заверши проверку: esc
7. Конвертируй цветовую модель: color_convert.py *** *** ***
8. Замаскируй объект: 1. Сделай фотографию объекта и сохрани её под именем object_1.JPG
                       2. python objects_color_detection.py
9. Заверши маскировку объекта: esc
10. Установи библиотеку imutils : pip install imutils
11. Отслеживание объекта : objects_traking.py
12. Если всё работает как надо, нажми на ecs, чтобы завершить отслеживание
13. Установи RPi.GPIO: pip install RPi.GPIO
14. Запусти отслеживание объекта, только теперь подключи мотор: python object_detection.py
15. Заверши отслеживание: esc
16. Определи центр видимости камеры: python objects_coordion.py
17. Заверши: esc
18. Запусти итоговый проект: aqua_urn_detection.py
