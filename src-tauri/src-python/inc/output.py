from inc import init
import time, os
from inc import common, config
import platform, threading

VERSION = '软工 1.0'
OS = platform.system()

def get_time1():
    return time.strftime("@ %Y-%m-%d /%H:%M:%S/", time.localtime())

def get_time2():
    return time.strftime("%H:%M:%S", time.localtime())

def start_output():
    threading.Thread(target=run_output_queue).start()

def close_output():
    exit_queue = common.get_value("exit_queue")
    exit_queue.get()
    output_report(common.get_value("success_list"))

def run_output_queue():
    output_queue = common.get_value("output_queue")
    exit_queue = common.get_value("exit_queue")
    while common.get_value("current_times") < common.get_value("total_times"):
        result = output_queue.get()
        output_result(result)
    exit_queue.put(True)

def put_output_queue(result):
    output_queue = common.get_value("output_queue")
    output_queue.put(result)

def output_result(result):
    current_target, current_script = result['url'], result['script']
    output_path = common.get_value("output_path")
    common.set_value("current_times", common.get_value("current_times") + 1)
    success_times = common.get_value("success_times")
    success_list = common.get_value("success_list")
    percent_num = int(common.get_value('current_times') / common.get_value('total_times') * 100)
    percent_str = f"[{percent_num}% {success_times}]" if common.get_value("show_progress") else ""
    try:
        if not result.get("name"):
            log_info(f"检测超时 {percent_str} {current_target} script: {current_script} ")
            return False
        if result['vulnerable']:
            log_success(f'检测到: {result["name"]} from script {current_script}, 目标: {current_target}')
            result['script'] = current_script
            result['url'] = current_target
            common.set_value("success_times", success_times + 1)
            success_list.append(result)
            data_save(output_path, result)
            return result
        else:
            log_info(f"正在检测 {percent_str} {current_target.rstrip('/')} poc: {result['name']}")
            return False
    except:
        log_error(f'poc中产生一个错误 script: {current_script}')
        return False

def output_report(succeed_result):
    output_path = common.get_value("output_path")
    log_info('所有检测任务完成, 即将生成报告......')
    if len(succeed_result) != 0:
        print('----')
        for result in succeed_result:
            for r in result.keys():
                if r == 'name':
                    print(f'[!] {r.capitalize()}: {result[r]}')
                    print(f'    {"script".capitalize()}: {result["script"]}')
                    print(f'    {"url".capitalize()}: {result["url"]}')
                elif r != 'script' and r != 'url':
                    print(f'      {r.capitalize()}: {result[r]}')
        print('----')
        if output_path != '':
            log_info(f'已将报告写入至 {os.path.join(os.path.abspath("."), output_path)}!')
        else:
            log_warning('程序没有生成任何报告类文件以记录此次任务的数据')
    else:
        log_critical('所有测试已结束但是程序未生成任何报告')

def data_save(output_path, result):
    if output_path == '': return
    with open(output_path, 'a+') as report_file:
        value = ''
        for r in result.keys():
            if str(r) == 'name':
                value += f'[!] {r.capitalize()}: {result["name"]}\n'
            else:
                value += f'     {r.capitalize()}: {result[r]}\n'
        report_file.write(value)

def log_info(mess):
    print(f"[INFO] {mess}")

def log_success(mess):
    print(f"[SUCCESS] {mess}")

def log_warning(mess):
    print(f"[WARNING] {mess}")

def log_critical(mess):
    print(f"[CRITICAL] {mess}")

def log_error(mess):
    print(f"[ERROR] {mess}")

def show(script_list):
    pocinfo_dict = {}
    for script in script_list:
        pocinfo_dict[script] = common.get_value("pocinfo_dict")[script]
    poc_info_list = []
    exp_num = 0
    log_info('loading POC/EXP ......')
    for pocinfo in pocinfo_dict.keys():
        poc_modole = pocinfo_dict[pocinfo]
        path = poc_modole.__file__
        try:
            result = poc_modole.verify("http://0.0.0.0")
            name = result['name']
        except:
            continue
        if result.get("attack"):
            attack = result['attack']
            exp_num += 1
        else:
            attack = False
        poc_info = (name, path, attack)
        poc_info_list.append(poc_info)

    for (name, path, attack) in poc_info_list:
        if attack:
            print(f'[+] Name: {name}\n    Attack: True')
        else:
            print(f'[+] Name: {name}')
        print('    Script: {path.split("\\")[-1] if "Windows" in OS else path.split("/")[-1]}')
        print('    Path: {path}\n')

    print(f"\n\t\t\t\t\t\t\t\t\t\tTotal POC: {len(poc_info_list)} EXP: {exp_num}")

def logo():
    print("\t "*5 + f"Version: {VERSION}\n")

def usage():
    print('''
        用法:
                获取poc/exp信息:   python3 run.py --show
                单目标检测:        python3 run.py -u http://xxx.xxx.xx 
                批量检测:          python3 run.py -f url.txt -o report.txt
                指定poc检测:       python3 run.py -f url.txt --poc="thinkphp2_rce.py"
                exp攻击模式:       python3 run.py -u 目标url --poc="指定poc文件" --attack
        参数:
                -u  --url      目标url
                -f  --file     指定目标url文件   
                -o  --output   指定生成报告的文件(默认{0})
                -p  --poc      指定单个或多个poc进行检测, 直接传入poc文件名, 多个poc用(,)分开
                -t  --thread   指定线程池最大并发数量(默认{1})
                -to --timeout  指定poc最大超时时间(默认{2}s)
                -d  --delay    指定poc休眠时间(默认{3}s)
                --show         展示poc/exp详细信息
                --attack       使用poc文件中的exp进行攻击'''.format(
        "不生成" if len(config.output_path) == 0 else config.output_path,
        config.max_threads, config.timeout,
        config.delay,
    ), end='')

