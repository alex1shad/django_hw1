import os
import json
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('current_time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет,
    # возвращается просто текст
    current_time = datetime.now().time()
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей
    # директории
    root_path = os.getcwd()
    dir_list = os.listdir(root_path+'\\')
    final_list = []
    def dir_cimpile(final_list, dir_list, root_path):
        while dir_list:
            for root in dir_list:
                if '.' not in root:
                    try:
                        new_dir_list = os.listdir(root_path + '\\' + root)
                        new_root_path = root_path + '\\' + root
                        final_list.append({root: []})
                        new_final_list = final_list[-1][root]
                        dir_list.remove(root)
                        dir_cimpile(new_final_list, new_dir_list, new_root_path)
                    except:
                        final_list.append(root)
                        dir_list.remove(root)
                else:
                    final_list.append(root)
                    dir_list.remove(root)

    dir_cimpile(final_list, dir_list, root_path)
    final_file = json.dumps({'root': final_list})
    return HttpResponse(str(final_file))
